from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProcessSpec:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0


@dataclass
class ProcessMetrics:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    start_time: int
    completion_time: int
    turnaround_time: int
    waiting_time: int
    response_time: int


@dataclass
class SimulationResult:
    module: str
    algorithm: str
    metrics: dict[str, Any]
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
