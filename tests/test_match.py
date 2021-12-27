from tennisim.match import prob_match
from tennisim.match import prob_match_outcome
from tennisim.set import prob_set


class TestProbMatchOutcome:
    """Tests for the `prob_match_outcome` function"""

    def test_prob_match_outcome_server_won(self) -> None:
        """if best of 3 and already won 2 then won"""
        assert prob_match_outcome(0.5, 2, 1, 3) == (1.0, {})

    def test_prob_match_outcome_server_lost(self) -> None:
        """if best of 3 and already lost 2 then lost"""
        assert prob_match_outcome(0.5, 1, 2, 3) == (0.0, {})

    def test_prob_match_outcome_server_won_five(self) -> None:
        """if best of 5 and already won 3 then won"""
        assert prob_match_outcome(0.5, 3, 1, 5) == (1.0, {})

    def test_prob_match_outcome_server_lost_five(self) -> None:
        """if best of 5 and already lost 3 then lost"""
        assert prob_match_outcome(0.5, 2, 3, 5) == (0.0, {})

    def test_prob_match_outcome_one_set_left(self) -> None:
        """if only one set left then p_set should equal p_match"""
        p_set = [x / 100 for x in range(0, 101)]
        p_match = [prob_match_outcome(x, 1, 1, 3)[0] for x in p_set]
        assert all([x == y for x, y in zip(p_set, p_match)])


class TestProbMatch:
    """Tests for the `prob_match` function"""

    def test_prob_match_already_won(self) -> None:
        assert prob_match(0.5, 0.5, 2, 1, 0, 0, 0, 0, 3) == 1.0

    def test_prob_match_already_lost(self) -> None:
        assert prob_match(0.5, 0.5, 1, 2, 0, 0, 0, 0, 3) == 0.0

    def test_prob_match_one_set_left(self) -> None:
        p_s = [x / 100 for x in range(1, 100)]
        p_sets = [prob_set(x, x, 0, 0) for x in p_s]
        p_matches = [prob_match(x, x, 1, 1, 0, 0, 0, 0, 3) for x in p_s]
        assert all(x == y for x, y in zip(p_matches, p_sets))

    def test_prob_match_not_started(self) -> None:
        assert prob_match(0.5, 0.5, 1, 1, 0, 0, 0, 0, 3) == 0.5
