"""Generate executable delivery artifacts for the 20-feature Power BI factory layer.

This layer turns the feature contracts into concrete per-process artifacts:
source profiles, native M templates, schema drift contracts, semantic compile
plans, report materialization specs, DAX test plans, lineage, acceptance packs,
performance budgets, version manifests, and end-to-end build manifests.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG = ROOT / "data" / "industry_process_catalog.json"
FEATURE_CATALOG = ROOT / "data" / "powerbi_feature_catalog.json"
FROWN_KB = ROOT / "data" / "powerbi_frown_knowledge_base.json"
DEMO_ROOT = ROOT / "outputs" / "industry-demo-data"
PACK_ROOT = ROOT / "outputs" / "industry-process-packs"
EXEC_ROOT = ROOT / "outputs" / "powerbi-execution-layer"


FROWN_PATTERNS = [
    {
        "id": "ambiguous_relationship_path",
        "errorContains": "ambiguous paths",
        "rootCause": "Two active filter paths connect the same fact and dimension grain.",
        "fixStrategy": "Remove fact-to-fact relationships, deactivate alternate paths, or route through conformed dimensions only.",
        "validationCommand": "python scripts\\powerbi_expert_factory.py validate --project <pbip-folder>",
    },
    {
        "id": "numeric_powerquery_navigation",
        "errorContains": "key didn't match any rows",
        "rootCause": "Power Query navigates source tables by numeric row index such as Source{6}.",
        "fixStrategy": "Use key-based navigation such as Source{[Item=\"Table\", Kind=\"Sheet\"]}[Data].",
        "validationCommand": "python scripts\\powerbi_expert_factory.py validate --project <pbip-folder>",
    },
    {
        "id": "directquery_olap_unsupported_edit",
        "errorContains": "not supported for DirectQuery connections to OLAP sources",
        "rootCause": "Model contains semantic edits that Power BI blocks for DirectQuery over OLAP sources.",
        "fixStrategy": "Move calculations to the source model or switch to an Import/composite design supported by the source.",
        "validationCommand": "python scripts\\powerbi_expert_factory.py feature-plan --process <processId>",
    },
    {
        "id": "missing_visual_binding",
        "errorContains": "visual has missing fields",
        "rootCause": "PBIR visual references a table column or measure that is not present in TMDL.",
        "fixStrategy": "Regenerate visuals from the semantic model inventory and rerun visual binding validation.",
        "validationCommand": "python scripts\\powerbi_expert_factory.py validate --project <pbip-folder>",
    },
    {
        "id": "schema_drift_missing_column",
        "errorContains": "column of the table wasn't found",
        "rootCause": "Source schema changed after model generation.",
        "fixStrategy": "Run source profiling, compare against schema_drift_contract.json, and update the source mapping.",
        "validationCommand": "python scripts\\powerbi_expert_factory.py build --process <processId> --source demo --out <folder>",
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def infer_type(values: list[str]) -> str:
    cleaned = [value for value in values if value not in {"", None}]
    if not cleaned:
        return "string"
    lowered = {str(value).lower() for value in cleaned}
    if lowered <= {"true", "false"}:
        return "boolean"
    if all(_is_int(value) for value in cleaned):
        return "int64"
    if all(_is_float(value) for value in cleaned):
        return "double"
    if all(_is_date(value) for value in cleaned):
        return "date"
    return "string"


def _is_int(value: str) -> bool:
    try:
        int(str(value))
        return True
    except ValueError:
        return False


def _is_float(value: str) -> bool:
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def _is_date(value: str) -> bool:
    text = str(value)
    return len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-"


def pq_type(inferred: str) -> str:
    return {
        "boolean": "type logical",
        "int64": "Int64.Type",
        "double": "type number",
        "date": "type date",
        "string": "type text",
    }[inferred]


def profile_csv(path: Path) -> dict:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else []
    profile_columns = []
    for column in columns:
        values = [row.get(column, "") for row in rows]
        non_null = [value for value in values if value not in {"", None}]
        profile_columns.append(
            {
                "name": column,
                "inferredType": infer_type(values),
                "nullCount": len(values) - len(non_null),
                "distinctCount": len(set(non_null)),
                "sampleValues": non_null[:3],
            }
        )
    return {
        "file": path.name,
        "rowCount": len(rows),
        "columnCount": len(columns),
        "columns": profile_columns,
        "candidateKeys": [column["name"] for column in profile_columns if column["distinctCount"] == len(rows)],
    }


def build_m_query(table_name: str, source_file: str, columns: list[dict]) -> str:
    type_pairs = ", ".join(f'{{"{col["name"]}", {pq_type(col["inferredType"])}}}' for col in columns)
    return "\n".join(
        [
            "let",
            f'    Source = Csv.Document(File.Contents("<demo-or-production-folder>\\\\{source_file}"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),',
            "    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),",
            f"    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{{type_pairs}}}, \"en-US\")",
            "in",
            "    ChangedType",
        ]
    )


def process_folder(process_id: str) -> Path:
    return EXEC_ROOT / "processes" / process_id


def write_process_execution(process: dict, features: list[dict]) -> dict[str, object]:
    process_id = process["processId"]
    folder = process_folder(process_id)
    demo_folder = DEMO_ROOT / process_id
    pack_folder = PACK_ROOT / process_id
    model_spec = load_json(pack_folder / "model_spec.json")
    report_pages = load_json(pack_folder / "report_pages.json")
    quality_gate = load_json(pack_folder / "quality_gate.json")

    source_profiles = {path.name: profile_csv(path) for path in sorted(demo_folder.glob("*.csv"))}
    write_json(folder / "source_profile.json", {"processId": process_id, "tables": source_profiles})

    m_queries = {
        file_name.replace(".csv", ""): build_m_query(file_name.replace(".csv", ""), file_name, profile["columns"])
        for file_name, profile in source_profiles.items()
    }
    write_json(folder / "m_query_templates.json", {"processId": process_id, "queries": m_queries})

    schema_contract = {
        "processId": process_id,
        "rules": [
            {
                "file": file_name,
                "requiredColumns": [column["name"] for column in profile["columns"]],
                "typeExpectations": {column["name"]: column["inferredType"] for column in profile["columns"]},
                "driftPolicy": "block build on missing columns; warn on type widening; require owner signoff on renamed fields",
            }
            for file_name, profile in source_profiles.items()
        ],
    }
    write_json(folder / "schema_drift_contract.json", schema_contract)

    semantic_compile_plan = {
        "processId": process_id,
        "sourceProfile": "source_profile.json",
        "modelSpec": f"outputs/industry-process-packs/{process_id}/model_spec.json",
        "tables": model_spec["tables"],
        "relationships": model_spec["relationships"],
        "compileOutputs": ["TMDL tables", "relationships.tmdl", "measure table", "format strings"],
    }
    write_json(folder / "semantic_compile_plan.json", semantic_compile_plan)

    report_materialization = {
        "processId": process_id,
        "reportPages": report_pages["pages"],
        "materializationOutputs": ["PBIR pages", "visual containers", "visual binding maps"],
        "visualBindingRule": "All requiredFields and requiredMeasures must resolve against semantic_compile_plan.json.",
    }
    write_json(folder / "report_materialization_plan.json", report_materialization)

    dax_test_plan = {
        "processId": process_id,
        "measuresFile": f"outputs/industry-process-packs/{process_id}/dax_measures.dax",
        "testCases": [
            {
                "kpi": kpi,
                "expectedResultStrategy": "reconcile generated DAX against demo source totals and KPI snapshot tolerance",
                "tolerance": "use ProcessKpiSnapshots[Tolerance]",
            }
            for kpi in process["kpis"]
        ],
    }
    write_json(folder / "dax_expected_results_plan.json", dax_test_plan)

    lineage = {
        "processId": process_id,
        "nodes": {
            "sources": list(source_profiles),
            "tables": [table["name"] for table in model_spec["tables"]],
            "measures": process["kpis"],
            "reportPages": [page["name"] for page in report_pages["pages"]],
        },
        "edges": [
            {"from": "cases.csv", "to": "ProcessCases"},
            {"from": "events.csv", "to": "ProcessEvents"},
            {"from": "kpi_snapshots.csv", "to": "ProcessKpiSnapshots"},
            {"from": "ProcessCases", "to": "generated KPI measures"},
            {"from": "generated KPI measures", "to": "Executive Overview"},
        ],
    }
    write_json(folder / "lineage_graph.json", lineage)
    (folder / "lineage_graph.mmd").write_text(
        "graph LR\n"
        "  cases[cases.csv] --> ProcessCases\n"
        "  events[events.csv] --> ProcessEvents\n"
        "  kpi[kpi_snapshots.csv] --> ProcessKpiSnapshots\n"
        "  ProcessCases --> Measures\n"
        "  Measures --> ReportPages\n",
        encoding="utf-8",
    )

    acceptance_pack = {
        "processId": process_id,
        "processName": process["name"],
        "ownerRole": process["ownerRole"],
        "qualityGate": quality_gate,
        "ownerAcceptanceQuestions": [
            "Are KPI definitions and tolerances approved?",
            "Are native production source owners and gateways assigned?",
            "Are RLS/OLS assumptions approved by IT/CoE?",
            "Are action owners accountable for generated exception cockpits?",
        ],
    }
    write_json(folder / "process_owner_acceptance_pack.json", acceptance_pack)

    security_policy = {
        "processId": process_id,
        "roles": model_spec.get("rls", []),
        "olsPolicy": "classify sensitive partner, employee, financial, and compliance fields before production release",
        "tenantBoundary": "No credentials or secrets are stored in generated artifacts.",
    }
    write_json(folder / "security_policy_plan.json", security_policy)

    performance_budget = {
        "processId": process_id,
        "rowBudget": sum(profile["rowCount"] for profile in source_profiles.values()),
        "visualBudgetPerPage": 8,
        "relationshipBudget": len(model_spec["relationships"]),
        "directQueryRisk": "medium" if len(model_spec.get("productionSourceRouting", [])) > 4 else "low",
        "refreshBudget": "demo import under 5 minutes; production requires gateway/load test evidence",
    }
    write_json(folder / "performance_budget.json", performance_budget)

    version_manifest = {
        "processId": process_id,
        "version": "1.0.0",
        "compatibleFactoryVersion": "2026-05-04",
        "changePolicy": "semantic versioning for process packs; breaking source or KPI changes require minor/major release notes",
    }
    write_json(folder / "process_pack_version.json", version_manifest)

    feature_status = {
        "processId": process_id,
        "featureCount": len(features),
        "features": [
            {
                "featureId": feature["id"],
                "featureName": feature["name"],
                "status": "generated",
                "evidenceFolder": f"outputs/powerbi-execution-layer/processes/{process_id}",
            }
            for feature in features
        ],
    }
    write_json(folder / "feature_execution_status.json", feature_status)

    build_manifest = {
        "eventType": "powerbi_factory_process_build",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process_id,
        "processName": process["name"],
        "sourceMode": "demo",
        "artifacts": [
            "source_profile.json",
            "m_query_templates.json",
            "schema_drift_contract.json",
            "semantic_compile_plan.json",
            "report_materialization_plan.json",
            "dax_expected_results_plan.json",
            "lineage_graph.json",
            "process_owner_acceptance_pack.json",
            "security_policy_plan.json",
            "performance_budget.json",
            "process_pack_version.json",
            "feature_execution_status.json",
        ],
    }
    write_json(folder / "build_manifest.json", build_manifest)
    (folder / "README.md").write_text(
        f"# {process['name']} Execution Layer\n\n"
        "Generated executable delivery artifacts for source profiling, M generation, semantic compile planning, "
        "report materialization, DAX tests, lineage, governance, and process-owner acceptance.\n",
        encoding="utf-8",
    )
    return {
        "ProcessID": process_id,
        "ProcessName": process["name"],
        "ExecutionFolder": f"outputs/powerbi-execution-layer/processes/{process_id}",
        "ArtifactCount": len(build_manifest["artifacts"]),
        "FeatureCount": len(features),
    }


def write_global_artifacts(rows: list[dict[str, object]], features: list[dict]) -> None:
    write_json(
        FROWN_KB,
        {
            "version": "2026-05-04",
            "description": "Power BI Frown-to-Fix knowledge base for generated expert-replacement artifacts.",
            "patterns": FROWN_PATTERNS,
        },
    )
    write_json(
        EXEC_ROOT / "golden_reference_suite.json",
        {
            "version": "2026-05-04",
            "referenceProcesses": ["order2cash", "lead2order", "procure2pay", "record2report"],
            "requiredEvidence": [
                "source_profile.json",
                "semantic_compile_plan.json",
                "report_materialization_plan.json",
                "dax_expected_results_plan.json",
                "build_manifest.json",
            ],
        },
    )
    write_json(
        EXEC_ROOT / "demo_to_production_migration_wizard.json",
        {
            "steps": [
                "Select generated demo process pack",
                "Profile production source with native connector",
                "Map production fields to schema_drift_contract.json",
                "Regenerate M queries from m_query_templates.json",
                "Run semantic, visual, DAX, refresh, and Desktop smoke validation",
                "Create process owner and CoE acceptance evidence",
            ]
        },
    )
    with (EXEC_ROOT / "execution_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (EXEC_ROOT / "README.md").write_text(
        "# Power BI Execution Layer\n\n"
        "Concrete execution artifacts for all 20 Power BI Expert-Replacement Factory features across all 32 process packs.\n\n"
        "- `processes/<process>/source_profile.json`: real demo-source profiling output.\n"
        "- `processes/<process>/m_query_templates.json`: native Power Query/M templates.\n"
        "- `processes/<process>/schema_drift_contract.json`: source compatibility contract.\n"
        "- `processes/<process>/semantic_compile_plan.json`: semantic model compiler input.\n"
        "- `processes/<process>/report_materialization_plan.json`: PBIR materialization plan.\n"
        "- `processes/<process>/dax_expected_results_plan.json`: DAX test strategy.\n"
        "- `processes/<process>/lineage_graph.json`: source-to-KPI/report lineage.\n"
        "- `processes/<process>/process_owner_acceptance_pack.json`: owner signoff pack.\n"
        "- `execution_index.csv`: process-level execution index.\n",
        encoding="utf-8",
    )


def main() -> int:
    processes = load_json(PROCESS_CATALOG)["processes"]
    features = load_json(FEATURE_CATALOG)["features"]
    EXEC_ROOT.mkdir(parents=True, exist_ok=True)
    rows = [write_process_execution(process, features) for process in processes]
    write_global_artifacts(rows, features)
    print(f"generated execution layer for {len(rows)} processes and {len(features)} features")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
