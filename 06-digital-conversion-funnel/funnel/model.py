"""Decision model for the digital-originations funnel."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class FunnelStep:
    step_id: str
    label_en: str
    label_es: str
    count: int
    from_previous: float
    drop_from_previous: int


@dataclass(frozen=True)
class FunnelResult:
    steps: tuple[FunnelStep, ...]
    overall_conversion: float
    bottleneck_index: int
    recovery_pp: float
    additional_final_conversions: int

    @property
    def bottleneck(self) -> FunnelStep:
        return self.steps[self.bottleneck_index]


def analyze(tables: dict[str, list[dict]], recovery_pp: float = 0.05) -> FunnelResult:
    """Count reached steps and quantify a transparent bottleneck scenario.

    ``recovery_pp`` is an absolute improvement in the bottleneck's step
    conversion. It is a planning scenario, never presented as a forecast.
    """
    catalog = sorted(tables["digital_funnel_steps"], key=lambda row: int(row["position"]))
    step_ids = [row["step_id"] for row in catalog]
    position = {step_id: i for i, step_id in enumerate(step_ids)}
    journeys: dict[str, set[str]] = defaultdict(set)

    for event in tables["digital_funnel_events"]:
        step_id = event["step_id"]
        if step_id not in position:
            raise ValueError(f"unknown funnel step: {step_id}")
        journeys[event["journey_id"]].add(step_id)

    for journey_id, reached in journeys.items():
        furthest = max(position[step_id] for step_id in reached)
        expected = set(step_ids[:furthest + 1])
        if reached != expected:
            raise ValueError(f"journey {journey_id} skips or repeats the declared funnel")

    counts = [sum(step_id in reached for reached in journeys.values()) for step_id in step_ids]
    steps = []
    for i, (row, count) in enumerate(zip(catalog, counts, strict=True)):
        previous = counts[i - 1] if i else count
        steps.append(FunnelStep(
            step_id=row["step_id"],
            label_en=row["label_en"],
            label_es=row["label_es"],
            count=count,
            from_previous=count / previous if previous else 0.0,
            drop_from_previous=previous - count if i else 0,
        ))

    bottleneck_index = min(range(1, len(steps)), key=lambda i: steps[i].from_previous)
    previous_count = steps[bottleneck_index - 1].count
    downstream_rate = steps[-1].count / steps[bottleneck_index].count
    additional_at_step = previous_count * recovery_pp
    additional_final = round(additional_at_step * downstream_rate)

    return FunnelResult(
        steps=tuple(steps),
        overall_conversion=steps[-1].count / steps[0].count,
        bottleneck_index=bottleneck_index,
        recovery_pp=recovery_pp,
        additional_final_conversions=additional_final,
    )
