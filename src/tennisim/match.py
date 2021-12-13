from typing import Tuple

from tennisim.game import prob_game
from tennisim.set import prob_set
from tennisim.tiebreak import prob_tiebreak
from tennisim.utils import comb


def prob_match_outcome(
    p_set: float, st_a: int, st_b: int, sets: int = 3
) -> Tuple[float, dict]:

    # solve corners first - you win by winning best of sets
    win_m = sets // 2 + 1
    if st_a == win_m:
        return 1.00, {}
    elif st_b == win_m:
        return 0.00, {}

    poss_set_scores = [(win_m, x) for x in range(st_b, win_m)]
    need_set_scores = [(x - st_a, y - st_b) for x, y in poss_set_scores]

    match_outcomes = {}
    for ps, ns in zip(poss_set_scores, need_set_scores):
        # subtract 1 as has to win final set
        s_needed = ns[0] - 1
        sets_played = sum(ns) - 1
        prob_s = (
            p_set
            * comb(sets_played, s_needed)
            * p_set ** s_needed
            * (1 - p_set) ** (sets_played - s_needed)
        )
        match_outcomes[ps] = prob_s

    return sum(match_outcomes.values()), match_outcomes


def prob_match(
    p_a: float,
    p_b: float,
    st_a: int = 0,
    st_b: int = 0,
    g_a: int = 0,
    g_b: int = 0,
    pt_a: int = 0,
    pt_b: int = 0,
    sets: int = 3,
) -> float:

    # check corners first
    win_m = sets // 2 + 1
    if st_a == win_m:
        return 1.00
    elif st_b == win_m:
        return 0.00

    p_set = prob_set(p_a, p_b, 0, 0)
    # check if we haven't started yet
    if pt_a == 0 and pt_b == 0:
        if g_a == 0 and g_b == 0:
            if st_a == 0 and st_b == 0:
                return prob_match_outcome(p_set, 0, 0)[0]
            else:
                # we have sets played but no games yet
                p_this_set = p_set
        else:
            # we have played games in this set
            # let's compute prob of winning set
            p_this_set = prob_set(p_a, p_b, g_a, g_b)
    elif g_a == 6 and g_b == 6:
        # then we're in tiebreak
        # so prob of winning set different
        p_this_set = prob_tiebreak(p_a, p_b, pt_a, pt_b)[0]
    else:
        # we have played points in this game
        # we can compute prob of winning set
        # by adding prob we win set if we win this game
        # with prob we win this set if we lose this game
        p_this_game = prob_game(p_a, pt_a, pt_b)
        p_this_set_if_w = p_this_game * prob_set(p_a, p_b, g_a + 1, g_b)
        p_this_set_if_l = (1 - p_this_game) * prob_set(p_a, p_b, g_a, g_b + 1)
        p_this_set = p_this_set_if_w + p_this_set_if_l

    # so now we have the probability of winning the set we are in
    # prob we win match is prob we win if we win this set
    # plus prob we win if we lose this set

    p_match_w_set = (
        p_this_set * prob_match_outcome(p_set, st_a + 1, st_b, sets=sets)[0]
    )
    p_match_l_set = (1 - p_this_set) * prob_match_outcome(
        p_set, st_a, st_b + 1, sets=sets
    )[0]
    p_match = p_match_w_set + p_match_l_set
    return p_match
