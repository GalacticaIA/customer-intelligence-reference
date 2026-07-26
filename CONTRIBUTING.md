# Contributing

This repository is a **reference implementation**, not a library. Nothing here is
meant to be installed as a dependency — the value is that every claim in it can
be re-run and checked.

That shapes what a useful contribution looks like.

## The most valuable contribution is a refutation

If a case reports a number and you can show the method that produced it is wrong,
that is worth more to us than a feature. Concretely:

- **A leak we missed.** Every case is supposed to be free of information the model
  could not have had at scoring time. If you find one, open an issue with the
  file and the line.
- **A reproducibility failure.** The generator is seeded and the outputs are
  committed, so `uv run generate.py` followed by a case's `run.py` must produce
  byte-for-byte identical files. If it does not on your machine, that is a bug —
  tell us your Python version and platform.
- **An estimator that is being asked to do something it cannot.** Case 05 exists
  because case 02 assumed a save rate; if another case is resting on an
  assumption it has not earned, say so.

## Adding a case

Cases are numbered and each one is expected to **pay a debt the previous one
wrote down** rather than stand alone. Before adding one:

1. It reads the shared data model in `data-model/`. It does not generate its own
   data — cases that invent their own world cannot be compared.
2. It imports its predecessors instead of restating them. If case 02 built a
   feature matrix, use it; a second copy will drift.
3. It ships a `README.md` stating **the decision it serves**, an `outputs/` with
   its charts and write-up, and tests in `tests/`.
4. The answer-key table (`churn_potential_outcomes`) is reachable through exactly
   one module. Do not read it directly.

## Before opening a pull request

```bash
cd data-model && uv run generate.py
uvx pytest tests/ -q
uvx ruff check .
```

Python is managed with [`uv`](https://docs.astral.sh/uv/). Please do not add a
`requirements.txt` or use bare `pip` — the reproducibility claim depends on the
toolchain being pinned.

## What is out of scope

Style-only rewrites of code that passes `ruff`, and dependency bumps without a
reason stated in the pull request.
