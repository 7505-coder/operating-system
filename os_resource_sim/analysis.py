from __future__ import annotations

from pathlib import Path

from .models import ProcessSpec
from .reporting import export_json, export_markdown
from .scheduling import run as schedule_run


def run_analysis(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    processes = [
        ProcessSpec("P1", 0, 7, 2),
        ProcessSpec("P2", 1, 5, 1),
        ProcessSpec("P3", 2, 3, 3),
        ProcessSpec("P4", 3, 1, 0),
    ]
    results = {
        "fcfs": schedule_run("fcfs", processes).to_dict(),
        "sjf": schedule_run("sjf", processes).to_dict(),
        "priority": schedule_run("priority", processes).to_dict(),
        "round_robin": schedule_run("rr", processes, quantum=2).to_dict(),
    }
    summary_rows = []
    for name, result in results.items():
        summary_rows.append(
            {
                "algorithm": name,
                "average_waiting_time": result["metrics"]["average_waiting_time"],
                "average_turnaround_time": result["metrics"]["average_turnaround_time"],
                "throughput": result["metrics"]["throughput"],
            }
        )

    chart_path = output_dir / "scheduling_waiting_time.png"
    chart_generated = False
    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(7, 4))
        plt.bar([row["algorithm"] for row in summary_rows], [row["average_waiting_time"] for row in summary_rows])
        plt.ylabel("Average Waiting Time")
        plt.title("Scheduling Comparison")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        chart_generated = True
    except Exception:
        chart_generated = False

    payload = {
        "summary": summary_rows,
        "chart_generated": chart_generated,
        "chart_path": str(chart_path) if chart_generated else None,
        "notes": [
            "SJF tends to reduce waiting time for this workload.",
            "Round Robin improves fairness but can increase average waiting time depending on quantum.",
        ],
    }
    export_json(payload, output_dir / "analysis_summary.json")
    export_markdown("Scheduling Analysis", {"metrics": {"chart_generated": chart_generated}, "details": payload}, output_dir / "analysis_summary.md")
    return payload
