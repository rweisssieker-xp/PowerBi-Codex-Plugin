"""Build a concrete Lead2Order Power BI analysis package."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_CATALOG = ROOT / "data" / "industry_process_catalog.json"
RUNTIME_PBIP = (
    ROOT
    / "outputs"
    / "powerbi-runtime-max-layer"
    / "processes"
    / "lead2order"
    / "pbip"
    / "Lead2Order"
)
OUT_ROOT = ROOT / "outputs" / "lead2order-powerbi-analysis"
OUT_PBIP = OUT_ROOT / "pbip" / "Lead2OrderAnalysis"


MEASURES = [
    {
        "name": "Lead Count",
        "kpi": "Lead Volume",
        "expression": "COUNTROWS('ProcessCases')",
        "format": "#,0",
        "question": "How many leads are currently in the Lead2Order funnel?",
        "decision": "Size daily intake, qualification workload, and sales follow-up capacity.",
    },
    {
        "name": "Pipeline Value",
        "kpi": "Pipeline Value",
        "expression": "SUM('ProcessCases'[PipelineValue])",
        "format": "#,0.00",
        "question": "How much commercial value is currently exposed in the funnel?",
        "decision": "Prioritize high-value leads and opportunity follow-up.",
    },
    {
        "name": "Average Pipeline Value",
        "kpi": "Pipeline Value",
        "expression": "AVERAGE('ProcessCases'[PipelineValue])",
        "format": "#,0.00",
        "question": "Which segments create high-value or low-value leads?",
        "decision": "Tune campaign targeting, qualification thresholds, and sales coverage.",
    },
    {
        "name": "MQL Count",
        "kpi": "MQL Rate",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[CurrentStage] <> \"Lead Created\")",
        "format": "#,0",
        "question": "How many leads moved beyond raw lead creation?",
        "decision": "Validate marketing qualification throughput.",
    },
    {
        "name": "MQL Rate",
        "kpi": "MQL Rate",
        "expression": "DIVIDE([MQL Count], [Lead Count])",
        "format": "0.0%",
        "question": "What share of leads becomes marketing qualified?",
        "decision": "Identify campaign, segment, and data-quality weaknesses.",
    },
    {
        "name": "SQL Count",
        "kpi": "SQL Rate",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[CurrentStage] IN {\"Opportunity Created\", \"Quote Sent\", \"Order Booked\"})",
        "format": "#,0",
        "question": "How many qualified leads become sales-accepted pipeline?",
        "decision": "Balance marketing handoff quality and sales acceptance capacity.",
    },
    {
        "name": "SQL Rate",
        "kpi": "SQL Rate",
        "expression": "DIVIDE([SQL Count], [MQL Count])",
        "format": "0.0%",
        "question": "Where does marketing-to-sales handoff leak conversion?",
        "decision": "Improve lead scoring, acceptance criteria, and routing logic.",
    },
    {
        "name": "Quote Count",
        "kpi": "Order Conversion Rate",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[CurrentStage] IN {\"Quote Sent\", \"Order Booked\"})",
        "format": "#,0",
        "question": "How many opportunities reach commercial quotation?",
        "decision": "Spot CPQ, pricing, or approval bottlenecks.",
    },
    {
        "name": "Order Count",
        "kpi": "Order Conversion Rate",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[CurrentStage] = \"Order Booked\")",
        "format": "#,0",
        "question": "How many Lead2Order cases become booked orders?",
        "decision": "Track conversion outcome and compare against target.",
    },
    {
        "name": "Order Conversion Rate",
        "kpi": "Order Conversion Rate",
        "expression": "DIVIDE([Order Count], [Lead Count])",
        "format": "0.0%",
        "question": "Which leads, owners, regions, and partners convert to orders?",
        "decision": "Focus sales actions on conversion blockers and high-yield segments.",
    },
    {
        "name": "Lead-to-Order Cycle Days",
        "kpi": "Lead-to-Order Cycle Time",
        "expression": "AVERAGE('ProcessCases'[ActualCycleDays])",
        "format": "#,0.0",
        "question": "How long does Lead2Order take end to end?",
        "decision": "Find cycle-time waste and target bottleneck removal.",
    },
    {
        "name": "Cycle Days vs Target",
        "kpi": "Lead-to-Order Cycle Time",
        "expression": "AVERAGE('ProcessCases'[ActualCycleDays]) - AVERAGE('ProcessCases'[TargetCycleDays])",
        "format": "#,0.0",
        "question": "Is Lead2Order faster or slower than target?",
        "decision": "Quantify process drift and SLA exposure.",
    },
    {
        "name": "SLA Breach Count",
        "kpi": "Lead-to-Order Cycle Time",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[SlaBreached] = TRUE())",
        "format": "#,0",
        "question": "How many Lead2Order cases breach SLA?",
        "decision": "Prioritize exception queues and owner escalation.",
    },
    {
        "name": "SLA Breach Rate",
        "kpi": "Lead-to-Order Cycle Time",
        "expression": "DIVIDE([SLA Breach Count], [Lead Count])",
        "format": "0.0%",
        "question": "What share of cases violates the Lead2Order SLA?",
        "decision": "Assess process reliability and backlog pressure.",
    },
    {
        "name": "Action Required Count",
        "kpi": "Action Backlog",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[ActionRequired] = TRUE())",
        "format": "#,0",
        "question": "How many cases need owner action now?",
        "decision": "Drive daily process-owner action management.",
    },
    {
        "name": "Action Required Rate",
        "kpi": "Action Backlog",
        "expression": "DIVIDE([Action Required Count], [Lead Count])",
        "format": "0.0%",
        "question": "How large is the actionable exception share?",
        "decision": "Assess whether the process is under control.",
    },
    {
        "name": "High Risk Lead Count",
        "kpi": "Pipeline Risk",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[RiskScore] >= 70)",
        "format": "#,0",
        "question": "Which leads carry high process or conversion risk?",
        "decision": "Focus owner attention on cases likely to fail or delay.",
    },
    {
        "name": "High Risk Pipeline Value",
        "kpi": "Pipeline Risk",
        "expression": "CALCULATE([Pipeline Value], 'ProcessCases'[RiskScore] >= 70)",
        "format": "#,0.00",
        "question": "How much pipeline value is at high risk?",
        "decision": "Protect revenue by escalating high-value risk cases.",
    },
    {
        "name": "Average Risk Score",
        "kpi": "Pipeline Risk",
        "expression": "AVERAGE('ProcessCases'[RiskScore])",
        "format": "#,0.0",
        "question": "Which regions, owners, or partners create elevated process risk?",
        "decision": "Prioritize root-cause remediation by segment.",
    },
    {
        "name": "Rework Event Count",
        "kpi": "Process Rework",
        "expression": "CALCULATE(COUNTROWS('ProcessEvents'), 'ProcessEvents'[ReworkFlag] = TRUE())",
        "format": "#,0",
        "question": "How much rework occurs in the Lead2Order event stream?",
        "decision": "Remove avoidable loops in qualification, CPQ, pricing, and order booking.",
    },
    {
        "name": "Automation Event Count",
        "kpi": "Automation Coverage",
        "expression": "CALCULATE(COUNTROWS('ProcessEvents'), 'ProcessEvents'[AutomationFlag] = TRUE())",
        "format": "#,0",
        "question": "How many process events run automated?",
        "decision": "Measure digital execution maturity.",
    },
    {
        "name": "Automation Rate",
        "kpi": "Automation Coverage",
        "expression": "DIVIDE([Automation Event Count], COUNTROWS('ProcessEvents'))",
        "format": "0.0%",
        "question": "Where is Lead2Order still manually executed?",
        "decision": "Find automation and workflow opportunities.",
    },
    {
        "name": "Total Event Cost",
        "kpi": "Process Cost",
        "expression": "SUM('ProcessEvents'[EventCost])",
        "format": "#,0.00",
        "question": "What is the operational event cost of Lead2Order?",
        "decision": "Quantify cost-to-serve and rework economics.",
    },
    {
        "name": "Average Event Cost",
        "kpi": "Process Cost",
        "expression": "AVERAGE('ProcessEvents'[EventCost])",
        "format": "#,0.00",
        "question": "Which activities are cost outliers?",
        "decision": "Prioritize cost optimization by event and owner.",
    },
    {
        "name": "KPI Red Count",
        "kpi": "KPI Health",
        "expression": "CALCULATE(COUNTROWS('ProcessKpiSnapshots'), 'ProcessKpiSnapshots'[Status] = \"Red\")",
        "format": "#,0",
        "question": "How many KPI periods are red?",
        "decision": "Focus management attention on failing metrics.",
    },
    {
        "name": "KPI Amber Count",
        "kpi": "KPI Health",
        "expression": "CALCULATE(COUNTROWS('ProcessKpiSnapshots'), 'ProcessKpiSnapshots'[Status] = \"Amber\")",
        "format": "#,0",
        "question": "How many KPI periods show early warning?",
        "decision": "Act before red KPI failure occurs.",
    },
    {
        "name": "KPI Green Count",
        "kpi": "KPI Health",
        "expression": "CALCULATE(COUNTROWS('ProcessKpiSnapshots'), 'ProcessKpiSnapshots'[Status] = \"Green\")",
        "format": "#,0",
        "question": "How many KPI periods are healthy?",
        "decision": "Distinguish controlled segments from exceptions.",
    },
    {
        "name": "Average KPI Gap",
        "kpi": "KPI Health",
        "expression": "AVERAGE('ProcessKpiSnapshots'[ActualValue]) - AVERAGE('ProcessKpiSnapshots'[TargetValue])",
        "format": "#,0.00",
        "question": "How far are Lead2Order KPIs from target?",
        "decision": "Quantify performance gap and management priority.",
    },
    {
        "name": "Root Cause Case Count",
        "kpi": "Root Cause",
        "expression": "CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[RootCause] <> \"\")",
        "format": "#,0",
        "question": "How many exceptions have a root cause recorded?",
        "decision": "Assess diagnostic completeness and evidence quality.",
    },
    {
        "name": "Root Cause Coverage Rate",
        "kpi": "Root Cause",
        "expression": "DIVIDE([Root Cause Case Count], [SLA Breach Count])",
        "format": "0.0%",
        "question": "Are breached cases explained well enough to act?",
        "decision": "Improve root-cause discipline before assigning actions.",
    },
]


PROBLEM_QUESTIONS = [
    {
        "area": "Funnel throughput",
        "question": "Where do leads drop between lead creation, qualification, opportunity, quote, and booked order?",
        "primaryMeasures": ["Lead Count", "MQL Rate", "SQL Rate", "Order Conversion Rate"],
        "drilldowns": ["CurrentStage", "Region", "OwnerName", "BusinessPartner"],
        "action": "Fix the stage with the largest conversion loss and assign owner-specific follow-up.",
    },
    {
        "area": "Pipeline value protection",
        "question": "Which high-value leads are blocked, delayed, or high risk?",
        "primaryMeasures": ["Pipeline Value", "High Risk Pipeline Value", "Action Required Count"],
        "drilldowns": ["BusinessPartner", "OwnerName", "RootCause", "CurrentStage"],
        "action": "Escalate high-value, high-risk cases before quote or order loss.",
    },
    {
        "area": "Cycle time and SLA",
        "question": "Why is Lead2Order slower than target and which owner queues create the delay?",
        "primaryMeasures": ["Lead-to-Order Cycle Days", "Cycle Days vs Target", "SLA Breach Rate"],
        "drilldowns": ["CurrentStage", "OwnerName", "Region", "RootCause"],
        "action": "Remove bottlenecks and rebalance workload for owners with SLA concentration.",
    },
    {
        "area": "Marketing-to-sales handoff",
        "question": "Are MQLs becoming SQLs with sufficient quality and speed?",
        "primaryMeasures": ["MQL Count", "MQL Rate", "SQL Count", "SQL Rate"],
        "drilldowns": ["Region", "BusinessPartner", "OwnerName"],
        "action": "Tune lead scoring and acceptance criteria where SQL conversion is weak.",
    },
    {
        "area": "Quote and CPQ execution",
        "question": "Which leads reach quote stage, and where do pricing, approval, or configuration delays appear?",
        "primaryMeasures": ["Quote Count", "Order Conversion Rate", "Lead-to-Order Cycle Days"],
        "drilldowns": ["CurrentStage", "RootCause", "OwnerName"],
        "action": "Target CPQ and approval process improvements.",
    },
    {
        "area": "Root-cause quality",
        "question": "Are SLA breaches explained with enough root-cause evidence?",
        "primaryMeasures": ["Root Cause Case Count", "Root Cause Coverage Rate", "SLA Breach Count"],
        "drilldowns": ["RootCause", "OwnerName", "Region"],
        "action": "Require root-cause completion for all actionable breaches.",
    },
    {
        "area": "Operational cost and rework",
        "question": "Which activities create avoidable event cost and rework?",
        "primaryMeasures": ["Rework Event Count", "Total Event Cost", "Average Event Cost"],
        "drilldowns": ["EventName", "SourceSystem", "TouchedBy"],
        "action": "Automate, simplify, or standardize high-cost event paths.",
    },
    {
        "area": "Automation opportunity",
        "question": "Which Lead2Order steps remain manual and should be automated?",
        "primaryMeasures": ["Automation Event Count", "Automation Rate", "Rework Event Count"],
        "drilldowns": ["EventName", "SourceSystem", "TouchedBy"],
        "action": "Prioritize workflow automation where manual effort and rework overlap.",
    },
    {
        "area": "KPI health",
        "question": "Which KPIs are red or amber, and what is the target gap?",
        "primaryMeasures": ["KPI Red Count", "KPI Amber Count", "Average KPI Gap"],
        "drilldowns": ["KPIName", "Period", "OwnerRole"],
        "action": "Create a KPI recovery plan for red metrics and preventive action for amber metrics.",
    },
    {
        "area": "Owner action cockpit",
        "question": "Who needs to do what today to improve Lead2Order performance?",
        "primaryMeasures": ["Action Required Count", "High Risk Lead Count", "SLA Breach Count"],
        "drilldowns": ["OwnerName", "CaseID", "CurrentStage", "RootCause"],
        "action": "Run daily action review by owner, severity, and value exposure.",
    },
]


REPORT_PAGES = [
    {
        "page": "Executive Lead2Order Overview",
        "purpose": "One-screen management view of funnel volume, pipeline value, conversion, SLA health, and action backlog.",
        "visuals": [
            {"type": "card", "title": "Lead Count", "measure": "Lead Count"},
            {"type": "card", "title": "Pipeline Value", "measure": "Pipeline Value"},
            {"type": "card", "title": "Order Conversion Rate", "measure": "Order Conversion Rate"},
            {"type": "card", "title": "SLA Breach Rate", "measure": "SLA Breach Rate"},
            {"type": "bar", "title": "Pipeline by Stage", "fields": ["CurrentStage", "Pipeline Value"]},
            {"type": "table", "title": "Top Action Cases", "fields": ["CaseID", "OwnerName", "CurrentStage", "PipelineValue", "RiskScore"]},
        ],
    },
    {
        "page": "Funnel Conversion",
        "purpose": "Explain stage conversion from raw lead to booked order.",
        "visuals": [
            {"type": "funnel", "title": "Lead Funnel", "measures": ["Lead Count", "MQL Count", "SQL Count", "Quote Count", "Order Count"]},
            {"type": "matrix", "title": "Conversion by Region and Owner", "fields": ["Region", "OwnerName"], "measures": ["MQL Rate", "SQL Rate", "Order Conversion Rate"]},
        ],
    },
    {
        "page": "Cycle Time and SLA",
        "purpose": "Find cycle-time delays, SLA breaches, and target variance.",
        "visuals": [
            {"type": "line", "title": "Cycle Days Trend", "fields": ["Period"], "measure": "Lead-to-Order Cycle Days"},
            {"type": "bar", "title": "SLA Breaches by Root Cause", "fields": ["RootCause"], "measure": "SLA Breach Count"},
            {"type": "scatter", "title": "Risk vs Pipeline Value", "fields": ["RiskScore", "PipelineValue", "OwnerName"]},
        ],
    },
    {
        "page": "Root Cause and Rework",
        "purpose": "Prioritize structural issues behind breaches, rework, and cost.",
        "visuals": [
            {"type": "matrix", "title": "Root Cause by Owner", "fields": ["RootCause", "OwnerName"], "measures": ["SLA Breach Count", "High Risk Pipeline Value"]},
            {"type": "bar", "title": "Rework by Event", "fields": ["EventName"], "measure": "Rework Event Count"},
            {"type": "bar", "title": "Event Cost by Source", "fields": ["SourceSystem"], "measure": "Total Event Cost"},
        ],
    },
    {
        "page": "Owner Action Cockpit",
        "purpose": "Turn findings into actionable queues for process owners and managers.",
        "visuals": [
            {"type": "table", "title": "Owner Action Queue", "fields": ["OwnerName", "CaseID", "CurrentStage", "RootCause", "PipelineValue", "RiskScore"]},
            {"type": "bar", "title": "Actions by Owner", "fields": ["OwnerName"], "measure": "Action Required Count"},
            {"type": "card", "title": "High Risk Pipeline", "measure": "High Risk Pipeline Value"},
        ],
    },
    {
        "page": "KPI Recovery Plan",
        "purpose": "Translate red and amber KPI periods into recovery actions.",
        "visuals": [
            {"type": "matrix", "title": "KPI Status by Period", "fields": ["KPIName", "Period", "Status"], "measures": ["Average KPI Gap"]},
            {"type": "card", "title": "Red KPI Periods", "measure": "KPI Red Count"},
            {"type": "card", "title": "Amber KPI Periods", "measure": "KPI Amber Count"},
        ],
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_process() -> dict:
    catalog = json.loads(PROCESS_CATALOG.read_text(encoding="utf-8"))
    for process in catalog["processes"]:
        if process["processId"] == "lead2order":
            return process
    raise ValueError("lead2order is missing from industry process catalog")


def dax_text() -> str:
    lines = [
        "-- Lead2Order analysis DAX catalog",
        "-- Generated for Process Owner, Process Manager, Data Analyst, and Power BI Designer replacement workflows.",
        "",
    ]
    for measure in MEASURES:
        lines.extend(
            [
                f"measure '{measure['name']}' =",
                f"\t{measure['expression']}",
                f"\tformatString: {measure['format']}",
                "",
            ]
        )
    return "\n".join(lines)


def patch_process_cases_tmdl() -> None:
    target = OUT_PBIP / "Lead2Order.SemanticModel" / "definition" / "tables" / "ProcessCases.tmdl"
    text = target.read_text(encoding="utf-8")
    marker = "\tpartition ProcessCases = m"
    before, after = text.split(marker, 1)
    existing = before.rstrip() + "\n\n"
    existing += "\n".join(f"\t{line}" if line else "" for line in dax_text().splitlines()[3:])
    target.write_text(existing.rstrip() + "\n\n" + marker + after, encoding="utf-8")


def build_package() -> dict:
    process = load_process()
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(RUNTIME_PBIP, OUT_PBIP)
    patch_process_cases_tmdl()

    manifest = {
        "eventType": "lead2order_powerbi_analysis_package",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "processId": process["processId"],
        "processName": process["name"],
        "ownerRole": process["ownerRole"],
        "sourceSystems": process["sourceSystems"],
        "kpiCount": len(process["kpis"]),
        "measureCount": len(MEASURES),
        "problemQuestionCount": len(PROBLEM_QUESTIONS),
        "reportPageCount": len(REPORT_PAGES),
        "pbipPath": "outputs/lead2order-powerbi-analysis/pbip/Lead2OrderAnalysis/Lead2Order.pbip",
        "semanticModelPath": "outputs/lead2order-powerbi-analysis/pbip/Lead2OrderAnalysis/Lead2Order.SemanticModel",
        "reportPath": "outputs/lead2order-powerbi-analysis/pbip/Lead2OrderAnalysis/Lead2Order.Report",
        "demoDataPath": "outputs/industry-demo-data/lead2order",
    }

    write_json(OUT_ROOT / "lead2order_powerbi_manifest.json", manifest)
    write_json(
        OUT_ROOT / "measure_catalog.json",
        {
            "processId": process["processId"],
            "processName": process["name"],
            "measures": MEASURES,
        },
    )
    write_json(
        OUT_ROOT / "kpi_problem_questions.json",
        {
            "processId": process["processId"],
            "processName": process["name"],
            "catalogKpis": process["kpis"],
            "problemQuestions": PROBLEM_QUESTIONS,
        },
    )
    write_json(
        OUT_ROOT / "report_blueprint.json",
        {
            "processId": process["processId"],
            "processName": process["name"],
            "pages": REPORT_PAGES,
        },
    )
    (OUT_ROOT / "dax_measures.dax").write_text(dax_text(), encoding="utf-8")
    (OUT_ROOT / "README.md").write_text(
        "# Lead2Order Power BI Analysis Package\n\n"
        "Concrete Power BI analysis package for the Lead2Order process owner. The package contains a PBIP "
        "project, a governed DAX measure catalog, KPI-to-problem-question mapping, and a report blueprint.\n\n"
        "## Contents\n\n"
        "- `pbip/Lead2OrderAnalysis/`: generated PBIP/PBIR/TMDL project using local demo CSV data.\n"
        "- `measure_catalog.json`: complete measure and KPI catalog with business questions and decisions.\n"
        "- `kpi_problem_questions.json`: process-owner questions mapped to measures, drilldowns, and actions.\n"
        "- `report_blueprint.json`: recommended pages and visuals for Power BI implementation.\n"
        "- `dax_measures.dax`: DAX catalog for review and copy into the semantic model.\n\n"
        "## Validation\n\n"
        "Run `python scripts\\powerbi_expert_factory.py validate --project outputs\\lead2order-powerbi-analysis\\pbip\\Lead2OrderAnalysis`.\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    manifest = build_package()
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
