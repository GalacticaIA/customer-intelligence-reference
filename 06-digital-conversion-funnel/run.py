#!/usr/bin/env python3
"""Generate the bilingual digital-originations funnel and its report."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data-model"))

from fintech import Config, generate  # noqa: E402
from funnel import analyze  # noqa: E402
from funnel.charts import render as render_chart  # noqa: E402
from funnel.report import render as render_report  # noqa: E402


def _load(data_dir: Path | None, cfg: Config) -> dict[str, list[dict]]:
    if data_dir is None:
        return generate(cfg)
    tables = {}
    for name in ("digital_funnel_steps", "digital_funnel_events"):
        with (data_dir / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
            tables[name] = list(csv.DictReader(handle))
    return tables


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=Config.n_customers)
    parser.add_argument("--months", type=int, default=Config.n_months)
    parser.add_argument("--seed", type=int, default=Config.seed)
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "outputs")
    args = parser.parse_args()

    cfg = Config(seed=args.seed, n_customers=args.customers, n_months=args.months)
    result = analyze(_load(args.data_dir, cfg))
    args.out.mkdir(parents=True, exist_ok=True)
    written = {
        "report.md": render_report(result),
        "funnel.svg": render_chart(result, "en"),
        "funnel.es.svg": render_chart(result, "es"),
    }
    for name, content in written.items():
        (args.out / name).write_text(content, encoding="utf-8")

    print(f"Overall conversion: {result.overall_conversion:.1%}")
    print(f"Bottleneck: {result.bottleneck.label_en}")
    print(f"Wrote {len(written)} files to {args.out}/")


if __name__ == "__main__":
    main()
