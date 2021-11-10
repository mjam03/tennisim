from tennisim import __version__
from tennisim.sim import sim_game
from tennisim.sim import sim_match
from tennisim.sim import sim_point
from tennisim.sim import sim_set
from tennisim.sim import sim_tiebreak


def test_version():
    assert __version__ == "0.1.0"


def test_point_zero():
    simed_points = [sim_point(0) for x in range(0, 1000)]
    assert max(simed_points) == 0


def test_point_one():
    simed_points = [sim_point(1) for x in range(0, 1000)]
    assert min(simed_points) == 1


def test_game_zero():
    simed_games = [sim_game(0) for x in range(0, 1000)]
    simed_games = [x[1] for x in simed_games if x[1][-1] == (0, 4)]
    assert len(simed_games) == 1000


def test_game_one():
    simed_games = [sim_game(1) for x in range(0, 1000)]
    simed_games = [x for x in simed_games if x[1][-1] == (4, 0)]
    assert len(simed_games) == 1000


def test_set_zero():
    simed_sets = [sim_set(0, 1) for x in range(0, 1000)]
    simed_sets = [x for x in simed_sets if x[1][-1] == (0, 6)]
    assert len(simed_sets) == 1000


def test_set_one():
    simed_sets = [sim_set(1, 0) for x in range(0, 1000)]
    simed_sets = [x for x in simed_sets if x[1][-1] == (6, 0)]
    assert len(simed_sets) == 1000


def test_tiebreak_zero():
    simed_tbs = [sim_tiebreak(1, 0) for x in range(0, 1000)]
    simed_tbs = [x for x in simed_tbs if x[1][-1] == (7, 0)]
    assert len(simed_tbs) == 1000


def test_tiebreak_one():
    simed_tbs = [sim_tiebreak(0, 1) for x in range(0, 1000)]
    simed_tbs = [x for x in simed_tbs if x[1][-1] == (0, 7)]
    assert len(simed_tbs) == 1000


def test_set_inf():
    assert sim_set(1, 1) == ()


def test_match_zero():
    simed_matches = [sim_match(1, 0) for x in range(0, 1000)]
    simed_matches = [x for x in simed_matches if x[1][-1] == (2, 0)]
    assert len(simed_matches) == 1000


def test_match_one():
    simed_matches = [sim_match(0, 1) for x in range(0, 1000)]
    simed_matches = [x for x in simed_matches if x[1][-1] == (0, 2)]
    assert len(simed_matches) == 1000
