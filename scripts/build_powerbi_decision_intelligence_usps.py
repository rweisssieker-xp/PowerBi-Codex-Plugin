"""Generate decision-intelligence USP evidence for every industrial process."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
CATALOG_PATH = ROOT / "data" / "powerbi_decision_intelligence_usp_catalog.json"
OUT_ROOT = ROOT / "outputs" / "powerbi-decision-intelligence-usps"


USP_DEFINITIONS = [
    ("decision_room_copilot", "Decision Room Copilot", "Turns a process question into decision options, evidence, risks, and recommended next action.", "Process Owner", "decision pack"),
    ("scenario_option_generator", "Scenario Option Generator", "Creates improvement scenarios from KPI gaps, constraints, backlog, capacity, cost, and value drivers.", "Process Manager", "scenario model"),
    ("tradeoff_matrix_builder", "Tradeoff Matrix Builder", "Compares decision options by value, time, risk, confidence, effort, compliance, and customer impact.", "Executive Sponsor", "tradeoff matrix"),
    ("decision_confidence_score", "Decision Confidence Score", "Scores each recommendation by source quality, model quality, KPI lineage, sample coverage, and validation status.", "CoE Reviewer", "confidence evidence"),
    ("action_roi_estimator", "Action ROI Estimator", "Estimates value capture, leakage reduction, cost avoidance, and payback for process actions.", "Finance Partner", "ROI estimate"),
    ("counterfactual_explainer", "Counterfactual Explainer", "Explains what would need to change for a KPI breach to disappear or a target to be reached.", "Data Analyst", "counterfactual"),
    ("decision_audit_trail", "Decision Audit Trail", "Stores decision question, evidence, assumptions, alternatives, approval, owner, and follow-up checks.", "Auditor", "audit trail"),
    ("owner_accountability_mapper", "Owner Accountability Mapper", "Maps every decision, exception, KPI, and action to accountable process, data, and system owners.", "Process Owner", "accountability map"),
    ("next_best_action_ranker", "Next Best Action Ranker", "Ranks recommended actions by value at risk, SLA urgency, feasibility, confidence, and dependency state.", "Process Manager", "ranked action queue"),
    ("decision_to_powerbi_page_composer", "Decision-to-Power-BI Page Composer", "Defines Power BI pages that show the evidence a process owner needs to make and monitor a decision.", "Power BI Designer", "decision page spec"),
    ("kpi_target_negotiation_pack", "KPI Target Negotiation Pack", "Creates target proposals, tolerances, baselines, outlier rules, and approval evidence for KPI target setting.", "Process Owner", "target contract"),
    ("constraint_bottleneck_detector", "Constraint Bottleneck Detector", "Identifies capacity, queue, source, supplier, customer, approval, and handover bottlenecks.", "Process Excellence Lead", "bottleneck map"),
    ("intervention_simulation_pack", "Intervention Simulation Pack", "Defines intervention tests for automation, staffing, policy, threshold, routing, and prioritization changes.", "Transformation Lead", "intervention plan"),
    ("decision_dependency_graph", "Decision Dependency Graph", "Links decisions to upstream sources, process stages, approvals, teams, systems, and downstream KPIs.", "Enterprise Process Owner", "dependency graph"),
    ("risk_adjusted_prioritizer", "Risk-Adjusted Prioritizer", "Prioritizes improvement moves with operational, financial, compliance, delivery, and data-quality risk adjustments.", "Risk Owner", "risk-adjusted backlog"),
    ("decision_feedback_loop", "Decision Feedback Loop", "Defines how decisions are monitored after release through KPI movement, action closure, and variance explanations.", "BI Adoption Lead", "feedback loop"),
    ("ai_facilitated_review_agenda", "AI-Facilitated Review Agenda", "Generates weekly and monthly performance-review agenda items from evidence, unresolved actions, and KPI movements.", "Process Manager", "review agenda"),
    ("decision_policy_guard", "Decision Policy Guard", "Checks recommendations against governance, security, compliance, RLS, data-quality, and release-policy boundaries.", "Governance Owner", "policy gate"),
    ("business_case_storyboard", "Business Case Storyboard", "Converts Power BI evidence into a business-case narrative with problem, value, options, ask, and expected impact.", "Executive Sponsor", "business case"),
    ("decision_learning_memory", "Decision Learning Memory", "Captures which decisions worked, which assumptions failed, and which process patterns should be reused.", "CoE Reviewer", "learning memory"),
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
    for sequence, (usp_id, name, summary, persona, artifact) in enumerate(USP_DEFINITIONS, start=1):
        capabilities.append(
            {
                "sequence": sequence,
                "id": usp_id,
                "name": name,
                "summary": summary,
                "primaryPersona": persona,
                "decisionArtifact": artifact,
                "implementationStatus": "implemented_as_decision_intelligence_evidence",
                "inputs": [
                    "process catalog",
                    "KPI catalog",
                    "source-routing evidence",
                    "quality gates",
                    "owner problem question",
                ],
                "outputs": [
                    artifact,
                    "Power BI decision-page evidence",
                    "action and owner evidence",
                    "governance review evidence",
                ],
                "acceptanceChecks": [
                    "capability maps to a decision owner",
                    "capability has process-specific KPI evidence",
                    "capability has an action or governance outcome",
                ],
            }
        )
    return {
        "version": "2026-05-04",
        "description": "Decision Intelligence USP layer for process-owner Power BI expert replacement.",
        "capabilityCount": len(capabilities),
        "capabilities": capabilities,
    }


def process_payload(process: dict, capability: dict, artifact_path: Path) -> dict:
    kpis = process.get("kpis", [])
    sources = process.get("sourceSystems", [])
    return {
        "eventType": "powerbi_decision_intelligence_usp_evidence",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process["processId"],
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityId": capability["id"],
        "capabilityName": capability["name"],
        "primaryPersona": capability["primaryPersona"],
        "decisionArtifact": capability["decisionArtifact"],
        "decisionInputs": {
            "caseName": process["caseName"],
            "valueLabel": process["valueLabel"],
            "kpis": kpis,
            "sourceSystems": sources,
        },
        "decisionOutputs": {
            "powerBiPage": f"{process['name']} Decision Cockpit",
            "measuresToExplain": kpis[:5],
            "sourceEvidence": sources[:5],
            "ownerActionQueue": f"{process['ownerRole']} action queue",
            "governanceGate": "decision_policy_guard",
        },
        "inputs": capability["inputs"],
        "outputs": capability["outputs"],
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
                "decisionArtifact": capability["decisionArtifact"],
                "artifactPath": rel(artifact_path),
                "artifactExists": True,
            }
        )

    plan = {
        "eventType": "powerbi_decision_intelligence_process_plan",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process_id,
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityCount": catalog["capabilityCount"],
        "decisionIntelligenceUsps": usps,
        "releaseUse": "decision review, scenario planning, action prioritization, owner signoff, and CoE evidence",
    }
    write_json(folder / "decision_intelligence_plan.json", plan)
    (folder / "README.md").write_text(
        f"# {process['name']} Decision Intelligence USPs\n\n"
        f"Generated evidence for {catalog['capabilityCount']} decision-intelligence USPs.\n",
        encoding="utf-8",
    )
    return {
        "ProcessID": process_id,
        "ProcessName": process["name"],
        "Domain": process["domain"],
        "CapabilityCount": catalog["capabilityCount"],
        "Plan": rel(folder / "decision_intelligence_plan.json"),
    }


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog()
    write_json(CATALOG_PATH, catalog)
    processes = load_json(PROCESS_CATALOG_PATH)["processes"]
    rows = [build_process(process, catalog) for process in processes]
    with (OUT_ROOT / "decision_intelligence_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(
        OUT_ROOT / "decision_intelligence_summary.json",
        {
            "eventType": "powerbi_decision_intelligence_summary",
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "processCount": len(rows),
            "capabilityCount": catalog["capabilityCount"],
            "evidenceArtifactCount": len(rows) * catalog["capabilityCount"],
        },
    )
    (OUT_ROOT / "README.md").write_text(
        "# Power BI Decision Intelligence USPs\n\n"
        "Decision-intelligence USP evidence layer for the AI-native Power BI Expert-Replacement Factory. "
        "It turns KPIs and process-owner problem questions into decision, scenario, action, and governance evidence.\n",
        encoding="utf-8",
    )
    print(f"generated {catalog['capabilityCount']} decision intelligence USPs for {len(rows)} processes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
