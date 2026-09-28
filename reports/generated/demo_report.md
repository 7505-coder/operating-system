# OS Resource Management Demo

## Metrics

- **scenarios**: 4

## Details

```json
{
  "scheduling": {
    "module": "scheduling",
    "algorithm": "sjf",
    "metrics": {
      "average_waiting_time": 7.75,
      "average_turnaround_time": 14.25,
      "throughput": 0.1538
    },
    "details": {
      "processes": [
        {
          "pid": "P1",
          "arrival_time": 0,
          "burst_time": 8,
          "priority": 2,
          "start_time": 0,
          "completion_time": 8,
          "turnaround_time": 8,
          "waiting_time": 0,
          "response_time": 0
        },
        {
          "pid": "P2",
          "arrival_time": 1,
          "burst_time": 4,
          "priority": 1,
          "start_time": 8,
          "completion_time": 12,
          "turnaround_time": 11,
          "waiting_time": 7,
          "response_time": 7
        },
        {
          "pid": "P3",
          "arrival_time": 2,
          "burst_time": 9,
          "priority": 3,
          "start_time": 17,
          "completion_time": 26,
          "turnaround_time": 24,
          "waiting_time": 15,
          "response_time": 15
        },
        {
          "pid": "P4",
          "arrival_time": 3,
          "burst_time": 5,
          "priority": 0,
          "start_time": 12,
          "completion_time": 17,
          "turnaround_time": 14,
          "waiting_time": 9,
          "response_time": 9
        }
      ],
      "timeline": [
        {
          "pid": "P1",
          "start": 0,
          "end": 8
        },
        {
          "pid": "P2",
          "start": 8,
          "end": 12
        },
        {
          "pid": "P4",
          "start": 12,
          "end": 17
        },
        {
          "pid": "P3",
          "start": 17,
          "end": 26
        }
      ]
    }
  },
  "memory": {
    "module": "memory",
    "algorithm": "best_fit",
    "metrics": {
      "total_memory": 1700,
      "used_memory": 750,
      "free_memory": 950,
      "allocation_failures": 0,
      "internal_fragmentation": 0,
      "external_fragmentation": 262
    },
    "details": {
      "blocks": [
        {
          "size": 426,
          "pid": "P4",
          "free": false
        },
        {
          "size": 174,
          "pid": null,
          "free": true
        },
        {
          "size": 112,
          "pid": "P3",
          "free": false
        },
        {
          "size": 88,
          "pid": null,
          "free": true
        },
        {
          "size": 212,
          "pid": "P1",
          "free": false
        },
        {
          "size": 688,
          "pid": null,
          "free": true
        }
      ],
      "operations": [
        {
          "action": "alloc",
          "pid": "P1",
          "size": 212,
          "success": true
        },
        {
          "action": "alloc",
          "pid": "P2",
          "size": 417,
          "success": true
        },
        {
          "action": "alloc",
          "pid": "P3",
          "size": 112,
          "success": true
        },
        {
          "action": "free",
          "pid": "P2",
          "success": true
        },
        {
          "action": "alloc",
          "pid": "P4",
          "size": 426,
          "success": true
        }
      ]
    }
  },
  "deadlock": {
    "module": "deadlock",
    "algorithm": "bankers",
    "metrics": {
      "safe": true,
      "completed_processes": 5
    },
    "details": {
      "safe_sequence": [
        "P1",
        "P3",
        "P4",
        "P0",
        "P2"
      ],
      "finish_flags": [
        true,
        true,
        true,
        true,
        true
      ],
      "need": [
        [
          7,
          4,
          3
        ],
        [
          1,
          2,
          2
        ],
        [
          6,
          0,
          0
        ],
        [
          0,
          1,
          1
        ],
        [
          4,
          3,
          1
        ]
      ],
      "available_end": [
        10,
        5,
        7
      ]
    }
  },
  "storage": {
    "module": "storage",
    "algorithm": "sstf",
    "metrics": {
      "total_head_movement": 236
    },
    "details": {
      "service_order": [
        65,
        67,
        37,
        14,
        98,
        122,
        124,
        183
      ]
    }
  }
}
```
