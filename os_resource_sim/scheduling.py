from __future__ import annotations

from collections import deque
from dataclasses import asdict
from typing import Callable

from .models import ProcessMetrics, ProcessSpec, SimulationResult


def _validate_processes(processes: list[ProcessSpec]) -> None:
    if not processes:
        raise ValueError("At least one process is required")
    seen: set[str] = set()
    for p in processes:
        if p.pid in seen:
            raise ValueError(f"Duplicate process ID: {p.pid}")
        seen.add(p.pid)
        if p.arrival_time < 0:
            raise ValueError(f"Negative arrival time for {p.pid}")
        if p.burst_time <= 0:
            raise ValueError(f"Burst time must be > 0 for {p.pid}")
        if p.priority < 0:
            raise ValueError(f"Priority must be >= 0 for {p.pid}")


def _build_result(algorithm: str, metrics: list[ProcessMetrics], timeline: list[dict[str, int | str]]) -> SimulationResult:
    avg_wait = sum(m.waiting_time for m in metrics) / len(metrics)
    avg_turn = sum(m.turnaround_time for m in metrics) / len(metrics)
    start = min(m.arrival_time for m in metrics)
    finish = max(m.completion_time for m in metrics)
    window = max(1, finish - start)
    throughput = len(metrics) / window
    return SimulationResult(
        module="scheduling",
        algorithm=algorithm,
        metrics={
            "average_waiting_time": round(avg_wait, 4),
            "average_turnaround_time": round(avg_turn, 4),
            "throughput": round(throughput, 4),
        },
        details={
            "processes": [asdict(m) for m in sorted(metrics, key=lambda item: item.pid)],
            "timeline": timeline,
        },
    )


def fcfs(processes: list[ProcessSpec]) -> SimulationResult:
    _validate_processes(processes)
    current = 0
    metrics: list[ProcessMetrics] = []
    timeline: list[dict[str, int | str]] = []
    for p in sorted(processes, key=lambda proc: (proc.arrival_time, proc.pid)):
        start = max(current, p.arrival_time)
        completion = start + p.burst_time
        timeline.append({"pid": p.pid, "start": start, "end": completion})
        metrics.append(
            ProcessMetrics(
                pid=p.pid,
                arrival_time=p.arrival_time,
                burst_time=p.burst_time,
                priority=p.priority,
                start_time=start,
                completion_time=completion,
                turnaround_time=completion - p.arrival_time,
                waiting_time=start - p.arrival_time,
                response_time=start - p.arrival_time,
            )
        )
        current = completion
    return _build_result("fcfs", metrics, timeline)


def _non_preemptive(processes: list[ProcessSpec], selector: Callable[[list[ProcessSpec]], ProcessSpec], algorithm: str) -> SimulationResult:
    _validate_processes(processes)
    pending = sorted(processes, key=lambda proc: (proc.arrival_time, proc.pid))
    ready: list[ProcessSpec] = []
    current = 0
    idx = 0
    metrics: list[ProcessMetrics] = []
    timeline: list[dict[str, int | str]] = []

    while idx < len(pending) or ready:
        while idx < len(pending) and pending[idx].arrival_time <= current:
            ready.append(pending[idx])
            idx += 1
        if not ready:
            current = pending[idx].arrival_time
            continue
        selected = selector(ready)
        ready.remove(selected)
        start = current
        completion = current + selected.burst_time
        timeline.append({"pid": selected.pid, "start": start, "end": completion})
        metrics.append(
            ProcessMetrics(
                pid=selected.pid,
                arrival_time=selected.arrival_time,
                burst_time=selected.burst_time,
                priority=selected.priority,
                start_time=start,
                completion_time=completion,
                turnaround_time=completion - selected.arrival_time,
                waiting_time=start - selected.arrival_time,
                response_time=start - selected.arrival_time,
            )
        )
        current = completion

    return _build_result(algorithm, metrics, timeline)


def sjf(processes: list[ProcessSpec]) -> SimulationResult:
    return _non_preemptive(
        processes,
        selector=lambda ready: min(ready, key=lambda proc: (proc.burst_time, proc.arrival_time, proc.pid)),
        algorithm="sjf",
    )


def priority(processes: list[ProcessSpec]) -> SimulationResult:
    return _non_preemptive(
        processes,
        selector=lambda ready: min(ready, key=lambda proc: (proc.priority, proc.arrival_time, proc.pid)),
        algorithm="priority",
    )


def round_robin(processes: list[ProcessSpec], quantum: int) -> SimulationResult:
    _validate_processes(processes)
    if quantum <= 0:
        raise ValueError("Quantum must be > 0")

    pending = sorted(processes, key=lambda proc: (proc.arrival_time, proc.pid))
    remaining = {p.pid: p.burst_time for p in pending}
    first_start: dict[str, int] = {}
    completion: dict[str, int] = {}
    ready: deque[ProcessSpec] = deque()
    current = 0
    idx = 0
    timeline: list[dict[str, int | str]] = []

    while idx < len(pending) or ready:
        while idx < len(pending) and pending[idx].arrival_time <= current:
            ready.append(pending[idx])
            idx += 1
        if not ready:
            current = pending[idx].arrival_time
            continue
        proc = ready.popleft()
        if proc.pid not in first_start:
            first_start[proc.pid] = current
        run = min(quantum, remaining[proc.pid])
        start = current
        end = start + run
        timeline.append({"pid": proc.pid, "start": start, "end": end})
        current = end
        remaining[proc.pid] -= run

        while idx < len(pending) and pending[idx].arrival_time <= current:
            ready.append(pending[idx])
            idx += 1

        if remaining[proc.pid] > 0:
            ready.append(proc)
        else:
            completion[proc.pid] = current

    metrics: list[ProcessMetrics] = []
    for p in pending:
        complete = completion[p.pid]
        turnaround = complete - p.arrival_time
        waiting = turnaround - p.burst_time
        start = first_start[p.pid]
        metrics.append(
            ProcessMetrics(
                pid=p.pid,
                arrival_time=p.arrival_time,
                burst_time=p.burst_time,
                priority=p.priority,
                start_time=start,
                completion_time=complete,
                turnaround_time=turnaround,
                waiting_time=waiting,
                response_time=start - p.arrival_time,
            )
        )

    return _build_result("round_robin", metrics, timeline)


def run(algorithm: str, processes: list[ProcessSpec], quantum: int | None = None) -> SimulationResult:
    algorithm = algorithm.lower()
    if algorithm == "fcfs":
        return fcfs(processes)
    if algorithm == "sjf":
        return sjf(processes)
    if algorithm == "priority":
        return priority(processes)
    if algorithm in {"rr", "round_robin"}:
        if quantum is None:
            raise ValueError("Quantum is required for Round Robin")
        return round_robin(processes, quantum)
    raise ValueError(f"Unsupported scheduling algorithm: {algorithm}")
