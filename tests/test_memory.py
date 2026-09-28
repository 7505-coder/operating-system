from os_resource_sim.memory import simulate


def test_memory_allocation_and_free():
    result = simulate(
        "best_fit",
        [100, 200],
        [
            {"action": "alloc", "pid": "P1", "size": 50},
            {"action": "free", "pid": "P1"},
        ],
    ).to_dict()
    assert result["metrics"]["allocation_failures"] == 0
    assert result["metrics"]["free_memory"] == 300


def test_memory_invalid_block_size():
    try:
        simulate("first_fit", [100, -1], [])
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_memory_impossible_allocation_tracked():
    result = simulate("worst_fit", [10], [{"action": "alloc", "pid": "P1", "size": 20}]).to_dict()
    assert result["metrics"]["allocation_failures"] == 1
