from __future__ import annotations

from dataclasses import dataclass

from .models import SimulationResult


@dataclass
class Block:
    size: int
    pid: str | None = None

    @property
    def free(self) -> bool:
        return self.pid is None


def _validate_blocks(blocks: list[int]) -> None:
    if not blocks:
        raise ValueError("At least one memory block is required")
    if any(size <= 0 for size in blocks):
        raise ValueError("Memory block sizes must be positive")


def _select_index(strategy: str, free_blocks: list[tuple[int, Block]], req_size: int) -> int:
    if strategy == "first_fit":
        return free_blocks[0][0]
    if strategy == "best_fit":
        return min(free_blocks, key=lambda item: item[1].size)[0]
    if strategy == "worst_fit":
        return max(free_blocks, key=lambda item: item[1].size)[0]
    raise ValueError(f"Unsupported memory strategy: {strategy}")


def simulate(strategy: str, blocks: list[int], operations: list[dict[str, str | int]]) -> SimulationResult:
    _validate_blocks(blocks)
    strategy = strategy.lower().replace("-", "_")
    if strategy not in {"first_fit", "best_fit", "worst_fit"}:
        raise ValueError(f"Unsupported memory strategy: {strategy}")

    state = [Block(size=size) for size in blocks]
    owned: set[str] = set()
    failures = 0
    log: list[dict[str, str | int | bool]] = []

    for op in operations:
        action = str(op.get("action", "")).lower()
        pid = str(op.get("pid", "")).strip()
        if not pid:
            raise ValueError("Operation pid is required")
        if action == "alloc":
            size = int(op.get("size", 0))
            if size <= 0:
                raise ValueError(f"Allocation size must be positive for {pid}")
            if pid in owned:
                raise ValueError(f"Process {pid} already has allocated memory")
            free_blocks = [(i, block) for i, block in enumerate(state) if block.free and block.size >= size]
            if not free_blocks:
                failures += 1
                log.append({"action": "alloc", "pid": pid, "size": size, "success": False})
                continue
            index = _select_index(strategy, free_blocks, size)
            selected = state[index]
            remainder = selected.size - size
            state[index] = Block(size=size, pid=pid)
            if remainder > 0:
                state.insert(index + 1, Block(size=remainder))
            owned.add(pid)
            log.append({"action": "alloc", "pid": pid, "size": size, "success": True})
        elif action == "free":
            released = False
            for block in state:
                if block.pid == pid:
                    block.pid = None
                    released = True
            if released:
                owned.discard(pid)
                merged: list[Block] = []
                for block in state:
                    if merged and merged[-1].free and block.free:
                        merged[-1].size += block.size
                    else:
                        merged.append(block)
                state = merged
            log.append({"action": "free", "pid": pid, "success": released})
        else:
            raise ValueError(f"Unsupported operation action: {action}")

    free_sizes = [block.size for block in state if block.free]
    total_free = sum(free_sizes)
    largest_free = max(free_sizes) if free_sizes else 0

    return SimulationResult(
        module="memory",
        algorithm=strategy,
        metrics={
            "total_memory": sum(blocks),
            "used_memory": sum(block.size for block in state if not block.free),
            "free_memory": total_free,
            "allocation_failures": failures,
            "internal_fragmentation": 0,
            "external_fragmentation": total_free - largest_free,
        },
        details={
            "blocks": [{"size": block.size, "pid": block.pid, "free": block.free} for block in state],
            "operations": log,
        },
    )
