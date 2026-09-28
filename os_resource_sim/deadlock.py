from __future__ import annotations

from .models import SimulationResult


Matrix = list[list[int]]


def _validate_matrix(matrix: Matrix, rows: int, cols: int, label: str) -> None:
    if len(matrix) != rows:
        raise ValueError(f"{label} row count does not match")
    for row in matrix:
        if len(row) != cols:
            raise ValueError(f"{label} column count does not match")
        if any(val < 0 for val in row):
            raise ValueError(f"{label} contains negative values")


def bankers_safe_state(available: list[int], maximum: Matrix, allocation: Matrix, process_ids: list[str] | None = None) -> SimulationResult:
    if any(val < 0 for val in available):
        raise ValueError("Available resources cannot be negative")
    rows = len(maximum)
    cols = len(available)
    _validate_matrix(maximum, rows, cols, "Maximum")
    _validate_matrix(allocation, rows, cols, "Allocation")
    if process_ids is None:
        process_ids = [f"P{i}" for i in range(rows)]
    if len(process_ids) != rows or len(set(process_ids)) != rows:
        raise ValueError("Process IDs must be unique and match process count")

    need = []
    for i in range(rows):
        nrow = []
        for j in range(cols):
            if allocation[i][j] > maximum[i][j]:
                raise ValueError("Allocation cannot exceed maximum demand")
            nrow.append(maximum[i][j] - allocation[i][j])
        need.append(nrow)

    work = available[:]
    finish = [False] * rows
    sequence: list[str] = []

    progress = True
    while progress:
        progress = False
        for i in range(rows):
            if finish[i]:
                continue
            if all(need[i][j] <= work[j] for j in range(cols)):
                for j in range(cols):
                    work[j] += allocation[i][j]
                finish[i] = True
                sequence.append(process_ids[i])
                progress = True

    safe = all(finish)
    return SimulationResult(
        module="deadlock",
        algorithm="bankers",
        metrics={"safe": safe, "completed_processes": len(sequence)},
        details={"safe_sequence": sequence, "finish_flags": finish, "need": need, "available_end": work},
    )


def detect_deadlock(available: list[int], allocation: Matrix, request: Matrix, process_ids: list[str] | None = None) -> SimulationResult:
    if any(val < 0 for val in available):
        raise ValueError("Available resources cannot be negative")
    rows = len(allocation)
    cols = len(available)
    _validate_matrix(allocation, rows, cols, "Allocation")
    _validate_matrix(request, rows, cols, "Request")
    if process_ids is None:
        process_ids = [f"P{i}" for i in range(rows)]
    if len(process_ids) != rows or len(set(process_ids)) != rows:
        raise ValueError("Process IDs must be unique and match process count")

    work = available[:]
    finish = [all(v == 0 for v in allocation[i]) for i in range(rows)]
    progressed = True

    while progressed:
        progressed = False
        for i in range(rows):
            if finish[i]:
                continue
            if all(request[i][j] <= work[j] for j in range(cols)):
                for j in range(cols):
                    work[j] += allocation[i][j]
                finish[i] = True
                progressed = True

    deadlocked = [process_ids[i] for i, done in enumerate(finish) if not done]
    return SimulationResult(
        module="deadlock",
        algorithm="detection",
        metrics={"deadlocked": bool(deadlocked), "deadlocked_count": len(deadlocked)},
        details={"deadlocked_processes": deadlocked, "finish_flags": finish, "available_end": work},
    )
