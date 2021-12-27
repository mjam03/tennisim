from tennisim.tiebreak import create_tb_outcomes
from tennisim.tiebreak import prob_tiebreak


class TestCreateTbOutcomes:
    """Tests for the `create_tb_outcomes` function"""

    def test_create_tb_outcomes_point_count(self) -> None:
        """test that point count 1 less than required scoreline as always win
        final point
        """
        outs = create_tb_outcomes(0.5, 0.5, 0, 0).values()
        p_to_serve = [x[1] for x in outs]
        p_to_return = [x[2] for x in outs]
        points = [x + y for x, y in zip(p_to_serve, p_to_return)]
        total_points = [sum(x[0]) for x in outs]
        assert all([(x - y) == 1 for x, y in zip(total_points, points)])


class TestProbTiebreak:
    """Tests for the `prob_tiebreak` function"""

    def test_prob_tiebreak_one(self) -> None:
        p_t = [prob_tiebreak(1, x / 100, 0, 0)[0] for x in range(0, 100)]
        assert all([x > 0.9999 for x in p_t])

    def test_prob_tiebreak_zero(self) -> None:
        p_t = [prob_tiebreak(0, x / 100, 0, 0)[0] for x in range(1, 101)]
        assert all([x < 0.00001 for x in p_t])

    def test_prob_tiebreak_server_win_seven_five(self) -> None:
        assert prob_tiebreak(0.5, 0.5, 7, 5) == (1.00, {})

    def test_prob_tiebreak_server_lose_five_seven(self) -> None:
        assert prob_tiebreak(0.5, 0.5, 5, 7) == (0.00, {})

    def test_prob_tiebreak_server_win_after_seven(self) -> None:
        assert prob_tiebreak(0.5, 0.5, 8, 6) == (1.00, {})

    def test_prob_tiebreak_server_lose_after_seven(self) -> None:
        assert prob_tiebreak(0.5, 0.5, 6, 8) == (0.00, {})

    def test_prob_tiebreak_six_all(self) -> None:
        """Test if six all"""
        assert prob_tiebreak(0.5, 0.5, 6, 6) == (0.5, {})

    def test_prob_tiebreak_six_five(self) -> None:
        p_win = 0.5 + 0.5 * 0.5
        assert prob_tiebreak(0.5, 0.5, 6, 5) == (p_win, {})

    def test_prob_tiebreak_five_six(self) -> None:
        p_win = 0.5 * 0.5
        assert prob_tiebreak(0.5, 0.5, 5, 6) == (p_win, {})

    def test_prob_tiebeak_odd_pp(slef) -> None:
        assert prob_tiebreak(1, 0.5, 5, 0)[0] == 1.0
