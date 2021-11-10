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
