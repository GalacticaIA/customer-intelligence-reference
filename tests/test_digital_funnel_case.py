from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "data-model"))
sys.path.insert(0, str(_ROOT / "06-digital-conversion-funnel"))

from fintech import Config, generate  # noqa: E402
from funnel import analyze  # noqa: E402
from funnel.charts import render  # noqa: E402


def test_funnel_counts_are_monotone_and_bottleneck_is_observed():
    result = analyze(generate(Config(seed=42, n_customers=800, n_months=18)))
    counts = [step.count for step in result.steps]
    assert all(left >= right > 0 for left, right in zip(counts, counts[1:], strict=False))
    assert result.bottleneck_index > 0
    assert result.bottleneck.from_previous == min(step.from_previous for step in result.steps[1:])
    assert result.additional_final_conversions > 0


def test_bilingual_figures_come_from_the_same_result():
    result = analyze(generate(Config(seed=42, n_customers=200, n_months=18)))
    english = render(result, "en")
    spanish = render(result, "es")
    assert "Synthetic data" in english
    assert "Datos sintéticos" in spanish
    for step in result.steps:
        assert f"{step.count:,}" in english
        assert f"{step.count:,}" in spanish


def test_unknown_step_fails_instead_of_disappearing():
    tables = generate(Config(seed=42, n_customers=50, n_months=18))
    tables["digital_funnel_events"][0]["step_id"] = "renamed_without_catalog"
    try:
        analyze(tables)
    except ValueError as error:
        assert "unknown funnel step" in str(error)
    else:
        raise AssertionError("an unknown step must fail loudly")
