from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from .analysis import run_analysis
from .deadlock import bankers_safe_state, detect_deadlock
from .io_utils import load_json_or_csv
from .memory import simulate as simulate_memory
from .models import ProcessSpec
from .reporting import export_csv, export_json, export_markdown
from .scheduling import run as run_scheduling
from .storage import run as run_storage

logger = logging.getLogger("os_resource_sim")


def _as_processes(raw: Any) -> list[ProcessSpec]:
    if not isinstance(raw, list):
        raise ValueError("Scheduling input must be a list")
    processes: list[ProcessSpec] = []
    for row in raw:
        processes.append(
            ProcessSpec(
                pid=str(row["pid"]),
                arrival_time=int(row["arrival"] if "arrival" in row else row["arrival_time"]),
                burst_time=int(row["burst"] if "burst" in row else row["burst_time"]),
                priority=int(row.get("priority", 0)),
            )
        )
    return processes


def _print_result(result: dict[str, Any]) -> None:
    print(json.dumps(result, indent=2))


def _export_payload(payload: dict[str, Any], export: str | None) -> None:
    if not export:
        return
    path = Path(export)
    suffix = path.suffix.lower()
    if suffix == ".json":
        export_json(payload, path)
    elif suffix == ".md":
        export_markdown("Simulation Result", payload, path)
    elif suffix == ".csv":
        rows = payload.get("details", {}).get("processes") or payload.get("details", {}).get("service_order")
        if isinstance(rows, list) and rows and isinstance(rows[0], dict):
            export_csv(rows, path)
        elif isinstance(rows, list):
            export_csv([{"index": idx, "value": value} for idx, value in enumerate(rows)], path)
        else:
            export_csv([payload.get("metrics", {})], path)
    else:
        raise ValueError("Export path must use .json, .csv, or .md")


def cmd_schedule(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    processes = _as_processes(data)
    result = run_scheduling(args.algorithm, processes, args.quantum).to_dict()
    _print_result(result)
    _export_payload(result, args.export)
    return 0


def cmd_memory(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    blocks = [int(x) for x in data["blocks"]]
    operations = list(data["operations"])
    result = simulate_memory(args.strategy, blocks, operations).to_dict()
    _print_result(result)
    _export_payload(result, args.export)
    return 0


def cmd_deadlock(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    pids = data.get("process_ids")
    if args.mode == "banker":
        result = bankers_safe_state(data["available"], data["maximum"], data["allocation"], pids).to_dict()
    else:
        result = detect_deadlock(data["available"], data["allocation"], data["request"], pids).to_dict()
    _print_result(result)
    _export_payload(result, args.export)
    return 0


def cmd_storage(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    if isinstance(data, list):
        requests = [int(row["request"]) for row in data]
        head = int(args.initial_head)
        disk_size = int(args.disk_size)
    else:
        requests = [int(x) for x in data["requests"]]
        head = int(data.get("initial_head", args.initial_head))
        disk_size = int(data.get("disk_size", args.disk_size))
    result = run_storage(args.algorithm, requests, head, disk_size, args.direction).to_dict()
    _print_result(result)
    _export_payload(result, args.export)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    output: dict[str, Any] = {}
    if args.module == "scheduling":
        processes = _as_processes(data)
        for algo in ["fcfs", "sjf", "priority", "rr"]:
            output[algo] = run_scheduling(algo, processes, quantum=args.quantum or 2).to_dict()["metrics"]
    else:
        if isinstance(data, list):
            requests = [int(row["request"]) for row in data]
            head = int(args.initial_head)
            disk_size = int(args.disk_size)
        else:
            requests = [int(x) for x in data["requests"]]
            head = int(data.get("initial_head", args.initial_head))
            disk_size = int(data.get("disk_size", args.disk_size))
        for algo in ["fcfs", "sstf", "scan", "cscan"]:
            output[algo] = run_storage(algo, requests, head, disk_size, args.direction).to_dict()["metrics"]

    print(json.dumps(output, indent=2))
    if args.export:
        _export_payload({"module": args.module, "metrics": output, "details": {}}, args.export)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    data = load_json_or_csv(args.input)
    if args.type == "scheduling":
        _ = _as_processes(data)
    elif args.type == "memory":
        if "blocks" not in data or "operations" not in data:
            raise ValueError("Memory input must contain blocks and operations")
    elif args.type == "deadlock":
        if "available" not in data or "allocation" not in data:
            raise ValueError("Deadlock input missing required fields")
    elif args.type == "storage":
        if not isinstance(data, list) and "requests" not in data:
            raise ValueError("Storage input must provide requests")
    print(f"VALID: {args.input}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    schedule_data = load_json_or_csv(str(root / "data/samples/scheduling.json"))
    schedule = run_scheduling("sjf", _as_processes(schedule_data)).to_dict()

    memory_data = load_json_or_csv(str(root / "data/samples/memory.json"))
    memory = simulate_memory("best_fit", [int(x) for x in memory_data["blocks"]], list(memory_data["operations"])).to_dict()

    deadlock_data = load_json_or_csv(str(root / "data/samples/deadlock_banker.json"))
    deadlock = bankers_safe_state(
        deadlock_data["available"], deadlock_data["maximum"], deadlock_data["allocation"], deadlock_data.get("process_ids")
    ).to_dict()

    storage_data = load_json_or_csv(str(root / "data/samples/storage.json"))
    storage = run_storage(
        "sstf",
        [int(x) for x in storage_data["requests"]],
        int(storage_data["initial_head"]),
        int(storage_data["disk_size"]),
        "right",
    ).to_dict()

    payload = {"scheduling": schedule, "memory": memory, "deadlock": deadlock, "storage": storage}
    export_json(payload, outdir / "demo_report.json")
    export_markdown("OS Resource Management Demo", {"metrics": {"scenarios": 4}, "details": payload}, outdir / "demo_report.md")
    print(json.dumps(payload, indent=2))
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    payload = run_analysis(Path(args.output_dir).resolve())
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OS resource-management simulation")
    parser.add_argument("--log-level", default="WARNING", help="Logging level")
    sub = parser.add_subparsers(dest="command", required=True)

    schedule = sub.add_parser("schedule", help="Run process scheduling simulation")
    schedule.add_argument("--algorithm", required=True, choices=["fcfs", "sjf", "priority", "rr", "round_robin"])
    schedule.add_argument("--input", required=True, help="JSON/CSV input path or - for stdin")
    schedule.add_argument("--quantum", type=int)
    schedule.add_argument("--export")
    schedule.set_defaults(func=cmd_schedule)

    memory = sub.add_parser("memory", help="Run memory management simulation")
    memory.add_argument("--strategy", required=True, choices=["first_fit", "best_fit", "worst_fit", "first-fit", "best-fit", "worst-fit"])
    memory.add_argument("--input", required=True)
    memory.add_argument("--export")
    memory.set_defaults(func=cmd_memory)

    deadlock = sub.add_parser("deadlock", help="Run deadlock simulation")
    deadlock.add_argument("--mode", required=True, choices=["banker", "detect"])
    deadlock.add_argument("--input", required=True)
    deadlock.add_argument("--export")
    deadlock.set_defaults(func=cmd_deadlock)

    storage = sub.add_parser("storage", help="Run disk scheduling simulation")
    storage.add_argument("--algorithm", required=True, choices=["fcfs", "sstf", "scan", "cscan", "c-scan"])
    storage.add_argument("--input", required=True)
    storage.add_argument("--initial-head", type=int, default=50)
    storage.add_argument("--disk-size", type=int, default=200)
    storage.add_argument("--direction", choices=["left", "right"], default="right")
    storage.add_argument("--export")
    storage.set_defaults(func=cmd_storage)

    compare = sub.add_parser("compare", help="Compare algorithms")
    compare.add_argument("--module", required=True, choices=["scheduling", "storage"])
    compare.add_argument("--input", required=True)
    compare.add_argument("--initial-head", type=int, default=50)
    compare.add_argument("--disk-size", type=int, default=200)
    compare.add_argument("--direction", choices=["left", "right"], default="right")
    compare.add_argument("--quantum", type=int)
    compare.add_argument("--export")
    compare.set_defaults(func=cmd_compare)

    validate = sub.add_parser("validate", help="Validate sample input")
    validate.add_argument("--type", required=True, choices=["scheduling", "memory", "deadlock", "storage"])
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=cmd_validate)

    demo = sub.add_parser("demo", help="Run full demo")
    demo.add_argument("--root", default=".")
    demo.add_argument("--output-dir", default="reports/generated")
    demo.set_defaults(func=cmd_demo)

    analyze = sub.add_parser("analyze", help="Run reproducible analysis")
    analyze.add_argument("--output-dir", default="reports/generated")
    analyze.set_defaults(func=cmd_analyze)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, str(args.log_level).upper(), logging.WARNING))
    try:
        return int(args.func(args))
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"ERROR: {exc}")
        return 2
    except FileNotFoundError as exc:
        logger.error("File error: %s", exc)
        print(f"ERROR: {exc}")
        return 2
    except Exception as exc:  # pragma: no cover
        logger.exception("Unexpected failure")
        print(f"ERROR: unexpected failure: {exc}")
        return 1
