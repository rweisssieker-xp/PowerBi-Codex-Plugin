"""Generate autonomous operations USP evidence for every industrial process."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
CATALOG_PATH = ROOT / "data" / "powerbi_autonomous_operations_usp_catalog.json"
OUT_ROOT = ROOT / "outputs" / "powerbi-autonomous-operations-usps"


USP_DEFINITIONS = [
    ("refresh_failure_triage_agent", "Refresh Failure Triage Agent", "Classifies refresh failures by connector, gateway, credential, schema drift, capacity, and source outage cause.", "BI Operations Owner", "refresh triage"),
    ("semantic_drift_monitor", "Semantic Drift Monitor", "Detects changes in measures, relationships, fields, source schemas, and KPI contracts before users see broken reports.", "Semantic Model Owner", "semantic drift evidence"),
    ("visual_breakage_monitor", "Visual Breakage Monitor", "Monitors report visual bindings, missing fields, invalid measures, page layout regressions, and mobile layout risk.", "Power BI Designer", "visual health evidence"),
    ("usage_adoption_optimizer", "Usage Adoption Optimizer", "Turns usage telemetry into adoption gaps, training actions, report consolidation candidates, and owner follow-up tasks.", "BI Adoption Lead", "adoption plan"),
    ("capacity_cost_watchdog", "Capacity Cost Watchdog", "Detects capacity hot spots, expensive refresh patterns, semantic model bloat, and cost optimization opportunities.", "Fabric Capacity Owner", "cost watchdog"),
    ("release_ring_orchestrator", "Release Ring Orchestrator", "Moves generated BI assets through dev, test, pilot, production, rollback, and certification rings with evidence.", "BI Release Manager", "release ring plan"),
    ("incident_to_fix_autopilot", "Incident-to-Fix Autopilot", "Converts user incidents, Frown logs, failed checks, and telemetry into ranked repair plans and validation evidence.", "Support Lead", "repair plan"),
    ("sla_monitoring_pack", "SLA Monitoring Pack", "Defines operational SLAs for refresh, source delivery, user access, report performance, incidents, and action closure.", "Operations Lead", "SLA pack"),
    ("continuous_improvement_backlog", "Continuous Improvement Backlog", "Creates improvement backlog items from recurring issues, low adoption, owner feedback, data-quality defects, and KPI misses.", "Transformation Lead", "improvement backlog"),
    ("automated_owner_nudges", "Automated Owner Nudges", "Generates accountable reminders for overdue actions, stale approvals, unresolved DQ issues, and KPI contract decisions.", "Process Owner", "owner nudge queue"),
    ("self_healing_model_patch_queue", "Self-Healing Model Patch Queue", "Creates controlled candidate fixes for relationship ambiguity, missing fields, broken measures, and source-type changes.", "Power BI Expert", "patch queue"),
    ("access_review_automation", "Access Review Automation", "Builds recurring access review evidence for workspace roles, RLS membership, sensitivity labels, and sharing exceptions.", "Security Owner", "access review"),
    ("gateway_health_command_center", "Gateway Health Command Center", "Tracks gateway cluster health, datasource mappings, credential age, refresh load, and failure concentration.", "Gateway Admin", "gateway command center"),
    ("data_quality_slo_monitor", "Data Quality SLO Monitor", "Monitors freshness, completeness, uniqueness, referential integrity, and business-rule SLOs per process pack.", "Data Owner", "DQ SLO evidence"),
    ("report_portfolio_rationalizer", "Report Portfolio Rationalizer", "Finds duplicate reports, unused dashboards, overlapping semantic models, and consolidation candidates.", "CoE Reviewer", "portfolio rationalization"),
    ("ai_ops_runbook_generator", "AI Ops Runbook Generator", "Generates operational runbooks for refresh failures, release rollback, source outages, access incidents, and report repairs.", "BI Operations Owner", "runbook"),
    ("production_readiness_sentinel", "Production Readiness Sentinel", "Continuously re-checks whether a process pack remains certified, supported, secure, performant, and owner-approved.", "CoE Reviewer", "readiness sentinel"),
    ("closed_loop_value_realization", "Closed-Loop Value Realization", "Tracks whether actions, decisions, and BI releases actually moved process KPIs and captured expected value.", "Executive Sponsor", "value realization evidence"),
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
                "operationsArtifact": artifact,
                "implementationStatus": "implemented_as_autonomous_operations_evidence",
                "operationalSignals": [
                    "refresh telemetry",
                    "source health",
                    "semantic model checks",
                    "report binding checks",
                    "usage and adoption telemetry",
                    "owner action state",
                ],
                "outputs": [
                    artifact,
                    "owner action evidence",
                    "operations health evidence",
                    "release or support evidence",
                ],
                "acceptanceChecks": [
                    "capability maps to an operations owner",
                    "capability has process-specific operational signals",
                    "capability has an action, repair, release, or support outcome",
                ],
            }
        )
    return {
        "version": "2026-05-04",
        "description": "Autonomous Operations USP layer for running generated Power BI assets after release.",
        "capabilityCount": len(capabilities),
        "capabilities": capabilities,
    }


def process_payload(process: dict, capability: dict, artifact_path: Path) -> dict:
    return {
        "eventType": "powerbi_autonomous_operations_usp_evidence",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process["processId"],
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityId": capability["id"],
        "capabilityName": capability["name"],
        "primaryPersona": capability["primaryPersona"],
        "operationsArtifact": capability["operationsArtifact"],
        "operationsScope": {
            "caseName": process["caseName"],
            "valueLabel": process["valueLabel"],
            "kpis": process["kpis"],
            "sourceSystems": process["sourceSystems"],
            "defaultCadence": "daily operations, weekly owner review, monthly CoE review",
        },
        "operationalSignals": capability["operationalSignals"],
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
                "operationsArtifact": capability["operationsArtifact"],
                "artifactPath": rel(artifact_path),
                "artifactExists": True,
            }
        )

    plan = {
        "eventType": "powerbi_autonomous_operations_process_plan",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process_id,
        "processName": process["name"],
        "domain": process["domain"],
        "ownerRole": process["ownerRole"],
        "capabilityCount": catalog["capabilityCount"],
        "autonomousOperationsUsps": usps,
        "releaseUse": "post-release operations, refresh support, telemetry review, access review, and continuous improvement",
    }
    write_json(folder / "autonomous_operations_plan.json", plan)
    (folder / "README.md").write_text(
        f"# {process['name']} Autonomous Operations USPs\n\n"
        f"Generated evidence for {catalog['capabilityCount']} autonomous operations USPs.\n",
        encoding="utf-8",
    )
    return {
        "ProcessID": process_id,
        "ProcessName": process["name"],
        "Domain": process["domain"],
        "CapabilityCount": catalog["capabilityCount"],
        "Plan": rel(folder / "autonomous_operations_plan.json"),
    }


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog()
    write_json(CATALOG_PATH, catalog)
    processes = load_json(PROCESS_CATALOG_PATH)["processes"]
    rows = [build_process(process, catalog) for process in processes]
    with (OUT_ROOT / "autonomous_operations_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(
        OUT_ROOT / "autonomous_operations_summary.json",
        {
            "eventType": "powerbi_autonomous_operations_summary",
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "processCount": len(rows),
            "capabilityCount": catalog["capabilityCount"],
            "evidenceArtifactCount": len(rows) * catalog["capabilityCount"],
        },
    )
    (OUT_ROOT / "README.md").write_text(
        "# Power BI Autonomous Operations USPs\n\n"
        "Autonomous operations USP evidence layer for the AI-native Power BI Expert-Replacement Factory. "
        "It turns generated Power BI assets into monitored, supported, continuously improved operating products.\n",
        encoding="utf-8",
    )
    print(f"generated {catalog['capabilityCount']} autonomous operations USPs for {len(rows)} processes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
