#!/usr/bin/env python3
"""Generate a starter Power BI implementation pack from CSV specs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_csv(path: Path | None) -> list[dict[str, str]]:
    if not path:
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in value).strip("_") or "Item"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def powerquery_for_table(row: dict[str, str]) -> str:
    table = row.get("table") or "Fact"
    source_kind = (row.get("source_kind") or "OData").lower()
    source_entity = row.get("source_entity") or table
    incremental = row.get("incremental_column", "")
    if source_kind in {"sql", "database"}:
        body = f'Source = Sql.Database(ServerName, DatabaseName),\n    Entity = Source{{[Schema = SchemaName, Item = "{source_entity}"]}}[Data]'
    elif source_kind in {"file", "csv"}:
        body = f'Source = Csv.Document(File.Contents(FilePath), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),\n    Entity = Table.PromoteHeaders(Source, [PromoteAllScalars = true])'
    else:
        body = f'Source = OData.Feed(SourceUrl, null, [Implementation = "2.0"]),\n    Entity = Source{{[Name = "{source_entity}", Signature = "table"]}}[Data]'
    filter_step = ""
    output = "Entity"
    if incremental:
        filter_step = f',\n    Filtered = Table.SelectRows(Entity, each [{incremental}] >= RangeStart and [{incremental}] < RangeEnd)'
        output = "Filtered"
    return f"// Generated starter query for {table}.\nlet\n    {body}{filter_step}\nin\n    {output}\n"


def dax_measure(row: dict[str, str]) -> str:
    name = row.get("name") or "Measure"
    expression = row.get("expression") or "BLANK()"
    description = row.get("description", "")
    prefix = f"-- {description}\n" if description else ""
    return f"{prefix}{name} =\n{expression}\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables", type=Path)
    parser.add_argument("--measures", type=Path)
    parser.add_argument("--out", type=Path, default=Path("powerbi-pack"))
    args = parser.parse_args()

    tables = read_csv(args.tables)
    measures = read_csv(args.measures)
    for table in tables:
        write(args.out / "powerquery" / f"{safe_name(table.get('table', 'Fact'))}.pq", powerquery_for_table(table))
    write(args.out / "dax" / "measures.dax", "\n".join(dax_measure(row) for row in measures))
    write(args.out / "REPORT_SPEC.md", "# Power BI Report Spec\n\nDocument pages, visuals, filters, RLS, refresh, and validation.\n")
    write(args.out / "MAINTENANCE_RUNBOOK.md", "# Maintenance Runbook\n\nDocument owners, refresh SLA, gateway, release checks, and support process.\n")
    print(f"Wrote Power BI pack to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

