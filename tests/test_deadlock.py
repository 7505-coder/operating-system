from os_resource_sim.deadlock import bankers_safe_state, detect_deadlock


def test_bankers_safe_case():
    result = bankers_safe_state(
        [3, 3, 2],
        [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
        ["P0", "P1", "P2", "P3", "P4"],
    ).to_dict()
    assert result["metrics"]["safe"] is True


def test_deadlock_detect_case():
    result = detect_deadlock(
        [0, 0, 0],
        [[0, 1, 0], [2, 0, 0], [3, 0, 3]],
        [[0, 0, 0], [2, 0, 2], [0, 0, 1]],
        ["P0", "P1", "P2"],
    ).to_dict()
    assert result["metrics"]["deadlocked"] is True


def test_invalid_negative_available():
    try:
        detect_deadlock([-1], [[0]], [[0]], ["P0"])
    except ValueError as exc:
        assert "negative" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
