from typing import List, Tuple

from tennisim.utils import comb


def compute_tb_outcomes(
    final_scores: List[Tuple[int, int]],
    needed_scores: List[Tuple[int, int]],
    p_a: float,
    p_b: float,
    pp: int,
) -> dict:
    """Given final scorelines and points already won by current server and
    returner, return:
     - the number of points that current server will serve ex final point
     - the number they will return ex final point
     - the probability they win the final point of the tb

    Args:
        final_scores (List[Tuple[int, int]]): tiebreak final scores e.g. (7,5)
        needed_scores (List[Tuple[int, int]]): implied needed scores
        p_a (float): probability current server wins point on serve
        p_b (float): probability current returner wins point on serve
        pp (int): points already played in tiebreak

    Returns:
        dict: results required to calculate probability of each final tb score
    """

    tb_outcomes = {}
    # loop to determine:
    # - pt_s: points 'a' will serve ex. final point
    # - pt_r: points 'a' will return ex. final point
    # - p_f: prob 'a' will win final point
    for fs, ns in zip(final_scores, needed_scores):
        # set points left to play for that given scoreline
        ptp = ns[0] + ns[1]
        # 4 scenarios now to determine service points each
        # and who serves the last point
        # 4 scenarios: [(odd pp, odd ptp), (odd pp, even ptp),...]
        if pp % 2 == 0:
            # then we have SR|RS|SR
            if ptp % 2 == 0:
                # then we have either SR|RS or SR|RS|SR
                if ptp % 4 == 0:
                    # then we serve final point
                    # e.g. SR|RS or SR|RS|SR|RS
                    pt_s = ptp // 2 - 1
                    pt_r = ptp // 2
                    p_f = p_a
                else:
                    # we return the final point
                    # e.g. SR or SR|RS|SR
                    pt_s = ptp // 2
                    pt_r = ptp // 2 - 1
                    p_f = 1 - p_b
            else:
                # we have SR|R or SR|RS|S
                if (ptp - 1) % 4 == 0:
                    # then we serve final point
                    pt_s = ptp // 2
                    pt_r = ptp // 2
                    p_f = p_a
                else:
                    pt_s = ptp // 2
                    pt_r = ptp // 2
                    p_f = 1 - p_b
        else:
            # then we have SS|RR|SS as odd points played
            if ptp % 2 == 0:
                # then we either have 'a' serves and returns 2 each
                # e.g. SS|RR or SS|RR|SS|RR
                # or 'a' serves 2 more e.g. SS|RR|SS
                if ptp % 4 == 0:
                    # then s and r is the same but return final point
                    pt_s = ptp // 2
                    pt_r = ptp // 2 - 1
                    p_f = 1 - p_b
                else:
                    # 'a' serves 2 more but serves final point
                    pt_s = ptp // 2
                    pt_r = ptp // 2 - 1
                    p_f = p_a
            else:
                # we have either SS|R or SS|RR|S SS|RR|SS|RR|S
                if (ptp - 1) % 4 == 0:
                    # then 'a' serves final point
                    # e.g. SS|RR|S or SS|RR|SS|RR|S
                    pt_s = ptp // 2
                    pt_r = ptp // 2
                    p_f = p_a
                else:
                    # 'a' returns final point
                    # e.g. SS|R or SS|RR|SS|R
                    pt_s = ptp // 2 + 1
                    pt_r = ptp // 2 - 1
                    p_f = 1 - p_b

        # add data to outcomes dict
        tb_outcomes[fs] = (ns, pt_s, pt_r, p_f)
    return tb_outcomes


def create_tb_outcomes(p_a: float, p_b: float, pt_a: int, pt_b: int) -> dict:
    """Given a first to 7 tiebreak, return tiebreak outcomes based on current
    scoreline. This is a helper function required to compute the probability
    of a given scoreline based on the current score.

    Args:
        p_a (float): probability current server wins point on serve
        p_b (float): probability current returner wins point on serve
        pt_a (int): points current server has already won
        pt_b (int): points current returner has already won

    Returns:
        dict: {final_tb_score: data_required_to_compute_prob}
    """

    # e.g. if current is 3-2 this will create [7-2, 7-3, 7-4, 7-5]
    final_scores = [(7, x) for x in range(pt_b, 5 + 1)]
    # e.g. if 3-2 then adjusts to points needed e.g. 7-2 becomes 5-0
    needed_scores = [(x - pt_a, y - pt_b) for x, y in final_scores]
    # points played var needed to know where we are in the service setup
    # e.g. if even then SR|SR|SR, if odd then SS|RR|SS etc.
    pp = pt_a + pt_b
    return compute_tb_outcomes(final_scores, needed_scores, p_a, p_b, pp)


def prob_tb_outcome(
    ns: Tuple[int, int],
    pt_s: int,
    pt_r: int,
    p_f: float,
    p_a: float,
    p_b: float,
) -> float:
    """For a given tiebreak score in points, ns, and the respective:
     - point count that current server will serve and return
     - prob of winning point on service for each player
     - prob that current server will win final point
    returns the probability of that outcome happening by taking into account
    all the possible paths that make that possible.


    Args:
        ns (Tuple[int, int]): needed scoreline e.g. (4,0) means current server
        needs to win 4 and current returner needs to win 0
        pt_s (int): point count that current server will serve
        pt_r (int): point count that current returner will serve
        p_f (float): probability that current server wins the final point
        p_a (float): probability current server wins point on serve
        p_b (float): probability current returner wins point on serve

    Returns:
        float: probability that tiebreak ends with given scoreline, ns
    """

    prob = 0.00
    # sub 1 as we know they win the final point
    n_a = ns[0] - 1
    # e.g. if 'a' needs 3 ex. final point this loops through [3, 2, 1, 0]
    for n_s in range(n_a + 1)[::-1]:
        if n_s <= pt_s:
            # if 'a' wins p points on serve, they need n_a - p on return
            n_r = n_a - n_s
            # check if it is possible to win this many return points
            if n_r >= 0 and n_r <= pt_r:
                # compute probabs
                p_serve = (
                    comb(pt_s, n_s) * p_a ** n_s * (1 - p_a) ** (pt_s - n_s)
                )
                p_return = (
                    comb(pt_r, n_r) * (1 - p_b) ** n_r * p_b ** (pt_r - n_r)
                )
                # multiply and also prob they win final point
                p_all = p_f * p_serve * p_return
                prob += p_all
    return prob


def prob_tiebreak(
    p_a: float, p_b: float, pt_a: int, pt_b: int
) -> Tuple[float, dict]:
    """Given a starting scoreline in a tiebreak, returns the probability that
    'a' (the current server) wins the tiebreak

    Args:
        p_a (float): probability that current server wins a point they serve
        p_b (float): probability that current returner wins a point they serve
        pt_a (int): points already won by current server
        pt_b (int): points already won by current returner

    Returns:
        float: probability that current server will win the tiebreak
    """
    # solve corners first - when set is over
    if pt_a == 7 and pt_b <= 5:
        # 'a' wins without extras
        return 1.00, {}
    elif pt_b == 7 and pt_a <= 5:
        # 'b' wins without extras
        return 0.00, {}
    # if at least 6-6
    elif pt_a > 5 and pt_b > 5:
        # if a has 2 more
        if pt_a - pt_b >= 2:
            # 'a' wins by being 2 clear
            return 1.00, {}
        elif pt_b - pt_a >= 2:
            # 'b' wins by being 2 clear
            return 0.00, {}

    # else we're still going so need to compute probabilities
    # let's start at most simple - when at 6-6 or higher
    # calc probability of both a and b winning 2 in a row
    p_a_two_in_row = p_a * (1 - p_b)
    p_b_two_in_row = (1 - p_a) * p_b
    # probab a wins when even score e.g. 6-6, 7-7
    # is ratio of their probab vs total
    p_a_wins_evens = p_a_two_in_row / (p_a_two_in_row + p_b_two_in_row)

    # now we can solve 6-6, 6-5, 5-6 and higher
    if (pt_a >= 6 and pt_b >= 5) or (pt_a >= 5 and pt_b >= 6):
        # if we're sitting level
        if pt_a == pt_b:
            # then simply need to be 2 clear
            return p_a_wins_evens, {}
        # if we're 1 up (above corners will set '2 up' to return 1)
        elif pt_a > pt_b:
            # then we just need to win one point and we know 'a' serves
            # or lose and then win extras
            return (p_a + (1 - p_a) * p_a_wins_evens), {}
        # if we're 1 behind
        elif pt_b > pt_a:
            # then we need to get back to deuce then win it
            return (p_a * p_a_wins_evens), {}

    # otherwise we are at 5-5 or less so need to compute probabilities
    # of winning pre 'extras' i.e. 2 clear points
    # to compute this we need to know the following things
    # - possible *final* scorelines for the set based on the current score
    # - based on that, the points a and b need to create that scoreline
    # - using points played, and points needed to play, who serves last point
    # - based on same info, how many points current server serves and returns
    tb_outcomes = create_tb_outcomes(p_a, p_b, pt_a, pt_b)
    tb_probabs = {}

    for outcome, [ns, pt_s, pt_r, p_f] in tb_outcomes.items():
        tb_probabs[outcome] = prob_tb_outcome(ns, pt_s, pt_r, p_f, p_a, p_b)

    # now we need to compute the probability we get to 6-6 and then win
    # score needed from here - add 1 to 'a' as we subtract that in the
    # below function that assumes 'a' wins final point but that
    # is not required here
    ns_6_6 = (6 - pt_a + 1, 6 - pt_b)
    # if we have even number of points to get to 6-6
    pts_6_6 = 12 - pt_a - pt_b
    if pts_6_6 % 2 == 0:
        # then serve and return same amount
        pt_s = pts_6_6 // 2
        pt_r = pts_6_6 // 2
    else:
        # 'a' serves one more
        pt_s = pts_6_6 // 2 + 1
        pt_r = pts_6_6 // 2
    p_6_6 = prob_tb_outcome(ns_6_6, pt_s, pt_r, 1, p_a, p_b)

    # if at 6-6 then prob of winning from here is above
    tb_probabs[(6, 6)] = p_6_6 * p_a_wins_evens

    return sum(tb_probabs.values()), tb_probabs
