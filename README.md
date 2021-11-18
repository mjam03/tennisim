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

# Example

Suppose we want to simulate a game of tennis. We define the probability that the server will win a given point:
```python
from tennisim.sim import sim_game

p = 0.7
sim_game(p)
```

This will simulate 1 game of tennis where the probability that the server will win any given point is `0.7`. It will return a tuple containing:
 - boolean result for if the server won the game
 - list of tuples for the score progression of the game

 We can then take this further and simulate 1,000 groups of 100 games to generate a distribution of results. This can be interesting when looking at how changes in the probability p or the length of a game impacts the servers win probability for the game.

 ```python
import numpy as np
from tennisim.sim import sim_game

# set params for simulation
games = 100
sims = 1000
probabs = np.linspace(0.5, 0.8, 4)
results = {}

# for each serve win probability
for p in probabs:
    # we now need to generate sims
    means = []
    game_lengths = []
    for i in range(0, sims):
        g_results = [sim_game(p) for x in range(games)]
        # get mean result
        mean_res = np.mean([x[0] for x in g_results])
        # get mean game length
        mean_length = np.mean([len(x[1]) for x in g_results])
        # join to results holders
        means.append(mean_res)
        game_lengths.append(mean_length)
    # add data to probab dict
    results[p] = (means, game_lengths)
 ```

 # Help
 
 For more info see the [documentation](https://mjam03.github.io/tennisim/)

 # License
 
 `tennisim` is free and open source software, distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).