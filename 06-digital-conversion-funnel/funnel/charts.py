"""Deterministic bilingual SVG for the digital conversion funnel."""

from __future__ import annotations

from .model import FunnelResult

W, H = 760, 470
PETROL = "#0F4C5C"
PETROL_2 = "#13657A"
PETROL_LT = "#9FD3DF"
INK = "#172126"
MUTED = "#5D6B72"
LINE = "#D8DFE2"
PAPER = "#F7F8F6"


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _text(x: float, y: float, value: str, *, anchor: str = "start", size: int = 12,
          fill: str = INK, weight: int = 400) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" font-family="ui-sans-serif,system-ui,sans-serif" '
        f'fill="{fill}">{_escape(value)}</text>'
    )


def render(result: FunnelResult, locale: str) -> str:
    es = locale == "es"
    title = "Originación digital: dónde se pierde la conversión" if es else \
        "Digital origination: where conversion is lost"
    subtitle = "Datos sintéticos · una misma cohorte" if es else "Synthetic data · one cohort"
    body = [
        f'<rect width="{W}" height="{H}" rx="2" fill="{PAPER}"/>',
        _text(28, 34, title, size=18, weight=700),
        _text(28, 56, subtitle, size=11, fill=MUTED),
    ]

    max_count = result.steps[0].count
    chart_left, chart_right = 232, 724
    top, row_gap, bar_height = 88, 53, 29
    for i, step in enumerate(result.steps):
        y = top + i * row_gap
        width = (chart_right - chart_left) * step.count / max_count
        label = step.label_es if es else step.label_en
        fill = PETROL_2 if i == result.bottleneck_index else PETROL
        opacity = 1.0 if i == result.bottleneck_index else 0.82
        body.append(_text(28, y + 20, label, size=12, weight=600 if i == result.bottleneck_index else 400))
        body.append(
            f'<rect x="{chart_left}" y="{y}" width="{width:.1f}" height="{bar_height}" '
            f'rx="2" fill="{fill}" fill-opacity="{opacity}"/>'
        )
        body.append(_text(chart_left + 12, y + 20, f"{step.count:,}", size=11, fill="#FFFFFF", weight=700))
        if i:
            drop = 1 - step.from_previous
            body.append(_text(chart_right, y + 20,
                              f"{step.from_previous:.0%}  ·  −{drop:.0%}",
                              anchor="end", size=11,
                              fill=PETROL if i == result.bottleneck_index else MUTED,
                              weight=700 if i == result.bottleneck_index else 400))
            connector_y = y - (row_gap - bar_height) / 2
            body.append(f'<line x1="{chart_left}" y1="{connector_y:.1f}" x2="{chart_right}" '
                        f'y2="{connector_y:.1f}" stroke="{LINE}" stroke-width="1"/>')

    note_y = 416
    body.append(f'<rect x="28" y="{note_y - 23}" width="704" height="52" rx="2" '
                f'fill="{PETROL_LT}" fill-opacity="0.24"/>')
    bottleneck_label = result.bottleneck.label_es if es else result.bottleneck.label_en
    if es:
        note = (f"Mayor fuga: {bottleneck_label}. Escenario: +{result.recovery_pp:.0%} en ese paso "
                f"≈ {result.additional_final_conversions:,} primeras transacciones adicionales.")
        disclosure = "Escenario de sensibilidad, no proyección de cliente."
    else:
        note = (f"Largest loss: {bottleneck_label}. Scenario: +{result.recovery_pp:.0%} at that step "
                f"≈ {result.additional_final_conversions:,} additional first transactions.")
        disclosure = "Sensitivity scenario, not a client forecast."
    body.append(_text(44, note_y, note, size=12, fill=PETROL, weight=700))
    body.append(_text(44, note_y + 18, disclosure, size=10, fill=MUTED))

    accessible = title + ". " + note
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{_escape(accessible)}">\n  '
        + "\n  ".join(body)
        + "\n</svg>\n"
    )
