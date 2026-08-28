from __future__ import annotations

from .model import FunnelResult


def render(result: FunnelResult) -> str:
    lines = [
        "# Digital-originations conversion funnel",
        "",
        "> Synthetic, deterministic data. This is a reproducible analytical artifact, not a client result.",
        "",
        "| Step | Reached | From previous | Lost at transition |",
        "|---|---:|---:|---:|",
    ]
    for step in result.steps:
        rate = "—" if step is result.steps[0] else f"{step.from_previous:.1%}"
        lost = "—" if step is result.steps[0] else f"{step.drop_from_previous:,}"
        lines.append(f"| {step.label_en} | {step.count:,} | {rate} | {lost} |")
    lines += [
        "",
        f"Overall conversion: **{result.overall_conversion:.1%}**.",
        "",
        f"The largest transition loss occurs before **{result.bottleneck.label_en}**. "
        f"A sensitivity scenario that improves that transition by {result.recovery_pp:.0%} absolute "
        f"yields approximately **{result.additional_final_conversions:,} additional first transactions**, "
        "holding every downstream rate constant.",
        "",
        "That last number is a transparent what-if, not a forecast: it answers which step deserves "
        "an experiment before anyone assigns revenue to it.",
        "",
    ]
    return "\n".join(lines)
