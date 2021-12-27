from tennisim.utils import comb


def theory_game(p: float) -> float:
    """Given probability that server wins any given point, returns
    probability they win the game

    Args:
        p (float): Probability that server wins given point

    Returns:
        float: Theoretical probability that server wins game
    """
    # compute probab server wins to love
    p_4_0 = comb(4, 4) * p ** 4
    # compute probab server wins to 15
    p_4_1 = (comb(5, 4) - comb(4, 4)) * p ** 4 * (1 - p)
    # compute probab server wins to 30
    p_4_2 = (comb(6, 4) - comb(5, 4)) * p ** 4 * (1 - p) ** 2
    # compute probab server wins after going to deuce
    deuce = comb(6, 3) * (p ** 5 * (1 - p) ** 3) / (1 - 2 * p * (1 - p))
    # return sum which is total probab they win game
    return p_4_0 + p_4_1 + p_4_2 + deuce


def prob_game_outcome(p: float, x: int, y: int) -> float:
    """Returns prob server wins x points, returner y points
    given prob, p, server wins any point

    Args:
        p (float): probability server wins a point
        x (int): count of points server wins
        y (int): count of points returner wins

    Returns:
        float: probability that server wins x points, returner y points
    """
    return comb(x + y, x) * p ** x * (1 - p) ** y


def prob_win_deuce(p: float) -> float:
    """Given probability, p, that server wins a point, returns the probability
    that the server will win deuce if it happens

    Args:
        p (float): probability server wins a point

    Returns:
        float: probability that server will win deuce
    """
    # returns the probability of winning deuce
    return p ** 2 / (1 - 2 * p * (1 - p))


def prob_deuce_occurs(p: float, x: int, y: int) -> float:
    """Returns probability of deuce happening if server has won x already,
    returner has won y already and serve wins any given point with probab, p

    Args:
        p (float): probability server wins a point
        x (int): points already won by server
        y (int): points already won by returner

    Returns:
        float: probability that deuce occurs given server has won x points
        already and returner has won y
    """
    return comb(6 - x - y, 3 - x) * p ** (3 - x) * (1 - p) ** (3 - y)


def prob_game(p: float, x: int, y: int) -> float:
    """Given server wins any point with prob, p, has already won x points
    and returner has won y points, returns the probability the server will
    win the game

    Args:
        p (float): probability server wins a point
        x (int): points already won by server
        y (int): points already won by returner

    Returns:
        float: probability of winning the game
    """
    # start by returning corners
    if x == 4 and y < 3:
        # x has won pre deuce
        return 1
    elif y == 4 and x < 3:
        # y has won pre deuce
        return 0
    elif x == 5:
        # x has won in deuce
        return 1
    elif y == 5:
        # y has won in deuce
        return 0

    # now we solve when the game is not over yet
    # init var to hold sum of probabiltities
    prob = 0.00

    # if opponent has not got 3 points yet
    # then can win pre-deuce
    # let's compute these probabilities and add them on
    for opp_p in range(max(0, 3 - y)):
        probab = p * prob_game_outcome(p, 4 - x - 1, opp_p)
        prob += probab

    # if not in deuce yet
    if x <= 3 and y <= 3:
        # then compute probability of getting there
        p_deuce = prob_deuce_occurs(p, x, y)
        # compute probability win in deuce
        p_win_deuce = prob_win_deuce(p)
        # multiply and add on
        prob += p_deuce * p_win_deuce
    # else if in deuce but x at 'advantage'
    elif x == 4 and y == 3:
        # then just need to win one more point to win
        prob += p
    # else if in deuce but y at 'advantage'
    elif x == 3 and y == 4:
        # then need to win next point and then deuce
        prob += p * prob_win_deuce(p)
    return prob
