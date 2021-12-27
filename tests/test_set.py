from tennisim.game import theory_game
from tennisim.set import prob_set
from tennisim.set import prob_set_outcome
from tennisim.tiebreak import prob_tiebreak


class TestProbSetOutcome:
    """Tests for the `set_outcome` function"""

    def test_prob_set_outcome_one(self) -> None:
        """Tests to ensure if guaranteed to win all games then do"""
        g_to_win = [x * 2 for x in range(1, 10)]
        s_ps = [
            prob_set_outcome((x, 0), x // 2, x // 2, 1, 1, 1) for x in g_to_win
        ]
        assert min(s_ps) == 1.0

    def test_prob_set_outcome_zero(self) -> None:
        """Tests to ensure if guaranteed to lose all games then do"""
        g_to_win = [x * 2 for x in range(1, 10)]
        s_ps = [
            prob_set_outcome((x, 0), x // 2, x // 2, 0, 0, 0) for x in g_to_win
        ]
        assert max(s_ps) == 0.0


class TestProbSet:
    """Tests for the `prob_set` function"""

    def test_prob_set_one(self) -> None:
        """Test if always win serve then never lose"""
        p_set = [prob_set(1, x / 1000, 0, 0) for x in range(0, 1000)]
        assert min(p_set) > 0.9999

    def test_prob_set_zero(self) -> None:
        """Test if always lose serve then never win"""
        p_set = [prob_set(0, x / 1000, 0, 0) for x in range(1, 1001)]
        assert max(p_set) < 0.0001

    def test_prob_set_already_won(self) -> None:
        """Test if we server already won then returns 1.0"""
        p_set = [prob_set(0.5, 0.5, 6, x) for x in range(0, 4)]
        assert min(p_set) == 1.0

    def test_prob_set_already_lost(self) -> None:
        """Test if we server already lost then returns 0.0"""
        p_set = [prob_set(0.5, 0.5, x, 6) for x in range(0, 4)]
        assert max(p_set) == 0.0

    def test_prob_set_pre_tb_win(self) -> None:
        """Test if 7-5 then server wins"""
        assert prob_set(0.5, 0.5, 7, 5) == 1.0

    def test_prob_set_pre_tb_lose(self) -> None:
        """Test if 7-5 then server wins"""
        assert prob_set(0.5, 0.5, 5, 7) == 0.0

    def test_prob_set_go_to_tiebreak(self) -> None:
        """Tests that if 6 all then returns same as tiebreak function"""
        assert prob_set(0.5, 0.5, 6, 6) == prob_tiebreak(0.5, 0.5, 0, 0)[0]

    def test_prob_set_one_game_left_server(self) -> None:
        """Prob should be equal to win game plus lose but win tb"""
        p_s = [x / 100 for x in range(0, 101)]
        p_set = [prob_set(x, 0.5, 6, 5) for x in p_s]
        p_game = [theory_game(x) for x in p_s]
        p_tb = [prob_tiebreak(x, 0.5, 0, 0)[0] for x in p_s]
        p_test = [x + (1 - x) * y for x, y in zip(p_game, p_tb)]
        assert max([abs(x - y) for x, y in zip(p_test, p_set)]) == 0.0

    def test_prob_set_one_game_left_returner(self) -> None:
        """Prob should be equal to win game and then win tb"""
        p_s = [x / 100 for x in range(0, 101)]
        p_set = [prob_set(x, 0.5, 5, 6) for x in p_s]
        p_game = [theory_game(x) for x in p_s]
        p_tb = [prob_tiebreak(x, 0.5, 0, 0)[0] for x in p_s]
        p_test = [x * y for x, y in zip(p_game, p_tb)]
        assert max([abs(x - y) for x, y in zip(p_test, p_set)]) == 0.0

    def test_prob_set_five_five(self) -> None:
        """Test that 5-5 outcome is as expected"""
        assert prob_set(0.5, 0.5, 5, 5) == 0.5
