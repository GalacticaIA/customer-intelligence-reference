# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **The data model** (`data-model/`) — a seeded generator emitting 15 related
  tables with an explicit causal structure. Churn labels at two observation
  cutoffs, the contact policy as a table rather than a constant, and a fenced-off
  answer key holding each customer's outcome had the campaign never run.
- **Case 02 · Churn without leakage** — out-of-time split, calibration,
  explainable drivers, prioritisation by expected value. Reruns the same model two
  dishonest ways (random split; one feature derived from the label) to show what
  each shortcut would have reported.
- **Case 03 · Governed next-best-offer** — the offer decision subject to consent,
  eligibility, exclusions and a contact policy. Reports the cost of each
  individual gate, and the cost of applying the same gates in the wrong order.
- **Case 05 · Campaign incrementality** — true uplift against the held-back
  control, read four ways, against the answer key. Settles the save rate case 02
  had to assume, and shows the experiment as designed cannot distinguish it from
  zero.
- CI on every push: lint, dataset generation, and the test suite. The dataset is
  generated *before* the suite runs — if the generator drifts, every case
  downstream is reading a different world than its write-up describes.

### Planned

- Case 01 · Actionable segmentation
- Case 04 · ARPU / value decomposition
