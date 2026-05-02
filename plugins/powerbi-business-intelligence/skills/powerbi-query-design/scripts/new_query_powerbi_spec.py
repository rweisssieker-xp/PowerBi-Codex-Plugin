#!/usr/bin/env python3
"""Create a Power BI query-to-model spec from a business question."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--out", type=Path, default=Path("QUERY_POWERBI_SPEC.md"))
    args = parser.parse_args()
    content = f"""# Query to Power BI Spec

## Business Question

{args.question}

## Source Extraction

- Connector:
- Entities/tables:
- Filters:
- Fields:
- Pagination/folding:
- Incremental boundary:

## Power BI Model

- Fact grain:
- Dimensions:
- Relationships:
- Measures:
- RLS:

## Report and Validation

- Pages:
- Visuals:
- Reconciliation source:
- Acceptance checks:
"""
    args.out.write_text(content, encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

