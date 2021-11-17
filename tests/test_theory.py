from tennisim.theory import theory_game


class TestTheoryGame:
    """Tests for the `theory_game` function"""

    def test_theory_game_zero(self) -> None:
        assert theory_game(0) == 0

    def test_theory_game_one(self) -> None:
        assert theory_game(1) == 1
