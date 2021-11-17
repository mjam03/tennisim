from math import factorial


def comb(n: int, r: int) -> float:
    """Returns combination count for binomial

    Args:
        n (int): how many options to choose from
        r (int): how many you want to choose

    Returns:
        int: count of combinations
    """
    return factorial(n) / (factorial(n - r) * factorial(r))


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
