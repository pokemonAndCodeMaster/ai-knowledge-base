"""Pure quota calculation for acceptance assignment previews."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Sequence


@dataclass(frozen=True)
class SamplingBucket:
    id: str
    good_available: int
    bad_available: int


@dataclass(frozen=True)
class SamplingPlan:
    target_count: int
    planned_good: int
    planned_bad: int
    shortage: int
    allocations: dict[str, tuple[int, int]]
    warnings: tuple[str, ...]


def _allocate_proportionally(target: int, capacities: Sequence[tuple[str, int]]) -> dict[str, int]:
    allocations = {key: 0 for key, _ in capacities}
    total_capacity = sum(capacity for _, capacity in capacities)
    if target <= 0 or total_capacity <= 0:
        return allocations

    target = min(target, total_capacity)
    theoretical = [(key, target * capacity / total_capacity, capacity) for key, capacity in capacities]
    for key, value, capacity in theoretical:
        allocations[key] = min(floor(value), capacity)

    remaining = target - sum(allocations.values())
    order = sorted(theoretical, key=lambda item: (-(item[1] - floor(item[1])), item[0]))
    while remaining:
        progressed = False
        for key, _, capacity in order:
            if allocations[key] >= capacity:
                continue
            allocations[key] += 1
            remaining -= 1
            progressed = True
            if remaining == 0:
                break
        if not progressed:
            break
    return allocations


def plan_ratio_sampling(buckets: Sequence[SamplingBucket], requested_target: int | None, good_ratio: float) -> SamplingPlan:
    total_good = sum(bucket.good_available for bucket in buckets)
    total_bad = sum(bucket.bad_available for bucket in buckets)
    total_available = total_good + total_bad
    target = min(requested_target or total_available, total_available)
    shortage = max((requested_target or total_available) - total_available, 0)
    desired_good = round(target * good_ratio)
    planned_good = min(desired_good, total_good)
    planned_bad = min(target - planned_good, total_bad)

    remaining = target - planned_good - planned_bad
    if remaining:
        extra_good = min(remaining, total_good - planned_good)
        planned_good += extra_good
        remaining -= extra_good
    if remaining:
        planned_bad += min(remaining, total_bad - planned_bad)

    warnings: list[str] = []
    if shortage:
        warnings.append(f"可用量不足，目标缺口 {shortage}")
    if planned_good != desired_good:
        warnings.append("Good 可用量不足，已由 Bad 可用量补足")
    desired_bad = target - desired_good
    if planned_bad != desired_bad and planned_good > desired_good:
        warnings.append("Bad 可用量不足，已由 Good 可用量补足")

    good_allocations = _allocate_proportionally(
        planned_good,
        [(bucket.id, bucket.good_available) for bucket in buckets],
    )
    bad_allocations = _allocate_proportionally(
        planned_bad,
        [(bucket.id, bucket.bad_available) for bucket in buckets],
    )
    return SamplingPlan(
        target_count=target,
        planned_good=planned_good,
        planned_bad=planned_bad,
        shortage=shortage,
        allocations={bucket.id: (good_allocations[bucket.id], bad_allocations[bucket.id]) for bucket in buckets},
        warnings=tuple(warnings),
    )
