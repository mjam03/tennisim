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