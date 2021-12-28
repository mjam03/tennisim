from typing import List, Tuple

from tennisim.game import theory_game
from tennisim.tiebreak import prob_tiebreak
from tennisim.utils import comb


def prob_set_outcome(
    score: Tuple[int, int],
    g_s: int,
    g_r: int,
    s_a: float,
    r_a: float,
    f_a: float,
) -> float:

    """For a given score outcome in games, returns the probability of that
    scoreline occurring given:
     - how many games the current server will serve and return
     - the prob of them winning service and return games

    Args:
        score (tuple): games server and returner needs to win for scoreline
        g_s (int): games current server will serve (ex final game)
        g_r (int): games current returner will serve (ex final game)
        s_a (float): prob server wins their service game
        r_a (float): prob server wins a return game
        f_a (float): prob server wins final game (already determined if serve
        or return)

    Returns:
        float: Probability of set scoreline occuring
    """

    # quick check to ensure that our inputs are correct
    # the sum of games to serve and games to return should equal
    # our desired scoreline
    # if g_s + g_r != sum(score):

    # get games you need to win and lose
    g_to_win = score[0]
    # init var to hold probab
    prob = 0.0

    # now let's loop through possible combinations of getting there
    # starting from win as many games on your serve as possible
    # then break a few (if needed) to achieve g_to_win
    # all the way to losing as many as possible on your serve
    # and breaking all the rest needed
    # all while ensuring we hit the target of g_to_win

    for g in range(g_to_win + 1)[::-1]:
        # win them all on your serve
        # if we have enough services
        if g <= g_s:
            # define return games we need to win to make up g_to_win
            r_to_win = g_to_win - g
            # if winning g service games, there are enough return games left
            # s.t. we can still win overall g_to_win
            if r_to_win >= 0 and r_to_win <= g_r:
                # then compute probability
                p = (
                    f_a
                    * comb(g_s, g)
                    * s_a ** g
                    * (1 - s_a) ** (g_s - g)
                    * comb(g_r, r_to_win)
                    * r_a ** r_to_win
                    * (1 - r_a) ** (g_r - r_to_win)
                )
                # add to total prob
                prob += p

    return prob


def prob_set(p_a: float, p_b: float, g_a: int, g_b: int) -> float:

    """Given probabilities for server and returner to win points on their
    respective serves, and the games already won by each, returns the prob
    that the current server will win the set

    Args:
        p_a (float): prob current server wins any point on their serve
        p_b (float): prob current returner wins any point on their serve
        g_a (int): games already won by current server
        g_b (int): games already won by current returner

    Returns:
        float: Probability that current server will win the set
    """

    # solve corners first
    if g_a == 7:
        # then a won either 7-5 or post tiebreak
        return 1.0
    elif g_b == 7:
        # then b won either 5-7 or post tiebreak
        return 0.0
    elif g_a == 6 and g_b < 5:
        # then a won pre tiebreak
        return 1.0
    elif g_b == 6 and g_a < 5:
        # then b won pre tiebreak
        return 0.0

    # we're not over yet, so we're either in 1 of 4 states:
    # about to start a tiebreak at 6-6
    # server or returner is leading 6-5 / 5-6
    # 5-5 so either heading for tb or 7-5 / 5-7 win
    # something else i.e. game _could_ finish being won with 6 games
    # let's go 1 by 1

    # var to store probab that we will add to for each outcome
    prob = 0.0

    # first let's store our probab of current server winning game
    # both on serve and when returning
    s_a: float = theory_game(p_a)
    r_a: float = 1.0 - theory_game(p_b)

    # probability of winning tiebreak
    prob_tb = prob_tiebreak(p_a, p_b, 0, 0)[0]

    # 6-6: let's solve if we are at 6-6
    if g_a == 6 and g_b == 6:
        return prob_tb
    # 6-5: else if g_a is one game away then
    elif g_a == 6 and g_b == 5:
        # they can either win it outright
        # or lose this game but win tiebreak
        return s_a + (1 - s_a) * prob_tb
    # 5-6 else if they are behind by 1
    elif g_a == 5 and g_b == 6:
        # they only have 1 option - win this game and the tiebreak
        return s_a * prob_tb
    # 5-5: else we may be at 5-5
    elif g_a == 5 and g_b == 5:
        # we can win by
        # - winning our serve then breaking theirs
        # - winning ours, losing theirs then winning the tiebreak
        # - losing ours, breaking theirs then winning the tiebreak
        p_7_5 = s_a * r_a
        p_6_6 = s_a * (1 - r_a) + (1 - s_a) * r_a
        return p_7_5 + p_6_6 * prob_tb
    # 'open play': we are not yet in the above stages
    else:
        # we now need to calculate 2 subsets
        # - the probability we win with 6 games i.e. pre 5-5
        # - the probability of reaching 5-5 * probab we win at 5-5
        # the p_5_5 is just the same as above
        # but need to know who is serving first at 5-5

        # pre 5-5
        a_needs = 6 - g_a
        # e.g. for (2,2) currently, gives [(4,0), (4,1), (4,2)]
        poss_scores: List[Tuple[int, int]] = [
            (a_needs, x) for x in range(4 - g_b + 1)
        ]
        # find who serves final game
        # given 'a' serves this game, if odd total game count
        # then 'a' will serve final, else 'b'
        # store prob 'a' wins final game for each poss scores
        poss_gc = [sum(x) for x in poss_scores]
        f_a = [[r_a, s_a][x % 2] for x in poss_gc]
        # now get the count of games to serve and return for 'a'
        # excluding the final game
        # e.g. if scoreline (4,0) then 2 serve games each left
        # but final will be returning (as 'a' serves this game)
        # so we would have (2,1) - 'a' serves 2, returns 1
        # with final game a return game

        # games (excl. final if 'a' serves it) left for 'a' to serve
        g_s: List[int] = [x // 2 for x in poss_gc]
        # games (excl. final if 'a' returns it) left for 'a' to return
        g_r: List[int] = [
            x // 2 if (x % 2 != 0) else (x // 2) - 1 for x in poss_gc
        ]

        # we now can amend our scorelines to subtract 1 from what 'a' needs
        # as we know that 'a' wins the final game (required to end the set)
        poss_scores = [(x - 1, y) for x, y in poss_scores]

        # we now have our components to compute the prob of finishing pre-tb
        # we have:
        # - poss games needed to w/l for given final set score (ex final game)
        # - prob of winning final game
        # - ex final game, counts of serve and return games (and their probs)

        # re-org our components by flipping lists
        # so we have a list of [scoreline, g_s, g_r, s_a, r_a, f_a]
        pre_tb_data = (
            poss_scores,
            g_s,
            g_r,
            [s_a for x in g_s],
            [r_a for x in g_s],
            f_a,
        )
        pre_tb_d = [list(i) for i in zip(*pre_tb_data)]

        # now for each outcome compute probab
        for poss_score, g_s_o, g_r_o, s_a_o, r_a_o, f_a_o in pre_tb_d:
            # and add on to our overall win probab
            prob += prob_set_outcome(
                poss_score, g_s_o, g_r_o, s_a_o, r_a_o, f_a_o
            )

        # now we need to compute probab of getting to 5-5
        games_to_5 = 10 - g_a - g_b
        # if odd num then 'a' serves more
        g_s_5_5 = games_to_5 // 2 + (1 if games_to_5 % 2 != 0 else 0)
        g_r_5_5 = games_to_5 // 2
        p_5_5 = prob_set_outcome(
            (5 - g_a, 5 - g_b), g_s_5_5, g_r_5_5, s_a, r_a, 1
        )

        # at 5-5 we have 2 options to win
        # either we win the next 2 games
        # or we win/lose or lose/win and win the tiebreak
        p_7_5 = p_5_5 * s_a * r_a
        p_6_6 = p_5_5 * (s_a * (1 - r_a) + (1 - s_a) * r_a)
        # i thinbk this bit might need refined so that the tiebreak
        # has serve dependency i.e. we work out who should serve first
        # in the tiebreak and then calculate the probability of winning
        # based on that
        p_win_tb = p_6_6 * prob_tb
        prob += p_7_5 + p_win_tb

    return prob
