#!/usr/bin/env python3
"""Generate a DAX measure pack from a CSV catalog."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measure-catalog", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    with args.measure_catalog.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dax_lines: list[str] = []
    for row in rows:
        name = row.get("measure") or row.get("name") or "Measure"
        expression = row.get("expression") or "BLANK()"
        definition = row.get("business_definition") or row.get("description") or ""
        if definition:
            dax_lines.append(f"-- {definition}")
        dax_lines.append(f"{name} =")
        dax_lines.append(expression)
        dax_lines.append("")

    (args.out_dir / "measures.dax").write_text("\n".join(dax_lines), encoding="utf-8")
    print(f"Wrote {len(rows)} measures to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

