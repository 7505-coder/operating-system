from __future__ import annotations

from .models import SimulationResult


def _validate(requests: list[int], initial_head: int, disk_size: int) -> None:
    if disk_size <= 0:
        raise ValueError("disk_size must be positive")
    if initial_head < 0 or initial_head >= disk_size:
        raise ValueError("initial_head out of range")
    if not requests:
        raise ValueError("At least one request is required")
    if any(r < 0 or r >= disk_size for r in requests):
        raise ValueError("Request out of range")


def _movement(head: int, order: list[int]) -> int:
    total = 0
    current = head
    for req in order:
        total += abs(req - current)
        current = req
    return total


def fcfs(requests: list[int], initial_head: int, disk_size: int) -> SimulationResult:
    _validate(requests, initial_head, disk_size)
    return SimulationResult(
        module="storage",
        algorithm="fcfs",
        metrics={"total_head_movement": _movement(initial_head, requests)},
        details={"service_order": requests},
    )


def sstf(requests: list[int], initial_head: int, disk_size: int) -> SimulationResult:
    _validate(requests, initial_head, disk_size)
    pending = requests[:]
    current = initial_head
    order: list[int] = []
    while pending:
        next_req = min(pending, key=lambda req: (abs(req - current), req))
        pending.remove(next_req)
        order.append(next_req)
        current = next_req
    return SimulationResult(
        module="storage",
        algorithm="sstf",
        metrics={"total_head_movement": _movement(initial_head, order)},
        details={"service_order": order},
    )


def scan(requests: list[int], initial_head: int, disk_size: int, direction: str = "right") -> SimulationResult:
    _validate(requests, initial_head, disk_size)
    direction = direction.lower()
    left = sorted([r for r in requests if r < initial_head], reverse=True)
    right = sorted([r for r in requests if r >= initial_head])
    order = right + left if direction == "right" else left + right
    movement_order = order[:]
    if direction == "right" and left:
        movement_order = right + [disk_size - 1] + left
    elif direction == "left" and right:
        movement_order = left + [0] + right
    return SimulationResult(
        module="storage",
        algorithm="scan",
        metrics={"total_head_movement": _movement(initial_head, movement_order)},
        details={"service_order": order, "direction": direction},
    )


def cscan(requests: list[int], initial_head: int, disk_size: int, direction: str = "right") -> SimulationResult:
    _validate(requests, initial_head, disk_size)
    direction = direction.lower()
    left = sorted([r for r in requests if r < initial_head])
    right = sorted([r for r in requests if r >= initial_head])

    if direction == "right":
        order = right + left
        movement_order = right
        if left:
            movement_order = right + [disk_size - 1, 0] + left
    else:
        order = list(reversed(left)) + list(reversed(right))
        movement_order = list(reversed(left))
        if right:
            movement_order = list(reversed(left)) + [0, disk_size - 1] + list(reversed(right))

    return SimulationResult(
        module="storage",
        algorithm="cscan",
        metrics={"total_head_movement": _movement(initial_head, movement_order)},
        details={"service_order": order, "direction": direction},
    )


def run(algorithm: str, requests: list[int], initial_head: int, disk_size: int, direction: str = "right") -> SimulationResult:
    algorithm = algorithm.lower()
    if algorithm == "fcfs":
        return fcfs(requests, initial_head, disk_size)
    if algorithm == "sstf":
        return sstf(requests, initial_head, disk_size)
    if algorithm == "scan":
        return scan(requests, initial_head, disk_size, direction)
    if algorithm in {"cscan", "c-scan"}:
        return cscan(requests, initial_head, disk_size, direction)
    raise ValueError(f"Unsupported disk scheduling algorithm: {algorithm}")
