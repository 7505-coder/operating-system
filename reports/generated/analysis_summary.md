# Scheduling Analysis

## Metrics

- **chart_generated**: False

## Details

```json
{
  "summary": [
    {
      "algorithm": "fcfs",
      "average_waiting_time": 7.0,
      "average_turnaround_time": 11.0,
      "throughput": 0.25
    },
    {
      "algorithm": "sjf",
      "average_waiting_time": 5.0,
      "average_turnaround_time": 9.0,
      "throughput": 0.25
    },
    {
      "algorithm": "priority",
      "average_waiting_time": 5.5,
      "average_turnaround_time": 9.5,
      "throughput": 0.25
    },
    {
      "algorithm": "round_robin",
      "average_waiting_time": 7.5,
      "average_turnaround_time": 11.5,
      "throughput": 0.25
    }
  ],
  "chart_generated": false,
  "chart_path": null,
  "notes": [
    "SJF tends to reduce waiting time for this workload.",
    "Round Robin improves fairness but can increase average waiting time depending on quantum."
  ]
}
```
