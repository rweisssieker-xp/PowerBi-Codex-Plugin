#!/usr/bin/env python3
"""Create a generic Power BI report specification from a business problem."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# {title}

## Business Outcome

- Decision owner:
- Business question:
- Required action:

## Data Sources

- Source systems:
- Connector pattern:
- Refresh mode:
- Credential and gateway notes:

## Semantic Model

- Fact grain:
- Dimensions:
- Relationships:
- Measures:
- RLS/OLS:

## Report Pages

1. Executive overview
2. Driver analysis
3. Cohort/process/flow analysis
4. Exceptions and next actions
5. Detail and reconciliation

## Validation

- Source totals:
- KPI definitions:
- Security tests:
- Refresh tests:
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    parser.add_argument("--out", type=Path, default=Path("POWERBI_REPORT_SPEC.md"))
    args = parser.parse_args()
    args.out.write_text(TEMPLATE.format(title=args.title), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
