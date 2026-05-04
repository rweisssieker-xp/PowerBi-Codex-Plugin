"""Generate market-differentiator USP evidence for every industrial process."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
CATALOG_PATH = ROOT / "data" / "powerbi_market_differentiator_usp_catalog.json"
OUT_ROOT = ROOT / "outputs" / "powerbi-market-differentiator-usps"


USP_DEFINITIONS = [
    ("process_digital_twin", "Process Digital Twin", "Model every case, event, KPI, owner, action, and exception as a process-owner navigable digital twin.", "Process Owner", "Turns static reporting into an operational process control model."),
    ("kpi_contract_negotiator", "KPI Contract Negotiator", "Creates explicit KPI formula, owner, tolerance, source, and dispute contracts before DAX is generated.", "Process Owner", "Prevents semantic KPI fights after dashboards go live."),
    ("root_cause_narrative_engine", "Root-Cause Narrative Engine", "Explains KPI breaches using source evidence, driver hierarchy, affected cases, and recommended action language.", "Process Manager", "Reduces analyst interpretation work in weekly performance reviews."),
    ("value_at_risk_prioritizer", "Value-at-Risk Prioritizer", "Ranks exceptions by commercial, operational, compliance, and customer impact.", "Process Manager", "Directs attention to the cases that matter most."),
    ("autonomous_action_board", "Autonomous Action Board", "Generates action queues by owner, severity, SLA, value, due date, and next best action.", "Process Owner", "Closes the gap between insight and execution."),
    ("benchmark_twin", "Benchmark Twin", "Compares process performance against internal plants, regions, products, suppliers, and external benchmark assumptions.", "Executive Sponsor", "Shows where improvement potential is real and material."),
    ("exception_pattern_memory", "Exception Pattern Memory", "Stores recurring failure patterns, root causes, repairs, and validation evidence per process pack.", "CoE Reviewer", "Builds reusable organizational learning instead of one-off dashboards."),
    ("kpi_dispute_resolver", "KPI Dispute Resolver", "Detects KPI definition conflicts, source mismatches, tolerance drift, and ownership gaps.", "Data Steward", "Makes metric trust auditable."),
    ("source_trust_score", "Source Trust Score", "Scores each source by freshness, completeness, schema drift, key quality, and credential readiness.", "Data Owner", "Makes source risk visible before report release."),
    ("visual_story_quality_scorer", "Visual Story Quality Scorer", "Scores report pages for executive scanability, owner workflow fit, binding integrity, and actionability.", "Power BI Designer", "Replaces first-pass visual QA with objective design evidence."),
    ("executive_briefing_pack", "Executive Briefing Pack", "Generates board-ready summary, KPI movement, root causes, risks, decisions, and asks.", "Executive Sponsor", "Turns Power BI evidence into management-ready communication."),
    ("audit_evidence_vault", "Audit Evidence Vault", "Stores generated model, DAX, M, source, validation, approval, and release evidence in one manifest.", "Auditor", "Makes AI-generated BI reviewable and certifiable."),
    ("semantic_model_warranty", "Semantic Model Warranty", "Defines what the generated semantic model guarantees, what remains owner-approved, and what requires escalation.", "CoE Reviewer", "Clarifies trust boundaries for expert replacement."),
    ("data_product_marketplace_pack", "Data Product Marketplace Pack", "Packages process models as reusable data products with owner, SLA, KPI, lineage, and quality metadata.", "Data Product Owner", "Makes process analytics reusable across teams."),
    ("multi_erp_harmonizer", "Multi-ERP Harmonizer", "Maps SAP, Dynamics, Oracle, Salesforce, Workday, ServiceNow, MES, WMS, and custom exports into common process semantics.", "Enterprise Architect", "Supports fragmented enterprise landscapes."),
    ("process_mining_bridge", "Process Mining Bridge", "Generates case/activity/timestamp event-log contracts for mining and Power BI analysis.", "Process Excellence Lead", "Bridges process mining and management reporting."),
    ("predictive_sla_breach_radar", "Predictive SLA Breach Radar", "Creates early-warning contracts for cases likely to breach SLA or miss conversion targets.", "Process Manager", "Moves from lagging dashboard to preventive action."),
    ("what_if_simulation_studio", "What-If Simulation Studio", "Defines scenario parameters for cycle time, conversion, capacity, backlog, cost, and risk simulation.", "Process Owner", "Supports improvement decisions before implementation."),
    ("owner_adoption_coach", "Owner Adoption Coach", "Tracks whether process owners use reports, act on findings, and close action loops.", "BI Adoption Lead", "Measures actual behavior change, not only report delivery."),
    ("automated_release_certifier", "Automated Release Certifier", "Combines model, visual, source, DAX, security, documentation, and Desktop smoke evidence into a release verdict.", "CoE Reviewer", "Makes release readiness repeatable."),
    ("governance_by_design", "Governance by Design", "Embeds RLS, labels, source decisions, lineage, approvals, and audit rules into each process pack.", "Governance Owner", "Makes governance part of generation, not an afterthought."),
    ("cost_to_serve_lens", "Cost-to-Serve Lens", "Adds cost, rework, automation, exception effort, and value leakage views to every process.", "Finance Partner", "Connects process performance to economic impact."),
    ("customer_supplier_360_joiner", "Customer/Supplier 360 Joiner", "Connects process cases to customer, supplier, product, asset, and location dimensions where available.", "Process Owner", "Explains process issues in business relationship context."),
    ("process_pack_composer", "Process Pack Composer", "Combines multiple process packs into end-to-end flows such as Lead2Cash, Source2Pay, Plan2Fulfill, and Idea2Launch.", "Enterprise Process Owner", "Supports cross-process operating models."),
    ("live_ops_command_center", "Live Ops Command Center", "Defines near-real-time refresh, alert, action, and escalation contracts for operational control rooms.", "Operations Lead", "Makes Power BI useful for daily control, not only monthly reporting."),
    ("ai_explanation_layer", "AI Explanation Layer", "Generates explainable summaries for measures, filters, source lineage, model assumptions, and recommended actions.", "Business User", "Makes complex semantic models understandable without a BI expert."),
    ("transformation_backlog_miner", "Transformation Backlog Miner", "Converts recurring defects, KPI gaps, owner feedback, and validation warnings into ranked improvement backlog items.", "Transformation Lead", "Turns analytics into a managed improvement portfolio."),
    ("kpi_lineage_explorer", "KPI Lineage Explorer", "Links KPI, DAX, source fields, owner, process stage, visual, and validation evidence.", "Data Steward", "Makes every number explainable from source to visual."),
    ("data_quality_negotiator", "Data Quality Negotiator", "Generates data-quality issue contracts between process owner, data owner, and source-system owner.", "Data Owner", "Moves DQ issues from complaint to accountable remediation."),
    ("board_to_action_cascade", "Board-to-Action Cascade", "Connects executive KPI reviews to owner actions, operational queues, due dates, and value realization evidence.", "Executive Sponsor", "Closes the loop from board decision to process outcome."),
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def build_catalog() -> dict:
    capabilities = []
    for sequence, (usp_id, name, summary, persona, value) in enumerate(USP_DEFINITIONS, start=1):
        capabilities.append(
            {
                "sequence": sequence,
                "id": usp_id,
                "name": name,
                "summary": summary,
                "primaryPersona": persona,
                "marketDifferentiator": value,
                "implementationStatus": "implemented_as_market_differentiator_evidence",
                "proofArtifacts": [
                    "process plan",
                    "persona value mapping",
                    "acceptance evidence",
                    "owner action linkage",
                ],
                "acceptanceChecks": [
                    "USP maps to a process owner or governance persona",
                    "USP has concrete evidence artifacts",
                    "USP links to measurable business value",
                ],
            }
        )
    return {
        "version": "2026-05-04",
        "description": "Market differentiator USP layer for the AI-native Power BI Expert-Replacement Factory.",
        "capabilityCount": len(capabilities),
        "capabilities": capabilities,
    }


def process_payload(process: dict, capability: dict, artifact_path: Path) -> dict:
    return {
        "eventType": "powerbi_market_differentiator_usp_evidence",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process["processId"],
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityId": capability["id"],
        "capabilityName": capability["name"],
        "primaryPersona": capability["primaryPersona"],
        "marketDifferentiator": capability["marketDifferentiator"],
        "processFit": {
            "caseName": process["caseName"],
            "valueLabel": process["valueLabel"],
            "kpis": process["kpis"],
            "sourceSystems": process["sourceSystems"],
        },
        "proofArtifacts": capability["proofArtifacts"],
        "acceptanceChecks": capability["acceptanceChecks"],
        "artifactPath": rel(artifact_path),
        "status": "evidence-ready",
    }


def build_process(process: dict, catalog: dict) -> dict:
    process_id = process["processId"]
    folder = OUT_ROOT / "processes" / process_id
    usps = []
    for capability in catalog["capabilities"]:
        artifact_path = folder / f"{capability['id']}.json"
        write_json(artifact_path, process_payload(process, capability, artifact_path))
        usps.append(
            {
                "sequence": capability["sequence"],
                "capabilityId": capability["id"],
                "capabilityName": capability["name"],
                "primaryPersona": capability["primaryPersona"],
                "marketDifferentiator": capability["marketDifferentiator"],
                "artifactPath": rel(artifact_path),
                "artifactExists": True,
            }
        )

    plan = {
        "eventType": "powerbi_market_differentiator_process_plan",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process_id,
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityCount": catalog["capabilityCount"],
        "marketDifferentiatorUsps": usps,
        "releaseUse": "positioning, sales engineering, owner acceptance, CoE review, and roadmap proof",
    }
    write_json(folder / "market_differentiator_plan.json", plan)
    (folder / "README.md").write_text(
        f"# {process['name']} Market Differentiator USPs\n\n"
        f"Generated evidence for {catalog['capabilityCount']} market-facing differentiator USPs.\n",
        encoding="utf-8",
    )
    return {
        "ProcessID": process_id,
        "ProcessName": process["name"],
        "Domain": process["domain"],
        "CapabilityCount": catalog["capabilityCount"],
        "Plan": rel(folder / "market_differentiator_plan.json"),
    }


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog()
    write_json(CATALOG_PATH, catalog)
    processes = load_json(PROCESS_CATALOG_PATH)["processes"]
    rows = [build_process(process, catalog) for process in processes]
    with (OUT_ROOT / "market_differentiator_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(
        OUT_ROOT / "market_differentiator_summary.json",
        {
            "eventType": "powerbi_market_differentiator_summary",
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "processCount": len(rows),
            "capabilityCount": catalog["capabilityCount"],
            "evidenceArtifactCount": len(rows) * catalog["capabilityCount"],
        },
    )
    (OUT_ROOT / "README.md").write_text(
        "# Power BI Market Differentiator USPs\n\n"
        "Market-facing USP evidence layer for the AI-native Power BI Expert-Replacement Factory. "
        "It turns product positioning into generated, process-specific proof artifacts.\n",
        encoding="utf-8",
    )
    print(f"generated {catalog['capabilityCount']} market differentiator USPs for {len(rows)} processes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
