# operating-system

Integrated Python-and-Bash operating-system resource-management simulation capstone project.

## Features

- **Process scheduling**: FCFS, SJF, Round Robin, Priority
- **Memory management**: first-fit, best-fit, worst-fit with allocation/release and fragmentation metrics
- **Deadlock management**: Banker's safety check and deadlock detection simulation
- **Storage management**: FCFS, SSTF, SCAN, C-SCAN
- **Reporting**: normalized result objects and export to JSON / CSV / Markdown
- **Bash integration**: environment checks, demo runs, report generation, and CLI piping
- **Testing**: pytest coverage for normal, invalid, boundary, and error cases

## Repository structure

- `/os_resource_sim`: Python package modules and CLI
- `/tests`: pytest suite
- `/data/samples`: JSON and CSV representative inputs
- `/scripts`: Bash integration scripts
- `/reports/generated`: generated demo/analysis outputs
- `/docs`: technical report and demo evidence guide

## Setup

```bash
python3 --version
python3 -m pip install -e .
python3 -m pip install pytest
# optional charts
python3 -m pip install '.[viz]'
```

## CLI usage

Entry points:

- `python3 -m os_resource_sim ...`
- `os-resource-sim ...` (after install)

### Scheduling

```bash
python3 -m os_resource_sim schedule --algorithm fcfs --input data/samples/scheduling.json
python3 -m os_resource_sim schedule --algorithm rr --quantum 2 --input data/samples/scheduling.csv
```

### Memory

```bash
python3 -m os_resource_sim memory --strategy best_fit --input data/samples/memory.json
```

### Deadlock

```bash
python3 -m os_resource_sim deadlock --mode banker --input data/samples/deadlock_banker.json
python3 -m os_resource_sim deadlock --mode detect --input data/samples/deadlock_detect.json
```

### Storage

```bash
python3 -m os_resource_sim storage --algorithm sstf --input data/samples/storage.json
python3 -m os_resource_sim storage --algorithm scan --direction right --input data/samples/storage.csv --initial-head 53 --disk-size 200
```

### Compare algorithms

```bash
python3 -m os_resource_sim compare --module scheduling --input data/samples/scheduling.json --quantum 2
python3 -m os_resource_sim compare --module storage --input data/samples/storage.json
```

### Validate input

```bash
python3 -m os_resource_sim validate --type scheduling --input data/samples/scheduling.csv
```

### Full demo and analysis

```bash
python3 -m os_resource_sim demo --root . --output-dir reports/generated
python3 -m os_resource_sim analyze --output-dir reports/generated
```

## Input formats

- Scheduling: list of objects/rows with `pid, arrival, burst, priority(optional)`
- Memory: object with `blocks` and `operations` (`alloc` with `size`, `free`)
- Deadlock banker: `available`, `maximum`, `allocation`, optional `process_ids`
- Deadlock detection: `available`, `allocation`, `request`, optional `process_ids`
- Storage: object with `requests`, optional `initial_head`, `disk_size`; or CSV with `request`

The CLI returns nonzero exit codes for invalid input or runtime failures.

## Bash scripts

```bash
./scripts/check_env.sh
./scripts/validate_samples.sh
./scripts/run_demo.sh
./scripts/generate_reports.sh
./scripts/pipeline_demo.sh
```

## Testing

```bash
pytest
```

## Analysis observations from sample workload

- SJF generally lowers waiting/turnaround in the provided process dataset.
- Round Robin improves fairness, but average waiting time depends on quantum.
- SSTF typically reduces head movement in clustered request patterns.

Observations are based on included sample datasets; they are workload-dependent.

## Documentation

- `docs/technical_report.md`
- `docs/demo_evidence_guide.md`

## License

MIT (`/LICENSE`)
