# tennisim

[![PyPI version shields.io](https://img.shields.io/pypi/v/tennisim.svg)](https://pypi.org/project/tennisim/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tennisim.svg)](https://pypi.python.org/pypi/tennisim/)
[![Actions Status](https://github.com/mjam03/tennisim/workflows/Tests/badge.svg)](https://github.com/mjam03/tennisim/actions)
[![Actions Status](https://github.com/mjam03/tennisim/workflows/Release/badge.svg)](https://github.com/mjam03/tennisim/actions)
[![codecov](https://codecov.io/gh/mjam03/tennisim/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/mjam03/tennisim)

Simulate tennis points, games, sets and matches.

Small pure python package (no dependencies outside of standard lib) to simulate tennis using points-based modelling i.e. given a probability of a server winning a given point, simulate the outcome of:
 - points
 - games
 - sets
 - tiebreaks
 - matches

with the ability to alter various parameters to gain some intuition behind how the tennis scoring system impacts matches. Using this we can answer various questions like:
 - what effect does removing the second serve have on match duration?
 - if the probability of winning a point on serve is reflective of skill, then how do rule alterations affect the likelihood that the more skillful player will actually end up winning the match (not just a given point)?

# Installing

`pip install tennisim`

# Points-based Modelling

Points-based modelling is a popular model for modelling tennis matches where predictions for games, sets and matches depends on modelling every constituent point. This can lead to a wealth of data that can be used to generate in-play match odds as we can output distributions e.g. for a given starting point, if we simulate 1000 outcomes how many show that player 1 wins the next set?

For more background I wrote [this article on Towards Data Science](https://towardsdatascience.com/building-a-tennis-match-simulator-in-python-3add9af6bebe).