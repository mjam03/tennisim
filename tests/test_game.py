from tennisim.game import prob_deuce_occurs
from tennisim.game import prob_game
from tennisim.game import prob_game_outcome
from tennisim.game import prob_win_deuce
from tennisim.game import theory_game


class TestTheoryGame:
    """Tests for the `theory_game` function"""

    def test_theory_game_zero(self) -> None:
        assert theory_game(0) == 0

    def test_theory_game_one(self) -> None:
        assert theory_game(1) == 1


class TestProbDeuceOccurs:
    """Tests for the `prob_deuce_occurs` function"""

    def test_prob_deuce_occurs_in_deuce_one(self) -> None:
        assert prob_deuce_occurs(1, 3, 3) == 1

    def test_prob_deuce_occurs_in_deuce_zero(self) -> None:
        assert prob_deuce_occurs(0, 3, 3) == 1

    def test_prob_deuce_occurs_zero(self) -> None:
        assert prob_deuce_occurs(0, 0, 0) == 0

    def test_prob_deuce_occurs_one(self) -> None:
        assert prob_deuce_occurs(1, 0, 0) == 0

    def test_prob_deuce_occurs_half(self) -> None:
        assert prob_deuce_occurs(0.5, 0, 0) == 5 / 16


class TestProbGame:
    """Tests for the `prob_game` function"""

    def test_prob_game_one(self) -> None:
        assert min([prob_game(1, 0, x) for x in range(0, 4)]) == 1.0

    def test_prob_game_zero(self) -> None:
        assert max([prob_game(0, x, 0) for x in range(0, 4)]) == 0.0

    def test_prob_game_server_won(self) -> None:
        assert min([prob_game(x / 100, 4, 0) for x in range(0, 100)]) == 1.0

    def test_prob_game_returner_won(self) -> None:
        assert max([prob_game(x / 100, 0, 4) for x in range(0, 100)]) == 0.0

    def test_prob_game_deuce(self) -> None:
        assert prob_game(0.5, 3, 3) == 0.5

    def test_prob_game_deuce_adv_in(self) -> None:
        assert prob_game(0.5, 4, 3) == 0.5

    def test_prob_game_deuce_adv_out(self) -> None:
        assert prob_game(0.5, 3, 4) == 0.25

    def test_prob_game_win_in_deuce(self) -> None:
        assert prob_game(0.5, 5, 3) == 1.0

    def test_prob_game_lose_in_deuce(self) -> None:
        assert prob_game(0.5, 3, 5) == 0.0


class TestProbGameOutcome:
    """Tests for the `prob_game_outcome` function"""

    def test_prob_game_outcome_one_point_for(self) -> None:
        ps = [x / 100 for x in range(0, 100)]
        probs = [prob_game_outcome(x, 1, 0) == x for x in ps]
        assert min(probs) == 1

    def test_prob_game_outcome_one_point_against(self) -> None:
        ps = [x / 100 for x in range(0, 100)]
        probs = [prob_game_outcome(x, 0, 1) == (1 - x) for x in ps]
        assert min(probs) == 1


class TestProbWinDeuce:
    """Tests for the `prob_win_deuce` function"""

    def test_prob_win_deuce(self) -> None:
        assert prob_win_deuce(0.5) == 0.5
