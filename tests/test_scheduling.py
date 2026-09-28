from os_resource_sim.models import ProcessSpec
from os_resource_sim.scheduling import run


def _sample():
    return [
        ProcessSpec("P1", 0, 5, 2),
        ProcessSpec("P2", 1, 3, 0),
        ProcessSpec("P3", 2, 1, 1),
    ]


def test_fcfs_basic_metrics():
    result = run("fcfs", _sample()).to_dict()
    assert result["module"] == "scheduling"
    assert result["metrics"]["average_waiting_time"] >= 0
    assert len(result["details"]["processes"]) == 3


def test_rr_invalid_quantum():
    try:
        run("rr", _sample(), quantum=0)
    except ValueError as exc:
        assert "Quantum" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_duplicate_pid_rejected():
    processes = [ProcessSpec("P1", 0, 1, 0), ProcessSpec("P1", 1, 1, 0)]
    try:
        run("sjf", processes)
    except ValueError as exc:
        assert "Duplicate" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
