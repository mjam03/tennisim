from math import factorial


def comb(n, r):
    return factorial(n) / (factorial(n - r) * factorial(r))
