from os_resource_sim.storage import run


def test_storage_algorithms_run():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    for algo in ["fcfs", "sstf", "scan", "cscan"]:
        result = run(algo, requests, 53, 200).to_dict()
        assert result["metrics"]["total_head_movement"] >= 0


def test_storage_invalid_request():
    try:
        run("fcfs", [500], 50, 200)
    except ValueError as exc:
        assert "range" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
