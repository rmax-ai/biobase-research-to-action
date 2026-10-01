# biobase-research-to-action

Biobase **Research-to-Action** POC: a natural-language biomedical research intent must
become a **correct, authorized, reproducible, and actionable transaction** across
heterogeneous/federated clinical data.

> **Status: bootstrap.** This repository currently contains only the initial skeleton
> (README, MIT license, Python + TypeScript scaffolding). The canonical product/system
> spec, synthetic-data plan, eval plan, and epic/task hierarchy land before any
> implementation.

## POC invariant

A natural-language biomedical research intent must become a correct, authorized,
reproducible, and actionable transaction across heterogeneous/federated clinical data.

## Canonical scenario (working proposal)

Find 200 metastatic NSCLC patients with KRAS G12C, pretreatment H&E, NGS, treatment
history, and >=12 months of outcomes for commercial AI model development; determine
feasibility, governance, provenance, supplier mix, and mock procurement.

## Layout

| Path | Purpose |
| --- | --- |
| `src/biobase_research_to_action/` | Python package (uv-managed, src layout) |
| `tests/` | Python test suite (pytest) |
| `ts/` | TypeScript workspace (placeholder) |

## Development

Python 3.12+ with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev
uv run pytest -q
uv run ruff check .
```

TypeScript (Node 20+):

```bash
npm install
npm run typecheck
```

## License

MIT — see [`LICENSE`](LICENSE).
