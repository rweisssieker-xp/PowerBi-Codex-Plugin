#!/usr/bin/env python3
"""Executable trust layer for the Power BI Expert-Replacement Factory.

The goal is pragmatic static validation for generated PBIP/PBIR/TMDL projects.
It does not replace Power BI Desktop, but it catches the classes of mistakes that
made the O2C reference fail: ambiguous paths, invalid visual bindings, brittle M
source definitions, and missing delivery evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import zipfile
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import request


ROOT = Path(__file__).resolve().parents[1]
FEATURE_CATALOG_PATH = ROOT / "data" / "powerbi_feature_catalog.json"
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
PREMIUM_USP_CATALOG_PATH = ROOT / "data" / "powerbi_premium_usp_catalog.json"
RUNTIME_MAX_CATALOG_PATH = ROOT / "data" / "powerbi_runtime_max_catalog.json"
PRODUCTION_HARDENING_CATALOG_PATH = ROOT / "data" / "powerbi_production_hardening_catalog.json"
MARKET_DIFFERENTIATOR_USP_CATALOG_PATH = ROOT / "data" / "powerbi_market_differentiator_usp_catalog.json"
DECISION_INTELLIGENCE_USP_CATALOG_PATH = ROOT / "data" / "powerbi_decision_intelligence_usp_catalog.json"
AUTONOMOUS_OPERATIONS_USP_CATALOG_PATH = ROOT / "data" / "powerbi_autonomous_operations_usp_catalog.json"

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
    lowered = table.lower()
    return lowered.startswith("fact_") or lowered in {"processcases", "processevents", "processkpisnapshots"}


def _is_dimension(table: str) -> bool:
    lowered = table.lower()
    return lowered.startswith("dim_") or lowered in {"date", "calendar", "dimprocess", "dimcalendar"}


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
        process_event_to_case = rel.from_table == "ProcessEvents" and rel.to_table == "ProcessCases"
        if _is_fact(rel.from_table) and _is_fact(rel.to_table) and not process_event_to_case:
            errors.append(
                f"Relationship {rel.name} is Fact_* -> Fact_*; use Fact_* -> Dim_* only to prevent ambiguous paths."
            )
        clean_star_edge = (
            (_is_fact(rel.from_table) and _is_dimension(rel.to_table))
            or (_is_dimension(rel.from_table) and _is_fact(rel.to_table))
            or process_event_to_case
        )
        if not clean_star_edge:
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
            if "#table" in source:
                matched = True
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


def load_premium_usp_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_premium_usp_catalog.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist; run scripts\\build_powerbi_premium_usp_layer.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def build_premium_usp_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_premium_usp_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    plan_path = root / "outputs" / "powerbi-premium-usp-layer" / "processes" / normalized_process_id / "premium_usp_plan.json"
    if not plan_path.exists():
        raise FileNotFoundError(f"{plan_path} does not exist; run scripts\\build_powerbi_premium_usp_layer.py first.")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["requestedProcessId"] = process_id
    plan["catalogCapabilityCount"] = catalog.get("capabilityCount")
    return plan


def load_runtime_max_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_runtime_max_catalog.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist; run scripts\\build_powerbi_runtime_max_layer.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def build_runtime_max_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_runtime_max_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    manifest_path = root / "outputs" / "powerbi-runtime-max-layer" / "processes" / normalized_process_id / "runtime_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"{manifest_path} does not exist; run scripts\\build_powerbi_runtime_max_layer.py first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["requestedProcessId"] = process_id
    manifest["catalogCapabilityCount"] = catalog.get("capabilityCount")
    return manifest


def load_production_hardening_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_production_hardening_catalog.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist; run scripts\\build_powerbi_production_hardening_layer.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_market_differentiator_usp_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_market_differentiator_usp_catalog.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist; run scripts\\build_powerbi_market_differentiator_usps.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_decision_intelligence_usp_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_decision_intelligence_usp_catalog.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist; run scripts\\build_powerbi_decision_intelligence_usps.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_autonomous_operations_usp_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "powerbi_autonomous_operations_usp_catalog.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist; run scripts\\build_powerbi_autonomous_operations_usps.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_market_differentiator_usp_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_market_differentiator_usp_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    plan_path = (
        root
        / "outputs"
        / "powerbi-market-differentiator-usps"
        / "processes"
        / normalized_process_id
        / "market_differentiator_plan.json"
    )
    if not plan_path.exists():
        raise FileNotFoundError(
            f"{plan_path} does not exist; run scripts\\build_powerbi_market_differentiator_usps.py first."
        )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["requestedProcessId"] = process_id
    plan["catalogCapabilityCount"] = catalog.get("capabilityCount")
    return plan


def build_decision_intelligence_usp_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_decision_intelligence_usp_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    plan_path = (
        root
        / "outputs"
        / "powerbi-decision-intelligence-usps"
        / "processes"
        / normalized_process_id
        / "decision_intelligence_plan.json"
    )
    if not plan_path.exists():
        raise FileNotFoundError(
            f"{plan_path} does not exist; run scripts\\build_powerbi_decision_intelligence_usps.py first."
        )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["requestedProcessId"] = process_id
    plan["catalogCapabilityCount"] = catalog.get("capabilityCount")
    return plan


def build_autonomous_operations_usp_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_autonomous_operations_usp_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    plan_path = (
        root
        / "outputs"
        / "powerbi-autonomous-operations-usps"
        / "processes"
        / normalized_process_id
        / "autonomous_operations_plan.json"
    )
    if not plan_path.exists():
        raise FileNotFoundError(
            f"{plan_path} does not exist; run scripts\\build_powerbi_autonomous_operations_usps.py first."
        )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["requestedProcessId"] = process_id
    plan["catalogCapabilityCount"] = catalog.get("capabilityCount")
    return plan


def build_production_hardening_plan(process_id: str, root: Path = ROOT) -> dict[str, Any]:
    catalog = load_production_hardening_catalog(root)
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    dashboard_path = (
        root
        / "outputs"
        / "powerbi-production-hardening"
        / "processes"
        / normalized_process_id
        / "production_release_dashboard.json"
    )
    if not dashboard_path.exists():
        raise FileNotFoundError(
            f"{dashboard_path} does not exist; run scripts\\build_powerbi_production_hardening_layer.py first."
        )
    dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))
    dashboard["requestedProcessId"] = process_id
    dashboard["catalogCapabilityCount"] = catalog.get("capabilityCount")
    dashboard["hardeningFolder"] = str(dashboard_path.parent).replace("\\", "/")
    return dashboard


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


def build_process_delivery(process_id: str, source: str, out: str | Path, root: Path = ROOT) -> dict[str, Any]:
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")
    if source != "demo":
        raise ValueError("Only --source demo is executable locally; production sources require connector credentials.")

    execution_folder = root / "outputs" / "powerbi-execution-layer" / "processes" / normalized_process_id
    if not execution_folder.exists():
        raise FileNotFoundError(
            f"{execution_folder} does not exist; run scripts\\build_powerbi_execution_layer.py first."
        )

    out_path = Path(out)
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    copied = []
    for path in sorted(execution_folder.iterdir()):
        if path.is_file():
            target = out_path / path.name
            shutil.copy2(path, target)
            copied.append(target.name)

    source_demo = root / "outputs" / "industry-demo-data" / normalized_process_id
    demo_target = out_path / "demo-data"
    shutil.copytree(source_demo, demo_target)
    copied.append("demo-data/")

    pack_source = root / "outputs" / "industry-process-packs" / normalized_process_id
    pack_target = out_path / "process-pack"
    shutil.copytree(pack_source, pack_target)
    copied.append("process-pack/")

    result = {
        "eventType": "powerbi_expert_factory_local_build",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "requestedProcessId": process_id,
        "processId": normalized_process_id,
        "source": source,
        "output": str(out_path),
        "artifactCount": len(copied),
        "artifacts": copied,
        "nextValidationCommands": [
            "python scripts\\ci_repository_checks.py",
            f"python scripts\\powerbi_expert_factory.py feature-plan --process {normalized_process_id}",
        ],
    }
    (out_path / "local_build_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def build_powerbi_report_package(
    process_id: str,
    source_description: str,
    out: str | Path,
    report_goal: str = "",
    root: Path = ROOT,
) -> dict[str, Any]:
    process_catalog = json.loads((root / "data" / "industry_process_catalog.json").read_text(encoding="utf-8"))
    processes = {process["processId"]: process for process in process_catalog.get("processes", [])}
    normalized_process_id = _normalize_process_id(process_id, processes)
    if normalized_process_id not in processes:
        known = ", ".join(sorted(processes)[:8])
        raise ValueError(f"Unknown processId '{process_id}'. Known examples: {known}")

    runtime_manifest = build_runtime_max_plan(normalized_process_id, root)
    source_pbip = root / runtime_manifest["pbip"]["projectPath"]
    if not source_pbip.exists():
        raise FileNotFoundError(
            f"{source_pbip} does not exist; run scripts\\build_powerbi_runtime_max_layer.py first."
        )

    process = processes[normalized_process_id]
    out_path = Path(out)
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    pbip_target = out_path / "pbip" / source_pbip.name
    shutil.copytree(source_pbip, pbip_target)

    kpis = process.get("kpis", [])
    owner_role = process.get("ownerRole", "Process Owner")
    source_profile = {
        "eventType": "powerbi_report_source_profile",
        "processId": normalized_process_id,
        "processName": process["name"],
        "sourceDescription": source_description,
        "sourceMode": "demo_scaffold_with_production_source_contract",
        "credentialPolicy": "external_runtime_only",
        "recommendedConnectors": _recommended_connectors(source_description),
        "requiredSourceEvidence": ["row counts", "schema snapshot", "freshness timestamp", "owner signoff"],
    }
    model_plan = {
        "eventType": "powerbi_model_build_plan",
        "processId": normalized_process_id,
        "grain": "one row per process case with event-level drill-through",
        "facts": ["ProcessCases", "ProcessEvents", "ProcessKpiSnapshots"],
        "dimensions": ["DimProcess", "DimCalendar"],
        "relationships": ["ProcessEvents -> ProcessCases", "ProcessCases -> DimProcess", "ProcessKpiSnapshots -> DimCalendar"],
        "rlsRoles": [owner_role, "Process Manager", "Power BI CoE"],
        "buildOutput": str(pbip_target).replace("\\", "/"),
    }
    dax_plan = {
        "eventType": "powerbi_dax_measure_plan",
        "processId": normalized_process_id,
        "measureCount": len(kpis) + 5,
        "measures": [
            {"name": "Case Count", "expression": "COUNTROWS('ProcessCases')", "kpiContract": "case volume"},
            {"name": "SLA Breach Count", "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[SlaBreached] = TRUE())", "kpiContract": "SLA control"},
            {"name": "Action Required Count", "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[ActionRequired] = TRUE())", "kpiContract": "owner action"},
            {"name": "Average Cycle Days", "expression": "AVERAGE('ProcessCases'[CycleDays])", "kpiContract": "cycle time"},
            {"name": "Risk Weighted Value", "expression": "SUMX('ProcessCases', 'ProcessCases'[Value] * 'ProcessCases'[RiskScore])", "kpiContract": "risk exposure"},
        ]
        + [
            {
                "name": _measure_name(kpi),
                "expression": f"-- governed measure placeholder for {kpi}",
                "kpiContract": kpi,
            }
            for kpi in kpis
        ],
        "expectedResultPolicy": "compare generated measures to source aggregates before release",
    }
    m_plan = {
        "eventType": "power_query_m_plan",
        "processId": normalized_process_id,
        "nativeConnectorPolicy": "prefer native Power BI connectors over custom ingestion",
        "recommendedConnectors": source_profile["recommendedConnectors"],
        "templates": [
            "Excel.Workbook(File.Contents(...), null, true)",
            "SharePoint.Files(siteUrl)",
            "Sql.Database(server, database)",
            "OData.Feed(serviceRoot)",
        ],
        "qualityRules": ["no numeric Source{n} navigation", "explicit type conversion", "schema drift contract required"],
    }
    report_pages = {
        "eventType": "powerbi_report_pages_plan",
        "processId": normalized_process_id,
        "goal": report_goal or f"{process['name']} process owner cockpit",
        "pages": [
            {"name": "Executive Overview", "purpose": "KPI status, trend, risk, and decision summary"},
            {"name": "Process Flow And Aging", "purpose": "case flow, cycle time, aging, bottlenecks"},
            {"name": "Exception And Root Cause", "purpose": "SLA breaches, drivers, segments, drill paths"},
            {"name": "Owner Action Cockpit", "purpose": "owner queues, action required cases, priorities"},
            {"name": "Data Quality And Trust", "purpose": "freshness, source reconciliation, validation evidence"},
        ],
    }
    improvement_plan = {
        "eventType": "powerbi_model_improvement_plan",
        "processId": normalized_process_id,
        "improvements": [
            "validate star-schema relationships and remove ambiguous paths",
            "replace placeholder KPI measures with source-specific DAX after profiling",
            "add incremental refresh policy when date grain and source volume justify it",
            "score report pages for density, actionability, and visual binding quality",
            "run DAX query request and expected-result reconciliation before certification",
        ],
    }
    validation_plan = {
        "eventType": "powerbi_report_validation_plan",
        "processId": normalized_process_id,
        "commands": [
            f"python scripts\\powerbi_expert_factory.py validate --project {pbip_target} --out {out_path / 'validation_result.json'}",
            f"python scripts\\powerbi_expert_factory.py dax-query-request --workspace <workspace-id> --dataset <dataset-id> --query \"EVALUATE ROW(\\\"Cases\\\", [Case Count])\" --out {out_path / 'dax_query_request.json'}",
            f"python scripts\\powerbi_expert_factory.py rest-deploy-request --workspace <workspace-id> --artifact {pbip_target} --operation import --operation refresh --out {out_path / 'rest_deploy_request.json'}",
        ],
        "acceptanceChecks": ["no validation errors", "all visuals bind to existing fields", "source evidence has no secrets"],
    }

    artifacts = {
        "source_profile.json": source_profile,
        "model_build_plan.json": model_plan,
        "dax_measure_plan.json": dax_plan,
        "power_query_m_plan.json": m_plan,
        "report_pages_plan.json": report_pages,
        "model_improvement_plan.json": improvement_plan,
        "validation_plan.json": validation_plan,
    }
    for filename, payload in artifacts.items():
        (out_path / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "eventType": "powerbi_expert_factory_report_package",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "requestedProcessId": process_id,
        "processId": normalized_process_id,
        "processName": process["name"],
        "sourceDescription": source_description,
        "reportGoal": report_goal,
        "output": str(out_path),
        "pbip": {
            **runtime_manifest["pbip"],
            "projectPath": str(pbip_target).replace("\\", "/"),
        },
        "artifacts": sorted(artifacts),
        "nextCommands": validation_plan["commands"],
    }
    (out_path / "report_package_manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def build_generalist_autopilot_run(
    process_id: str,
    source_description: str,
    business_goal: str,
    out: str | Path,
    root: Path = ROOT,
) -> dict[str, Any]:
    out_path = Path(out)
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    package = build_powerbi_report_package(
        process_id,
        source_description,
        out_path / "report-package",
        business_goal,
        root,
    )
    runtime_plan = build_runtime_max_plan(package["processId"], root)
    (out_path / "runtime_max_plan.json").write_text(json.dumps(runtime_plan, indent=2), encoding="utf-8")

    result = {
        "eventType": "powerbi_generalist_autopilot_run",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "requestedProcessId": process_id,
        "processId": package["processId"],
        "processName": package["processName"],
        "businessGoal": business_goal,
        "sourceDescription": source_description,
        "businessSummary": [
            "A governed Power BI report/model package was generated from the process-owner request.",
            "The package includes model, DAX, Power Query/M, report-page, validation, and improvement artifacts.",
            "Authenticated tenant, DAX, gateway, and deployment actions remain approval-gated.",
        ],
        "outputs": {
            "reportPackage": str(out_path / "report-package").replace("\\", "/"),
            "runtimeMaxPlan": str(out_path / "runtime_max_plan.json").replace("\\", "/"),
        },
        "nextActions": [
            "review assumptions and owner acceptance questions",
            "run validation command from the report package",
            "connect authenticated runtime executors when tenant credentials are available",
        ],
    }
    (out_path / "generalist_autopilot_manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def build_generalist_prompt_run(prompt: str, out: str | Path, root: Path = ROOT) -> dict[str, Any]:
    out_path = Path(out)
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    interpreted = interpret_generalist_prompt(prompt)
    (out_path / "interpreted_request.json").write_text(json.dumps(interpreted, indent=2), encoding="utf-8")
    autopilot = build_generalist_autopilot_run(
        interpreted["processId"],
        interpreted["sourceDescription"],
        interpreted["businessGoal"],
        out_path / "autopilot",
        root,
    )
    result = {
        "eventType": "powerbi_generalist_prompt_run",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "interpretedRequest": interpreted,
        "autopilotManifest": str(out_path / "autopilot" / "generalist_autopilot_manifest.json").replace("\\", "/"),
        "reportPackage": autopilot["outputs"]["reportPackage"],
        "nextActions": autopilot["nextActions"],
    }
    (out_path / "generalist_prompt_run_manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def interpret_generalist_prompt(prompt: str) -> dict[str, Any]:
    text = prompt.lower()
    process_id = _infer_process_from_prompt(text)
    sources = _infer_sources_from_prompt(prompt)
    goal = _infer_goal_from_prompt(text)
    return {
        "eventType": "powerbi_generalist_prompt_interpretation",
        "processId": process_id,
        "sourceDescription": sources,
        "businessGoal": goal,
        "assumptions": [
            "free-text interpretation is heuristic until source metadata is scanned",
            "process owner wants actionability, not only KPI reporting",
            "credentials and live tenant actions remain approval-gated",
        ],
        "confidence": "medium" if process_id != "data2insight2action" else "low",
    }


def _infer_process_from_prompt(text: str) -> str:
    process_signals = [
        ("order2cash", ["o2c", "order to cash", "order2cash", "auftrag", "aufträge", "rechnung", "rechnungen", "cash", "lieferung", "lieferungen"]),
        ("lead2order", ["lead", "opportunity", "quote", "angebot", "auftragseingang", "vertriebspipeline"]),
        ("procure2pay", ["p2p", "procure", "purchase", "einkauf", "lieferant", "bestellung", "wareneingang"]),
        ("record2report", ["abschluss", "monatsabschluss", "close", "bilanz", "guv", "reporting close"]),
        ("complaint2capa", ["reklamation", "complaint", "capa", "abweichung", "nonconformance"]),
        ("dock2stock", ["lager", "warehouse", "dock", "stock", "wareneingang", "einlagerung"]),
    ]
    scores = []
    for process_id, tokens in process_signals:
        scores.append((sum(1 for token in tokens if token in text), process_id))
    score, process_id = max(scores)
    return process_id if score else "data2insight2action"


def _infer_sources_from_prompt(prompt: str) -> str:
    text = prompt.lower()
    sources = []
    if "sap" in text:
        sources.append("SAP export")
    if "excel" in text or "xlsx" in text:
        sources.append("Excel dispute or manual business list")
    if "csv" in text:
        sources.append("CSV operational extract")
    if "lager" in text or "warehouse" in text or "wms" in text:
        sources.append("warehouse delivery or inventory extract")
    if "crm" in text or "salesforce" in text or "dynamics" in text:
        sources.append("CRM opportunity/customer extract")
    if not sources:
        sources.append("source contract required from described business process")
    return ", ".join(dict.fromkeys(sources))


def _infer_goal_from_prompt(text: str) -> str:
    goals = []
    if "montag" in text or "monday" in text:
        goals.append("Monday process owner cockpit")
    else:
        goals.append("Process owner cockpit")
    if any(token in text for token in ["hängt", "haengen", "hängen", "stuck", "blockiert", "blocked"]):
        goals.append("stuck and blocked cases")
    if any(token in text for token in ["spät", "verspät", "late", "delay", "liefer"]):
        goals.append("late deliveries and aging")
    if "cash" in text:
        goals.append("cash risk")
    if any(token in text for token in ["rechnung", "invoice"]):
        goals.append("invoice blocks")
    if any(token in text for token in ["datenqualität", "data quality"]):
        goals.append("data quality drivers")
    goals.append("owners and prioritized next actions")
    return " for " + ", ".join(goals)


def run_pbix_binary_intake(pbix_path: str | Path, out: str | Path | None = None) -> dict[str, Any]:
    path = Path(pbix_path)
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path.suffix.lower() not in {".pbix", ".pbit"}:
        raise ValueError("PBIX binary intake supports .pbix and .pbit files only.")

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    entries: list[str] = []
    entry_meta: list[dict[str, Any]] = []
    unsupported: list[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            infos = sorted(archive.infolist(), key=lambda item: item.filename)
            for info in infos:
                entries.append(info.filename)
                entry_meta.append(
                    {
                        "name": info.filename,
                        "compressedBytes": info.compress_size,
                        "uncompressedBytes": info.file_size,
                    }
                )
    except zipfile.BadZipFile:
        unsupported.append("file is not a readable ZIP container")

    classification = {
        "hasReportLayout": any(name.lower().replace("\\", "/") in {"report/layout", "report/layout.json"} for name in entries),
        "hasDataModelSchema": any("datamodelschema" in name.lower() for name in entries),
        "hasConnections": any("connections" in name.lower() for name in entries),
        "hasMetadata": any("metadata" in name.lower() for name in entries),
    }
    result = {
        "eventType": "powerbi_runtime_executor_pbix_binary_intake",
        "executor": "pbix_binary_intake",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "parsed" if not unsupported else "unsupported",
        "file": {
            "path": str(path),
            "name": path.name,
            "extension": path.suffix.lower(),
            "bytes": path.stat().st_size,
            "sha256": digest,
        },
        "package": {
            "entryCount": len(entries),
            "entries": entries,
            "entryMetadata": entry_meta,
        },
        "classification": classification,
        "unsupportedArtifacts": unsupported,
        "credentialPolicy": "no_payload_content_or_secrets_emitted",
        "nextActions": [
            "map extractable metadata to legacy_report_reverse_engineer",
            "create migration blockers for unsupported binary sections",
            "run PBIP conversion when source project files are available",
        ],
    }
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def build_tenant_scan_request(tenant_id: str, workspace_ids: list[str] | None = None) -> dict[str, Any]:
    return _runtime_request(
        "live_tenant_scanner",
        "Power BI tenant scan request",
        {
            "tenantId": tenant_id,
            "workspaceIds": workspace_ids or ["*"],
            "include": ["workspaces", "datasets", "reports", "refreshes", "gateways", "lineage", "owners", "endorsements"],
        },
        [
            "GET /groups",
            "GET /groups/{workspaceId}/reports",
            "GET /groups/{workspaceId}/datasets",
            "GET /groups/{workspaceId}/datasets/{datasetId}/refreshes",
            "GET /gateways",
        ],
        ["tenant inventory", "workspace lineage map", "refresh and owner evidence"],
    )


def build_dax_query_run_request(workspace_id: str, dataset_id: str, dax_query: str) -> dict[str, Any]:
    return _runtime_request(
        "dax_query_runner",
        "DAX query execution request",
        {
            "workspaceId": workspace_id,
            "datasetId": dataset_id,
            "query": dax_query,
            "resultPolicy": "store_schema_row_counts_and_expected_result_verdicts",
        },
        ["POST /groups/{workspaceId}/datasets/{datasetId}/executeQueries"],
        ["query result evidence", "measure reconciliation verdict", "expected-result comparison"],
    )


def build_powerbi_rest_deployment_request(workspace_id: str, artifact_path: str, operations: list[str] | None = None) -> dict[str, Any]:
    selected = operations or ["import", "update_parameters", "refresh", "endorse"]
    return _runtime_request(
        "powerbi_rest_deployer",
        "Power BI REST deployment request",
        {
            "workspaceId": workspace_id,
            "artifactPath": artifact_path,
            "operationSequence": selected,
            "releaseApprovalRequired": True,
        },
        [f"REST operation: {operation}" for operation in selected],
        ["deployment evidence", "operation result manifest", "release approval record"],
    )


def build_gateway_audit_request(gateway_id: str, datasource_ids: list[str] | None = None) -> dict[str, Any]:
    return _runtime_request(
        "gateway_configuration_auditor",
        "Gateway configuration audit request",
        {
            "gatewayId": gateway_id,
            "datasourceIds": datasource_ids or ["*"],
            "checks": ["cluster ownership", "datasource mappings", "credential mode", "failover", "single point of failure"],
        },
        [
            "GET /gateways/{gatewayId}",
            "GET /gateways/{gatewayId}/datasources",
            "GET /gateways/{gatewayId}/datasources/{datasourceId}/users",
        ],
        ["gateway inventory", "datasource mapping", "risk and SPOF findings"],
    )


def run_tenant_scan_executor(
    tenant_id: str,
    workspace_ids: list[str] | None = None,
    transport=None,
) -> dict[str, Any]:
    runtime_request = build_tenant_scan_request(tenant_id, workspace_ids)
    planned = [
        {"method": "GET", "url": "https://api.powerbi.com/v1.0/myorg/groups"},
    ]
    for workspace_id in workspace_ids or []:
        planned.extend(
            [
                {"method": "GET", "url": f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports"},
                {"method": "GET", "url": f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"},
            ]
        )
    return _execute_powerbi_plan("live_tenant_scanner", runtime_request, planned, transport)


def run_dax_query_executor(
    workspace_id: str,
    dataset_id: str,
    dax_query: str,
    transport=None,
) -> dict[str, Any]:
    runtime_request = build_dax_query_run_request(workspace_id, dataset_id, dax_query)
    planned = [
        {
            "method": "POST",
            "url": f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/executeQueries",
            "payload": {"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        }
    ]
    return _execute_powerbi_plan("dax_query_runner", runtime_request, planned, transport)


def run_gateway_audit_executor(
    gateway_id: str,
    datasource_ids: list[str] | None = None,
    transport=None,
) -> dict[str, Any]:
    runtime_request = build_gateway_audit_request(gateway_id, datasource_ids)
    planned = [
        {"method": "GET", "url": f"https://api.powerbi.com/v1.0/myorg/gateways/{gateway_id}"},
        {"method": "GET", "url": f"https://api.powerbi.com/v1.0/myorg/gateways/{gateway_id}/datasources"},
    ]
    for datasource_id in datasource_ids or []:
        planned.append(
            {
                "method": "GET",
                "url": f"https://api.powerbi.com/v1.0/myorg/gateways/{gateway_id}/datasources/{datasource_id}/users",
            }
        )
    return _execute_powerbi_plan("gateway_configuration_auditor", runtime_request, planned, transport)


def run_powerbi_rest_executor(
    workspace_id: str,
    artifact_path: str,
    operations: list[str] | None = None,
    transport=None,
) -> dict[str, Any]:
    runtime_request = build_powerbi_rest_deployment_request(workspace_id, artifact_path, operations)
    selected = operations or ["import", "update_parameters", "refresh", "endorse"]
    planned = []
    for operation in selected:
        planned.append(
            {
                "method": "POST",
                "url": f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/{operation}",
                "payload": {"artifactPath": artifact_path, "operation": operation},
            }
        )
    return _execute_powerbi_plan("powerbi_rest_deployer", runtime_request, planned, transport)


def _execute_powerbi_plan(executor: str, runtime_request: dict[str, Any], planned: list[dict[str, Any]], transport=None) -> dict[str, Any]:
    token = os.environ.get("POWERBI_ACCESS_TOKEN")
    base = {
        "eventType": "powerbi_runtime_executor_result",
        "executor": executor,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "credentialPolicy": "external_runtime_only",
        "plannedRequests": _scrub_requests(planned),
        "runtimeRequest": runtime_request,
    }
    if not token:
        return {
            **base,
            "status": "dry_run",
            "reason": "POWERBI_ACCESS_TOKEN is not set; no external Power BI API call was made.",
            "evidence": ["planned request list", "credential boundary"],
        }

    caller = transport or _default_powerbi_transport
    responses = []
    for item in planned:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = caller(item["method"], item["url"], headers=headers, payload=item.get("payload"))
        responses.append(_summarize_response(response))
    return {
        **base,
        "status": "executed",
        "responseCount": len(responses),
        "responses": responses,
    }


def _default_powerbi_transport(method: str, url: str, headers: dict[str, str] | None = None, payload: Any = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers or {}, method=method)
    with request.urlopen(req, timeout=60) as response:
        text = response.read().decode("utf-8")
        return json.loads(text) if text else {"status": response.status}


def _scrub_requests(planned: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "method": item["method"],
            "url": item["url"],
            **({"payloadShape": sorted(item["payload"].keys())} if isinstance(item.get("payload"), dict) else {}),
        }
        for item in planned
    ]


def _summarize_response(response: Any) -> dict[str, Any]:
    if isinstance(response, dict):
        return {
            "keys": sorted(response.keys()),
            "rowCount": len(response.get("value", [])) if isinstance(response.get("value"), list) else None,
            "ok": response.get("ok", True),
        }
    return {"type": type(response).__name__}


def _runtime_request(
    executor: str,
    description: str,
    inputs: dict[str, Any],
    operations: list[str],
    evidence: list[str],
) -> dict[str, Any]:
    return {
        "eventType": "powerbi_runtime_executor_request",
        "executor": executor,
        "description": description,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "credentialPolicy": "external_runtime_only",
        "secretHandling": "caller supplies credentials outside generated artifacts; outputs store metadata and evidence only",
        "inputs": inputs,
        "operations": operations,
        "evidence": evidence,
        "status": "ready_for_authenticated_runtime",
    }


def _recommended_connectors(source_description: str) -> list[str]:
    lowered = source_description.lower()
    connectors = []
    if any(token in lowered for token in ["excel", "xlsx", "csv", "file export"]):
        connectors.append("Excel.Workbook / Folder.Files")
    if any(token in lowered for token in ["sharepoint", "onedrive"]):
        connectors.append("SharePoint.Files")
    if any(token in lowered for token in ["sql", "database", "warehouse"]):
        connectors.append("Sql.Database")
    if any(token in lowered for token in ["sap", "bw", "s/4", "s4"]):
        connectors.append("SAP Business Warehouse / OData")
    if any(token in lowered for token in ["crm", "dataverse", "dynamics"]):
        connectors.append("Dataverse / OData")
    if any(token in lowered for token in ["rest", "api"]):
        connectors.append("Web.Contents")
    return connectors or ["source contract required"]


def _measure_name(kpi: str) -> str:
    words = re.sub(r"[^A-Za-z0-9]+", " ", kpi).strip().split()
    return " ".join(word[:1].upper() + word[1:] for word in words) or "Governed KPI"


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


def _write_optional_json(payload: dict[str, Any], out: str | Path | None) -> None:
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(payload, indent=2), encoding="utf-8")


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

    premium_usps = sub.add_parser("premium-usps", help="List the 25 premium USP contracts.")
    premium_usps.add_argument("--out")

    runtime_max = sub.add_parser("runtime-max", help="List the 70 runtime max USP capabilities.")
    runtime_max.add_argument("--out")

    hardening = sub.add_parser("hardening", help="List the 15 production hardening capabilities.")
    hardening.add_argument("--out")

    market_usps = sub.add_parser("market-usps", help="List the 30 market differentiator USP capabilities.")
    market_usps.add_argument("--out")

    decision_usps = sub.add_parser("decision-usps", help="List the 20 decision intelligence USP capabilities.")
    decision_usps.add_argument("--out")

    operations_usps = sub.add_parser("operations-usps", help="List the 18 autonomous operations USP capabilities.")
    operations_usps.add_argument("--out")

    feature_plan = sub.add_parser("feature-plan", help="Create a 20-feature delivery plan for a process.")
    feature_plan.add_argument("--process", required=True)
    feature_plan.add_argument("--out")

    premium_plan = sub.add_parser("premium-usp-plan", help="Create a 25-premium-USP plan for a process.")
    premium_plan.add_argument("--process", required=True)
    premium_plan.add_argument("--out")

    runtime_plan = sub.add_parser("runtime-max-plan", help="Create a 70-USP runtime max plan for a process.")
    runtime_plan.add_argument("--process", required=True)
    runtime_plan.add_argument("--out")

    hardening_plan = sub.add_parser("hardening-plan", help="Create a production hardening dashboard for a process.")
    hardening_plan.add_argument("--process", required=True)
    hardening_plan.add_argument("--out")

    market_plan = sub.add_parser("market-usp-plan", help="Create a 30-USP market differentiator plan for a process.")
    market_plan.add_argument("--process", required=True)
    market_plan.add_argument("--out")

    decision_plan = sub.add_parser("decision-usp-plan", help="Create a 20-USP decision intelligence plan for a process.")
    decision_plan.add_argument("--process", required=True)
    decision_plan.add_argument("--out")

    operations_plan = sub.add_parser("operations-usp-plan", help="Create an 18-USP autonomous operations plan for a process.")
    operations_plan.add_argument("--process", required=True)
    operations_plan.add_argument("--out")

    build = sub.add_parser("build", help="Build a local process delivery bundle from the execution layer.")
    build.add_argument("--process", required=True)
    build.add_argument("--source", default="demo", choices=["demo"])
    build.add_argument("--out", required=True)

    report_package = sub.add_parser("report-package", help="Generate a Power BI report/model package for a process request.")
    report_package.add_argument("--process", required=True)
    report_package.add_argument("--sources", required=True)
    report_package.add_argument("--goal", default="")
    report_package.add_argument("--out", required=True)

    generalist_run = sub.add_parser("generalist-autopilot-run", help="Run Process Owner / Process Manager autonomous report-package delivery.")
    generalist_run.add_argument("--process", required=True)
    generalist_run.add_argument("--sources", required=True)
    generalist_run.add_argument("--goal", required=True)
    generalist_run.add_argument("--out", required=True)

    generalist_prompt = sub.add_parser("generalist-prompt-run", help="Interpret a free-text Process Owner request and run autonomous report-package delivery.")
    generalist_prompt.add_argument("--prompt", required=True)
    generalist_prompt.add_argument("--out", required=True)

    pbix_intake = sub.add_parser("pbix-intake", help="Run credential-safe PBIX/PBIT binary intake metadata extraction.")
    pbix_intake.add_argument("--file", required=True)
    pbix_intake.add_argument("--out")

    tenant_scan = sub.add_parser("tenant-scan-request", help="Create a credential-safe tenant scanner runtime request.")
    tenant_scan.add_argument("--tenant", required=True)
    tenant_scan.add_argument("--workspace", action="append", dest="workspaces")
    tenant_scan.add_argument("--out")

    dax_run = sub.add_parser("dax-query-request", help="Create a credential-safe DAX query runner request.")
    dax_run.add_argument("--workspace", required=True)
    dax_run.add_argument("--dataset", required=True)
    dax_run.add_argument("--query", required=True)
    dax_run.add_argument("--out")

    rest_deploy = sub.add_parser("rest-deploy-request", help="Create a credential-safe Power BI REST deployment request.")
    rest_deploy.add_argument("--workspace", required=True)
    rest_deploy.add_argument("--artifact", required=True)
    rest_deploy.add_argument("--operation", action="append", dest="operations")
    rest_deploy.add_argument("--out")

    gateway_audit = sub.add_parser("gateway-audit-request", help="Create a credential-safe gateway audit runtime request.")
    gateway_audit.add_argument("--gateway", required=True)
    gateway_audit.add_argument("--datasource", action="append", dest="datasources")
    gateway_audit.add_argument("--out")

    tenant_scan_run = sub.add_parser("tenant-scan-run", help="Run tenant scanner when POWERBI_ACCESS_TOKEN is set, otherwise return dry-run evidence.")
    tenant_scan_run.add_argument("--tenant", required=True)
    tenant_scan_run.add_argument("--workspace", action="append", dest="workspaces")
    tenant_scan_run.add_argument("--out")

    dax_run_live = sub.add_parser("dax-query-run", help="Run DAX query when POWERBI_ACCESS_TOKEN is set, otherwise return dry-run evidence.")
    dax_run_live.add_argument("--workspace", required=True)
    dax_run_live.add_argument("--dataset", required=True)
    dax_run_live.add_argument("--query", required=True)
    dax_run_live.add_argument("--out")

    rest_deploy_run = sub.add_parser("rest-deploy-run", help="Run Power BI REST operations when POWERBI_ACCESS_TOKEN is set, otherwise return dry-run evidence.")
    rest_deploy_run.add_argument("--workspace", required=True)
    rest_deploy_run.add_argument("--artifact", required=True)
    rest_deploy_run.add_argument("--operation", action="append", dest="operations")
    rest_deploy_run.add_argument("--out")

    gateway_audit_run = sub.add_parser("gateway-audit-run", help="Run gateway audit when POWERBI_ACCESS_TOKEN is set, otherwise return dry-run evidence.")
    gateway_audit_run.add_argument("--gateway", required=True)
    gateway_audit_run.add_argument("--datasource", action="append", dest="datasources")
    gateway_audit_run.add_argument("--out")

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
    if args.command == "premium-usps":
        result = load_premium_usp_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "runtime-max":
        result = load_runtime_max_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "hardening":
        result = load_production_hardening_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "market-usps":
        result = load_market_differentiator_usp_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "decision-usps":
        result = load_decision_intelligence_usp_catalog()
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "operations-usps":
        result = load_autonomous_operations_usp_catalog()
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
    if args.command == "premium-usp-plan":
        result = build_premium_usp_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "runtime-max-plan":
        result = build_runtime_max_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "hardening-plan":
        result = build_production_hardening_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "market-usp-plan":
        result = build_market_differentiator_usp_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "decision-usp-plan":
        result = build_decision_intelligence_usp_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "operations-usp-plan":
        result = build_autonomous_operations_usp_plan(args.process)
        text = json.dumps(result, indent=2)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0
    if args.command == "build":
        result = build_process_delivery(args.process, args.source, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "report-package":
        result = build_powerbi_report_package(args.process, args.sources, args.out, args.goal)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "generalist-autopilot-run":
        result = build_generalist_autopilot_run(args.process, args.sources, args.goal, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "generalist-prompt-run":
        result = build_generalist_prompt_run(args.prompt, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "pbix-intake":
        result = run_pbix_binary_intake(args.file, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "tenant-scan-request":
        result = build_tenant_scan_request(args.tenant, args.workspaces)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "dax-query-request":
        result = build_dax_query_run_request(args.workspace, args.dataset, args.query)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "rest-deploy-request":
        result = build_powerbi_rest_deployment_request(args.workspace, args.artifact, args.operations)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "gateway-audit-request":
        result = build_gateway_audit_request(args.gateway, args.datasources)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "tenant-scan-run":
        result = run_tenant_scan_executor(args.tenant, args.workspaces)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "dax-query-run":
        result = run_dax_query_executor(args.workspace, args.dataset, args.query)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "rest-deploy-run":
        result = run_powerbi_rest_executor(args.workspace, args.artifact, args.operations)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "gateway-audit-run":
        result = run_gateway_audit_executor(args.gateway, args.datasources)
        _write_optional_json(result, args.out)
        print(json.dumps(result, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
