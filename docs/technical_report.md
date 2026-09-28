# Technical Report

## Design decisions

The project is organized as a Python package with cohesive modules per OS area (scheduling, memory, deadlock, storage, reporting) and an argparse-based CLI entrypoint. Data interchange is normalized through `SimulationResult` objects so downstream reporting/export logic can be reused.

## Implemented algorithms and complexity

- Scheduling: FCFS, SJF (non-preemptive), Priority (non-preemptive), Round Robin.
- Memory: first-fit, best-fit, worst-fit with splitting and coalescing.
- Deadlock: Banker's safety check and matrix-based deadlock detection.
- Storage: FCFS, SSTF, SCAN, C-SCAN.

Typical time complexity (n = process/request count, m = resource types):

- FCFS: O(n log n) due to sorting by arrival
- SJF/Priority non-preemptive: O(n^2) in simple ready-list implementation
- Round Robin: O(k) time slices, bounded by total burst/quantum behavior
- Memory simulation: O(op * blocks)
- Banker's/detection: O(n^2 * m)
- SSTF: O(n^2)

## Assumptions and validation

- IDs must be unique where required.
- Negative and out-of-range values are rejected.
- Round Robin requires quantum > 0.
- Allocation cannot exceed declared maximum in Banker's input.

## Limitations

- Scheduling implementations prioritize clarity and correctness over optimization.
- Memory model uses variable partition simulation with coalescing; internal fragmentation is fixed at 0 in this model.
- Visualization uses matplotlib only when available; otherwise the analysis still produces text/JSON/Markdown outputs.

## Analysis findings

On the provided sample datasets, SJF shows lower average waiting and turnaround than FCFS for the tested process mix, while Round Robin can trade lower response latency for higher waiting depending on quantum. For disk scheduling samples, SSTF often reduces movement compared with FCFS. These findings are dataset-specific and are documented as observations, not universal claims.
