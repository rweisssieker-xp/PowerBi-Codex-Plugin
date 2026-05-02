#!/usr/bin/env python3
"""Create a Power BI business problem blueprint."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("problem")
    parser.add_argument("--out", type=Path, default=Path("POWERBI_BUSINESS_BLUEPRINT.md"))
    args = parser.parse_args()
    content = f"""# {args.problem} Power BI Blueprint

## Executive Intent

- Decision owner:
- Business decision:
- Target behavior:
- Success metric:

## Data Source Plan

- Source systems:
- Connector pattern:
- Refresh mode:
- Gateway/security:
- Reconciliation source:

## Semantic Model

- Fact grain:
- Fact tables:
- Dimensions:
- Relationships:
- RLS/OLS:

## KPI and DAX Catalog

| KPI | Business Definition | DAX Measure | Validation |
| --- | --- | --- | --- |

## Report Pages

1. Executive overview
2. Driver analysis
3. Flow/cohort/aging analysis
4. Exceptions and next actions
5. Detail and reconciliation

## Delivery

- PBIP/PBIX artifact:
- Deployment pipeline:
- Refresh SLA:
- Support owner:
"""
    args.out.write_text(content, encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

