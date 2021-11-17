import random
from typing import List
from typing import Tuple
from typing import Union


def sim_point(p_s: float) -> bool:
    """Simulate point in tennis by drawing from uni dist

    Args:
        p_s (float): probability server wins point

    Returns:
        bool: True if server won, False if not
    """
    return random.uniform(0, 1) <= p_s


def sim_game(p_s: float, ppg: int = 4) -> Tuple[bool, List[Tuple[int, int]]]:
    """Simulate game of tennis using just prob server wins point

    Args:
        p_s (float): probability server wins point
        ppg (int): points per game in case want to play with longer game length

    Returns:
        Tuple[bool, list]: tuple of True if server won game and list
        of tuples of points as the game progressed. E.g. if server won all
        points would return (True, [(1,0),(2,0),(3,0),(4,0)])
    """
    scores = []
    # s and r are points scored by server and returner
    s = 0
    r = 0
    # while game still going
    while (s < ppg) and (r < ppg):
        # simulate the point
        if sim_point(p_s):
            s += 1
        else:
            r += 1

        # add score tuple to the score list
        scores.append((s, r))

        # we need a catcher here if we get to 3-3
        # so that we can handle deuce
        if (s == (ppg - 1)) and (r == (ppg - 1)):
            # give a bit more space
            while (s < (ppg + 1)) and (r < (ppg + 1)):
                # simulate the point
                if sim_point(p_s):
                    s += 1
                else:
                    r += 1
                # add score tuple to the score list
                scores.append((s, r))

                # if we're at 4 all then bring us back to 3 all
                if (r == ppg) and (s == ppg):
                    s = ppg - 1
                    r = ppg - 1
            # if we've excited then must be game over after deuce
            if s == ppg + 1:
                return (True, scores)
            elif r == ppg + 1:
                return (False, scores)

    # if here then must have finished game pre-deuce
    # return True if server wins, false if returner
    if s == ppg:
        return (True, scores)
    else:
        return (False, scores)


def sim_tiebreak(
    a_s: float, b_s: float, a_first: bool = True
) -> Tuple[bool, list]:
    """Simulate tiebreak using probab of each player winning on serve

    Args:
        a_s (float): probability player a wins point on serve
        b_s (float): probability player b wins point on serve
        a_first (bool, optional): bool to mark who serves first.
        Defaults to True for player a to serve first

    Returns:
        Tuple[bool, list]: returns tuple of result (True if a won, false if b)
        and the progression of tiebreak points
    """
    tb_scores = []
    a = 0
    b = 0
    points_served = 0
    server = a_first

    # while we haven't exited due to tiebreak win condition being met
    while True:
        # then serve and sim point
        if server:
            point = sim_point(a_s)
            # if true then server has won
            if point:
                a += 1
            else:
                b += 1
        else:
            point = sim_point(b_s)
            # if true then server has won
            if point:
                b += 1
            else:
                a += 1
        tb_scores.append((a, b))

        # check to see if a has won
        if (a >= 7) and (a - b) >= 2:
            # a has won by being >=7 and 2 points clear
            return (True, tb_scores)

        # check to see if b has won
        if (b >= 7) and (b - a) >= 2:
            # b has won by being >=7 and 2 points clear
            return (False, tb_scores)

        # if we need to continue because no one won
        # then need to handle who serves next

        # add to points served var and determine new server
        points_served += 1
        # check at start to see if we have only served 1
        if len(tb_scores) == 1:
            # then only played 1, but swap server
            server = not server
            points_served = 0
        elif points_served == 2:
            # swap server as they have had their 2 serves
            server = not server
            # and reset count to 0
            points_served = 0


def sim_set(
    a_s: float, b_s: float, a_first: bool = True
) -> Union[Tuple, Tuple[bool, list, list]]:
    """Simulate set using probab of each player winning on serve

    Args:
        a_s (float): probability player a wins point on serve
        b_s (float): probability player b wins point on serve
        a_first (bool, optional): bool to mark who serves first.
        Defaults to True for player a to serve first

    Returns:
        Union[Tuple, Tuple[bool, list, list]]: returns tuple of
        result (True if a won, false if b), list of progression of game scores
        and list of progression of scores within games
    """
    # checker to prevent infinite tiebreak
    if (a_s == 1) and (b_s == 1):
        print("Each player will win every service point")
        print("Will enter infinite tiebreak loop")
        return ()

    # games is a storing variable for game scores
    game_scores = []
    # games stores game score in set
    games = []
    # a and b are count of games won for each player
    a = 0
    b = 0
    # while someone hasn't won the set yet
    # winning set handled by early exits below
    while True:
        # simulate the game and set new server
        if a_first:
            game = sim_game(a_s)
            a_first = not a_first
            # update score
            if game[0]:
                # a held serve
                a += 1
            else:
                # a was broken
                b += 1
        else:
            game = sim_game(b_s)
            a_first = not a_first
            # update score
            if game[0]:
                # b held serve
                b += 1
            else:
                # b was broken
                a += 1

        # add game to game list and scores
        game_scores.append(game[1])
        games.append((a, b))

        # check if a has won
        if a >= 6 and (a - b) >= 2:
            # a has won either 6-0/1/2/3/4
            # or a has won 7-5
            return (True, games, game_scores)

        # check if b has won
        if b >= 6 and (b - a) >= 2:
            # b has won either 6-0/1/2/3/4
            # or a has won 7-5
            return (False, games, game_scores)

        # check if we should start a tiebreak
        if a == 6 and b == 6:
            # then we are in a tie break
            tb_result = sim_tiebreak(a_s, b_s, a_first=a_first)
            # update score
            if tb_result[0]:
                a += 1
            else:
                b += 1
            games.append((a, b))
            game_scores.append(tb_result[1])
            # return result
            if a > b:
                return (True, games, game_scores)
            else:
                return (False, games, game_scores)


def sim_match(
    a_s: float, b_s: float, a_first: bool = True, best_of: int = 3
) -> Tuple[bool, list, list, list]:
    """Simulate tennis match using probab of each player winning on serve

    Args:
        a_s (float): probability player a wins point on serve
        b_s (float): probability player b wins point on serve
        a_first (bool, optional): bool to mark who serves first.
        Defaults to True for player a to serve first
        best_of (int, optional): how many sets to play best of. Defaults to 3.

    Returns:
        Tuple[bool, list, list, list]: returns tuple of result (true if a won,
        false if b won), progression of match scores, set scores and
        game scores within those sets
    """

    set_scores = []
    game_scores = []
    match_scores = []
    a = 0
    b = 0

    first_to = (best_of // 2) + 1
    starting_server = a_first

    while True:
        # simulate the set
        s = sim_set(a_s, b_s, a_first=starting_server)
        # add to set totals
        if s[0]:
            # a won the set
            a += 1
        else:
            # b won the set
            b += 1

        # update list vars
        game_scores.append(s[2])
        set_scores.append(s[1])
        match_scores.append((a, b))

        # check if we have finished the match yet
        if a == first_to:
            return (True, match_scores, set_scores, game_scores)
        if b == first_to:
            return (False, match_scores, set_scores, game_scores)

        # need to check who serves first in the next set
        if len(s[1]) % 2 != 0:
            # then we played an odd number of games so change
            starting_server = not starting_server
