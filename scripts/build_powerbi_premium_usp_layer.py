"""Generate the 25 Premium USP layer for the Power BI Expert-Replacement Factory."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG = ROOT / "data" / "industry_process_catalog.json"
PREMIUM_CATALOG = ROOT / "data" / "powerbi_premium_usp_catalog.json"
OUTPUT_ROOT = ROOT / "outputs" / "powerbi-premium-usp-layer"


PREMIUM_USPS = [
    ("real_source_connector_runner", "Real Source Connector Runner", "Execute real source profiling through native Power BI connector families without storing credentials.", "connector-runtime"),
    ("credential_safe_source_session", "Credential-Safe Source Session", "Run source checks through ephemeral credential sessions and persist only metadata and evidence.", "security-runtime"),
    ("auto_field_mapping_ai", "Auto Field Mapping AI", "Map source-specific fields such as KUNNR, CustomerNo, and AccountId to governed semantic fields.", "mapping-ai"),
    ("process_mining_import", "Process Mining Import", "Import event-log structures from Celonis, SAP Signavio, UiPath Process Mining, and ServiceNow.", "process-mining"),
    ("kpi_ontology_graph", "KPI Ontology / KPI Knowledge Graph", "Maintain KPI definitions, synonyms, formulas, owners, and comparability across processes.", "knowledge-graph"),
    ("business_question_router", "Business Question Router", "Route natural-language business questions to process packs, KPIs, data sources, measures, and visuals.", "intake-ai"),
    ("semantic_model_auto_repair", "Semantic Model Auto-Repair", "Generate repair patches for TMDL relationships, tables, measures, and naming issues.", "model-repair"),
    ("pbir_visual_materializer", "PBIR Visual Materializer", "Create PBIR visual containers from report specs and semantic bindings.", "report-runtime"),
    ("full_pbip_generator_all_processes", "Full PBIP Generator For All Processes", "Generate PBIP/PBIR/TMDL project skeletons for every industrial process pack.", "pbip-runtime"),
    ("powerbi_desktop_log_parser", "Power BI Desktop Log Parser", "Parse Desktop traces and Frown snapshots and connect them to repair knowledge.", "desktop-qa"),
    ("measure_benchmark_engine", "Measure Benchmark Engine", "Score DAX measures for complexity, dependencies, redundancy, and regression risk.", "dax-performance"),
    ("ai_report_critic_designer_scoring", "AI Report Critic / Designer Scoring", "Score report pages for UX, layout, visual choice, density, and executive readability.", "design-qa"),
    ("natural_language_dax_explainer", "Natural Language DAX Explainer", "Explain every DAX measure in business and technical language.", "dax-explainability"),
    ("what_if_scenario_generator", "What-if Scenario Generator", "Generate scenario models for SLA, capacity, cost, conversion, backlog, and risk changes.", "simulation"),
    ("action_recommendation_engine", "Action Recommendation Engine", "Recommend actions from root cause, value impact, risk, owner capacity, and SLA pressure.", "action-ai"),
    ("value_case_calculator", "Value Case Calculator", "Calculate opportunity value, effort, expected benefit, and confidence for each process initiative.", "value-management"),
    ("tenant_readiness_scanner", "Tenant Readiness Scanner", "Check tenant prerequisites for gateway, sensitivity labels, deployment pipelines, capacity, and RLS.", "tenant-governance"),
    ("deployment_pipeline_generator", "Deployment Pipeline Generator", "Generate Dev/Test/Prod deployment, release evidence, rollback, and approval plans.", "release-automation"),
    ("data_contract_generator", "Data Contract Generator", "Generate source-owner to process-owner contracts for fields, types, refresh SLA, drift, and ownership.", "data-contracts"),
    ("multi_agent_bi_sprint_orchestrator", "Multi-Agent BI Sprint Orchestrator", "Coordinate consultant, modeler, DAX, designer, QA, and CoE agents with evidence handoffs.", "agent-orchestration"),
    ("report_portfolio_rationalizer", "Report Portfolio Rationalizer", "Analyze existing reports, detect duplicates, and propose reusable target process packs.", "portfolio-optimization"),
    ("process_pack_marketplace_ui", "Process Pack Marketplace UI", "Define a UI-ready catalog for selecting, comparing, installing, and versioning process packs.", "marketplace-ui"),
    ("industry_compliance_packs", "Industry Compliance Packs", "Add SOX, GMP, ESG/CSRD, IATF, ISO 9001, and audit evidence requirements.", "compliance"),
    ("automated_documentation_publisher", "Automated Documentation Publisher", "Publish owner handbook, CoE pack, model docs, KPI glossary, and release notes.", "documentation-automation"),
    ("fabric_lakehouse_warehouse_scaffold", "Fabric Lakehouse/Warehouse Scaffold", "Generate optional Fabric Lakehouse, Warehouse, Notebook, and Pipeline architecture scaffolds.", "fabric-architecture"),
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_catalog() -> list[dict[str, object]]:
    capabilities = []
    for index, (capability_id, name, summary, capability_type) in enumerate(PREMIUM_USPS, start=1):
        capabilities.append(
            {
                "sequence": index,
                "id": capability_id,
                "name": name,
                "summary": summary,
                "capabilityType": capability_type,
                "implementationStatus": "implemented_as_premium_usp_contract",
                "inputs": [
                    "process context",
                    "source profile or metadata",
                    "semantic model contract",
                    "governance policy",
                ],
                "outputs": [
                    "premium capability contract",
                    "execution recipe",
                    "acceptance evidence contract",
                    "process mapping",
                ],
                "acceptanceChecks": [
                    "contract exists",
                    "process mapping exists",
                    "evidence requirements are explicit",
                    "no credentials or tenant secrets are persisted",
                ],
                "contractPath": f"outputs/powerbi-premium-usp-layer/capabilities/{capability_id}/premium_contract.json",
                "recipePath": f"outputs/powerbi-premium-usp-layer/capabilities/{capability_id}/execution_recipe.md",
                "evidencePath": f"outputs/powerbi-premium-usp-layer/capabilities/{capability_id}/evidence_contract.json",
            }
        )
    write_json(
        PREMIUM_CATALOG,
        {
            "version": "2026-05-04",
            "description": "Twenty-five premium USP features above the core Power BI Expert-Replacement Factory layer.",
            "capabilityCount": len(capabilities),
            "capabilities": capabilities,
        },
    )
    return capabilities


def write_capability_outputs(capabilities: list[dict[str, object]]) -> None:
    rows = []
    for capability in capabilities:
        folder = OUTPUT_ROOT / "capabilities" / str(capability["id"])
        write_json(folder / "premium_contract.json", capability)
        write_json(
            folder / "evidence_contract.json",
            {
                "id": capability["id"],
                "name": capability["name"],
                "requiredEvidence": [
                    "input metadata snapshot",
                    "generated decision output",
                    "validation result",
                    "owner or CoE acceptance note",
                ],
                "blockingRules": capability["acceptanceChecks"],
            },
        )
        (folder / "execution_recipe.md").write_text(
            f"# {capability['name']}\n\n"
            f"{capability['summary']}\n\n"
            "## Runtime Contract\n\n"
            "- Read process context from the selected process pack.\n"
            "- Use generated source profiles, semantic compile plans, lineage, and acceptance packs.\n"
            "- Persist metadata, generated plans, and validation evidence only.\n"
            "- Never persist credentials, tokens, or tenant secrets.\n\n"
            "## Acceptance Checks\n\n"
            + "\n".join(f"- {check}" for check in capability["acceptanceChecks"])
            + "\n",
            encoding="utf-8",
        )
        rows.append(
            {
                "CapabilityID": capability["id"],
                "CapabilityName": capability["name"],
                "CapabilityType": capability["capabilityType"],
                "Contract": capability["contractPath"],
                "Recipe": capability["recipePath"],
                "Evidence": capability["evidencePath"],
            }
        )
    with (OUTPUT_ROOT / "premium_usp_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_process_outputs(capabilities: list[dict[str, object]]) -> None:
    processes = load_json(PROCESS_CATALOG)["processes"]
    matrix_rows = []
    for process in processes:
        process_id = str(process["processId"])
        process_folder = OUTPUT_ROOT / "processes" / process_id
        plan = {
            "processId": process_id,
            "processName": process["name"],
            "domain": process["domain"],
            "premiumUspCount": len(capabilities),
            "premiumUsps": [
                {
                    "id": capability["id"],
                    "name": capability["name"],
                    "capabilityType": capability["capabilityType"],
                    "status": "planned_with_contract",
                    "contractPath": capability["contractPath"],
                    "evidencePath": capability["evidencePath"],
                }
                for capability in capabilities
            ],
            "dependsOn": {
                "coreFeatureContracts": "outputs/powerbi-feature-factory",
                "executionLayer": f"outputs/powerbi-execution-layer/processes/{process_id}",
                "processPack": f"outputs/industry-process-packs/{process_id}",
            },
        }
        write_json(process_folder / "premium_usp_plan.json", plan)
        (process_folder / "README.md").write_text(
            f"# {process['name']} Premium USP Plan\n\n"
            f"Maps all {len(capabilities)} premium USP contracts to `{process_id}`.\n",
            encoding="utf-8",
        )
        for capability in capabilities:
            matrix_rows.append(
                {
                    "ProcessID": process_id,
                    "ProcessName": process["name"],
                    "Domain": process["domain"],
                    "CapabilityID": capability["id"],
                    "CapabilityName": capability["name"],
                    "CapabilityType": capability["capabilityType"],
                    "Status": "planned_with_contract",
                }
            )
    with (OUTPUT_ROOT / "process_premium_usp_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix_rows[0].keys()))
        writer.writeheader()
        writer.writerows(matrix_rows)


def write_readme(capabilities: list[dict[str, object]]) -> None:
    lines = [
        "# Power BI Premium USP Layer",
        "",
        "Twenty-five premium USP contracts above the core 20-feature Power BI Expert-Replacement Factory layer.",
        "",
        "Generated artifacts:",
        "",
        "- `premium_usp_index.csv`: premium USP catalog index.",
        "- `process_premium_usp_matrix.csv`: all 25 premium USPs mapped to every industrial process.",
        "- `capabilities/<id>/premium_contract.json`: machine-readable premium USP contract.",
        "- `capabilities/<id>/execution_recipe.md`: implementation recipe and guardrails.",
        "- `capabilities/<id>/evidence_contract.json`: validation and release evidence requirements.",
        "- `processes/<process>/premium_usp_plan.json`: process-specific premium USP plan.",
        "",
        "## Premium USPs",
        "",
    ]
    lines.extend(f"- `{capability['id']}`: {capability['name']}" for capability in capabilities)
    (OUTPUT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    capabilities = build_catalog()
    write_capability_outputs(capabilities)
    write_process_outputs(capabilities)
    write_readme(capabilities)
    print(f"generated {len(capabilities)} premium USP contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
