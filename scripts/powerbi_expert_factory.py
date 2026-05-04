#!/usr/bin/env python3
"""Executable trust layer for the Power BI Expert-Replacement Factory.

The goal is pragmatic static validation for generated PBIP/PBIR/TMDL projects.
It does not replace Power BI Desktop, but it catches the classes of mistakes that
made the O2C reference fail: ambiguous paths, invalid visual bindings, brittle M
source definitions, and missing delivery evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEATURE_CATALOG_PATH = ROOT / "data" / "powerbi_feature_catalog.json"
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"

TABLE_RE = re.compile(r"^table\s+(.+?)\s*$")
COLUMN_RE = re.compile(r"^\s*column\s+(.+?)\s*$")
MEASURE_RE = re.compile(r"^\s*measure\s+'?([^'=]+?)'?\s*=")
REL_RE = re.compile(r"^relationship\s+(.+?)\s*$")
FROM_RE = re.compile(r"^\s*fromColumn:\s*([^.]+)\.(.+?)\s*$")
TO_RE = re.compile(r"^\s*toColumn:\s*([^.]+)\.(.+?)\s*$")
SOURCE_FUNCTIONS = [
    "Excel.Workbook",
    "Csv.Document",
    "Json.Document",
    "OData.Feed",
    "Sql.Database",
    "Oracle.Database",
    "SapBusinessWarehouse.Cubes",
    "SharePoint.Files",
    "SharePoint.Contents",
    "Web.Contents",
    "Databricks.Catalogs",
    "Snowflake.Databases",
]


@dataclass
class Table:
    name: str
    path: str
    columns: set[str] = field(default_factory=set)
    measures: set[str] = field(default_factory=set)
    partitions: list[str] = field(default_factory=list)


@dataclass
class Relationship:
    name: str
    from_table: str
    from_column: str
    to_table: str
    to_column: str


@dataclass
class Model:
    project: Path
    tables: dict[str, Table]
    relationships: list[Relationship]


def _clean_name(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    return raw


def _project_definition(project: Path) -> Path:
    candidates = list(project.glob("*.SemanticModel/definition"))
    if candidates:
        return candidates[0]
    if (project / "definition").exists():
        return project / "definition"
    return project


def parse_model(project: str | Path) -> Model:
    root = Path(project)
    definition = _project_definition(root)
    tables: dict[str, Table] = {}
    relationships: list[Relationship] = []

    for tmdl in sorted((definition / "tables").glob("*.tmdl")):
        text = tmdl.read_text(encoding="utf-8")
        table_name = None
        table = None
        current_partition: list[str] | None = None
        for line in text.splitlines():
            table_match = TABLE_RE.match(line)
            if table_match:
                table_name = _clean_name(table_match.group(1))
                table = Table(name=table_name, path=str(tmdl))
                tables[table_name] = table
                current_partition = None
                continue
            if table is None:
                continue
            column_match = COLUMN_RE.match(line)
            if column_match:
                table.columns.add(_clean_name(column_match.group(1)))
                current_partition = None
                continue
            measure_match = MEASURE_RE.match(line)
            if measure_match:
                table.measures.add(_clean_name(measure_match.group(1).strip()))
                current_partition = None
                continue
            if line.lstrip().startswith("partition "):
                current_partition = [line]
                table.partitions.append(line)
                continue
            if current_partition is not None:
                current_partition.append(line)
                table.partitions[-1] = "\n".join(current_partition)

    rel_file = definition / "relationships.tmdl"
    if rel_file.exists():
        current: dict[str, str] = {}
        for line in rel_file.read_text(encoding="utf-8").splitlines():
            rel_match = REL_RE.match(line)
            if rel_match:
                if current:
                    rel = _relationship_from_dict(current)
                    if rel:
                        relationships.append(rel)
                current = {"name": rel_match.group(1)}
                continue
            from_match = FROM_RE.match(line)
            if from_match:
                current["from_table"] = from_match.group(1).strip()
                current["from_column"] = from_match.group(2).strip()
                continue
            to_match = TO_RE.match(line)
            if to_match:
                current["to_table"] = to_match.group(1).strip()
                current["to_column"] = to_match.group(2).strip()
        if current:
            rel = _relationship_from_dict(current)
            if rel:
                relationships.append(rel)

    return Model(project=root, tables=tables, relationships=relationships)


def _relationship_from_dict(raw: dict[str, str]) -> Relationship | None:
    required = {"name", "from_table", "from_column", "to_table", "to_column"}
    if not required.issubset(raw):
        return None
    return Relationship(
        name=raw["name"],
        from_table=raw["from_table"],
        from_column=raw["from_column"],
        to_table=raw["to_table"],
        to_column=raw["to_column"],
    )


def _is_fact(table: str) -> bool:
    return table.lower().startswith("fact_")


def _is_dimension(table: str) -> bool:
    lowered = table.lower()
    return lowered.startswith("dim_") or lowered in {"date", "calendar"}


def validate_model_graph(model: Model) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    adjacency: dict[str, set[str]] = defaultdict(set)

    for rel in model.relationships:
        for table_name, column_name, side in [
            (rel.from_table, rel.from_column, "fromColumn"),
            (rel.to_table, rel.to_column, "toColumn"),
        ]:
            if table_name not in model.tables:
                errors.append(f"Relationship {rel.name} references missing table {table_name} in {side}.")
            elif column_name not in model.tables[table_name].columns:
                errors.append(
                    f"Relationship {rel.name} references missing column {table_name}.{column_name} in {side}."
                )
        # TMDL generated here uses fromColumn = fact-side key and toColumn =
        # dimension-side key. Default single-direction filter flow therefore is
        # dimension -> fact. Ambiguous path checks must respect that direction;
        # otherwise a normal constellation/star schema with shared dimensions is
        # incorrectly reported as ambiguous.
        adjacency[rel.to_table].add(rel.from_table)
        if _is_fact(rel.from_table) and _is_fact(rel.to_table):
            errors.append(
                f"Relationship {rel.name} is Fact_* -> Fact_*; use Fact_* -> Dim_* only to prevent ambiguous paths."
            )
        if not (_is_fact(rel.from_table) and _is_dimension(rel.to_table)) and not (
            _is_dimension(rel.from_table) and _is_fact(rel.to_table)
        ):
            warnings.append(
                f"Relationship {rel.name} is not a clean Fact_* -> Dim_* edge: {rel.from_table} -> {rel.to_table}."
            )

    for rel in model.relationships:
        alternate = _has_alternate_path(adjacency, rel.to_table, rel.from_table, (rel.to_table, rel.from_table))
        if alternate:
            errors.append(
                f"Ambiguous path risk between {rel.from_table} and {rel.to_table}; direct relationship {rel.name} has another active path."
            )

    return _result("model_graph", errors, warnings, {"relationships": len(model.relationships)})


def _has_alternate_path(
    adjacency: dict[str, set[str]], start: str, target: str, skipped_edge: tuple[str, str]
) -> bool:
    skipped = {skipped_edge, (skipped_edge[1], skipped_edge[0])}
    queue: deque[str] = deque([start])
    seen = {start}
    while queue:
        node = queue.popleft()
        for nxt in adjacency.get(node, set()):
            if (node, nxt) in skipped:
                continue
            if nxt == target:
                return True
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def validate_native_sources(model: Model) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    connectors: dict[str, int] = defaultdict(int)

    for table in model.tables.values():
        if not table.partitions:
            warnings.append(f"Table {table.name} has no partition source.")
        for source in table.partitions:
            matched = False
            for fn in SOURCE_FUNCTIONS:
                count = source.count(fn)
                if count:
                    connectors[fn] += count
                    matched = True
            if "DATATABLE(" in source.upper():
                warnings.append(f"Table {table.name} uses DATATABLE; keep it out of production source routing.")
            if re.search(r"Source\s*\{\s*\d+\s*\}", source):
                errors.append(f"Table {table.name} uses numeric row navigation like Source{{6}}; use key navigation.")
            if "File.Contents" in source:
                for file_path in re.findall(r'File\.Contents\("([^"]+)"\)', source):
                    if not Path(file_path).exists() and not Path(model.project, file_path).exists():
                        warnings.append(f"Table {table.name} references a file path that is not present: {file_path}.")
            if not matched:
                warnings.append(f"Table {table.name} has no recognized native connector function in its partition.")

    return _result("native_sources", errors, warnings, {"connectors": dict(sorted(connectors.items()))})


def validate_visual_bindings(project: str | Path, model: Model) -> dict[str, Any]:
    root = Path(project)
    errors: list[str] = []
    warnings: list[str] = []
    visual_count = 0
    binding_count = 0

    for visual in sorted(root.glob("*.Report/definition/pages/*/visuals/*/visual.json")):
        visual_count += 1
        try:
            payload = json.loads(visual.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{visual}: invalid visual.json: {exc}")
            continue
        bindings = list(_iter_visual_fields(payload))
        binding_count += len(bindings)
        if not bindings:
            warnings.append(f"{visual}: visual has no query bindings.")
        for kind, table_name, item_name in bindings:
            if table_name not in model.tables:
                errors.append(f"{visual}: binding references missing table {table_name}.{item_name}.")
                continue
            table = model.tables[table_name]
            if kind == "Column" and item_name not in table.columns:
                errors.append(f"{visual}: binding references missing column {table_name}.{item_name}.")
            if kind == "Measure" and item_name not in table.measures:
                errors.append(f"{visual}: binding references missing measure {table_name}.{item_name}.")

    return _result("visual_bindings", errors, warnings, {"visuals": visual_count, "bindings": binding_count})


def _iter_visual_fields(node: Any):
    if isinstance(node, dict):
        for kind in ("Column", "Measure"):
            if kind in node and isinstance(node[kind], dict):
                field = node[kind]
                table_name = (
                    field.get("Expression", {})
                    .get("SourceRef", {})
                    .get("Entity")
                )
                item_name = field.get("Property") or field.get("Measure")
                if table_name and item_name:
                    yield kind, table_name, item_name
        for value in node.values():
            yield from _iter_visual_fields(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_visual_fields(item)


def validate_dax_static(model: Model) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    risky = ["EARLIER(", "USERELATIONSHIP(", "CROSSFILTER(", "ALL("]
    for table in model.tables.values():
        text = Path(table.path).read_text(encoding="utf-8")
        for token in risky:
            if token in text.upper():
                warnings.append(f"{table.name} contains {token}; require explicit KPI contract and regression test.")
    measure_count = sum(len(table.measures) for table in model.tables.values())
    if measure_count == 0:
        warnings.append("Model contains no measures; process analytics should expose governed KPIs.")
    return _result("dax_static", errors, warnings, {"measures": measure_count})


def run_acceptance(project: str | Path) -> dict[str, Any]:
    root = Path(project)
    model = parse_model(root)
    checks = [
        validate_model_graph(model),
        validate_native_sources(model),
        validate_visual_bindings(root, model),
        validate_dax_static(model),
    ]
    errors = [msg for check in checks for msg in check["errors"]]
    warnings = [msg for check in checks for msg in check["warnings"]]
    return {
        "status": "fail" if errors else "pass",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "project": str(root),
        "summary": {
            "tables": len(model.tables),
            "relationships": len(model.relationships),
            "measures": sum(len(table.measures) for table in model.tables.values()),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def write_evidence(project: str | Path, out: str | Path) -> dict[str, Any]:
    acceptance = run_acceptance(project)
    evidence = {
        "eventType": "powerbi_expert_factory_acceptance",
        "timestamp": acceptance["generatedAt"],
        "artifact": str(project),
        "status": acceptance["status"],
        "summary": acceptance["summary"],
        "checks": [
            {"name": check["name"], "status": check["status"], "errorCount": len(check["errors"])}
            for check in acceptance["checks"]
        ],
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    return evidence


def load_feature_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_feature_catalog.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist; run scripts\\build_powerbi_feature_factory.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def build_feature_delivery_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_feature_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")

    process = processes[normalized_process_id]
    feature_steps = []
    for index, feature in enumerate(catalog.get("features", []), start=1):
        contract_path = root / feature["contractPath"]
        validation_path = root / feature["validationContractPath"]
        feature_steps.append(
            {
                "sequence": index,
                "featureId": feature["id"],
                "featureName": feature["name"],
                "implementationType": feature["implementationType"],
                "inputs": feature["inputs"],
                "outputs": feature["outputs"],
                "cliCommands": feature["cliCommands"],
                "acceptanceChecks": feature["acceptanceChecks"],
                "contractPath": feature["contractPath"],
                "validationContractPath": feature["validationContractPath"],
                "contractExists": contract_path.exists(),
                "validationContractExists": validation_path.exists(),
            }
        )

    return {
        "eventType": "powerbi_expert_factory_feature_delivery_plan",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "requestedProcessId": process_id,
        "processId": normalized_process_id,
        "processName": process["name"],
        "domain": process["domain"],
        "featureCount": len(feature_steps),
        "features": feature_steps,
    }


def _normalize_process_id(process_id: str, processes: dict[str, Any]) -> str:
    if process_id in processes:
        return process_id
    normalized = process_id.lower().replace("-to-", "2").replace("_to_", "2").replace(" ", "")
    normalized = normalized.replace("-", "").replace("_", "")
    for known in processes:
        if known.lower().replace("-", "").replace("_", "") == normalized:
            return known
    return process_id


def _result(name: str, errors: list[str], warnings: list[str], meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "fail" if errors else "pass",
        "errors": errors,
        "warnings": warnings,
        **meta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PBIP/PBIR/TMDL projects for Power BI expert replacement.")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Run static acceptance checks.")
    validate.add_argument("--project", required=True)
    validate.add_argument("--out")

    evidence = sub.add_parser("evidence", help="Write a compact acceptance evidence event.")
    evidence.add_argument("--project", required=True)
    evidence.add_argument("--out", required=True)

    features = sub.add_parser("features", help="List executable USP feature contracts.")
    features.add_argument("--out")

    feature_plan = sub.add_parser("feature-plan", help="Create a 20-feature delivery plan for a process.")
    feature_plan.add_argument("--process", required=True)
    feature_plan.add_argument("--out")

    args = parser.parse_args()
    if args.command == "validate":
        result = run_acceptance(args.project)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 1 if result["status"] == "fail" else 0
    if args.command == "evidence":
        print(json.dumps(write_evidence(args.project, args.out), indent=2))
        return 0
    if args.command == "features":
        result = load_feature_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "feature-plan":
        result = build_feature_delivery_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
