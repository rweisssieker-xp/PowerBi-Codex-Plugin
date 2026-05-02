#!/usr/bin/env python3
"""Create a generic semantic model specification."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--out", type=Path, default=Path("SEMANTIC_MODEL_SPEC.md"))
    args = parser.parse_args()
    content = f"""# {args.name} Semantic Model Spec

## Scope

- Business process:
- Source systems:
- Refresh mode:

## Facts

| Fact | Grain | Source | Incremental Column |
| --- | --- | --- | --- |

## Dimensions

| Dimension | Key | Attributes | Security Notes |
| --- | --- | --- | --- |

## Measures

| Measure | Definition | DAX | Validation |
| --- | --- | --- | --- |

## Relationships, Security, and Refresh

- Relationships:
- RLS/OLS:
- Gateway:
- Incremental refresh:
- Deployment pipeline:
"""
    args.out.write_text(content, encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

