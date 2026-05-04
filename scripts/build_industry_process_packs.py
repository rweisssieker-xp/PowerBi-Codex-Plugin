"""Generate Power BI process-pack specs for every industrial process."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
PACK_ROOT = ROOT / "outputs" / "industry-process-packs"
SOURCE_ROUTING_PATH = ROOT / "outputs" / "source-routing" / "process_source_routing.json"


def safe_measure_name(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value.strip())
    return cleaned.replace("%", "Pct")


def dax_for_kpi(kpi: str, value_column: str) -> str:
    measure_name = safe_measure_name(kpi)
    lower = kpi.lower()
    if "cycle" in lower or "aging" in lower or "time" in lower or "latency" in lower:
        expression = "AVERAGE('ProcessCases'[ActualCycleDays])"
    elif "%" in kpi or "rate" in lower or "adherence" in lower or "compliance" in lower or "accuracy" in lower:
        expression = "DIVIDE(CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[SlaBreached] = FALSE()), COUNTROWS('ProcessCases'))"
    elif "count" in lower or "volume" in lower or "loops" in lower or "breach" in lower:
        expression = "COUNTROWS('ProcessCases')"
    elif "risk" in lower or "score" in lower:
        expression = "AVERAGE('ProcessCases'[RiskScore])"
    else:
        expression = f"SUM('ProcessCases'[{value_column}])"
    return f"{measure_name} = {expression}"


def build_model_spec(process: dict[str, object], source_route: dict[str, object]) -> dict[str, object]:
    value_column = str(process["valueLabel"])
    return {
        "processId": process["processId"],
        "processName": process["name"],
        "grain": "One row per process case in ProcessCases; one row per lifecycle event in ProcessEvents; one row per KPI/month in ProcessKpiSnapshots.",
        "storageMode": "Import",
        "nativeSourcePattern": {
            "connector": "Folder.Files + Csv.Document",
            "demoPath": f"outputs/industry-demo-data/{process['processId']}",
            "productionRouting": "Replace CSV folder with validated native ERP/CRM/WMS/MES/QMS/EPM/Fabric connector according to source metadata.",
        },
        "productionSourceRouting": source_route.get("productionSourceRouting", []),
        "fallbackSourcePatterns": source_route.get("fallbackPatterns", []),
        "requiredSourceDecisions": source_route.get("requiredSourceDecisions", []),
        "tables": [
            {
                "name": "ProcessCases",
                "sourceFile": "cases.csv",
                "type": "fact",
                "key": "CaseID",
                "valueColumn": value_column,
                "columns": [
                    "ProcessID",
                    "ProcessName",
                    "CaseID",
                    "CaseName",
                    "Domain",
                    "OwnerRole",
                    "OwnerName",
                    "Region",
                    "PlantID",
                    "BusinessPartner",
                    "CurrentStage",
                    "StartDate",
                    "TargetDate",
                    "ActualOrForecastDate",
                    "TargetCycleDays",
                    "ActualCycleDays",
                    "SlaBreached",
                    "RootCause",
                    value_column,
                    "RiskScore",
                    "ActionRequired",
                ],
            },
            {
                "name": "ProcessEvents",
                "sourceFile": "events.csv",
                "type": "fact",
                "key": "CaseID|EventSequence",
                "columns": [
                    "ProcessID",
                    "ProcessName",
                    "CaseID",
                    "EventSequence",
                    "EventName",
                    "EventDate",
                    "SourceSystem",
                    "TouchedBy",
                    "AutomationFlag",
                    "ReworkFlag",
                    "EventCost",
                ],
            },
            {
                "name": "ProcessKpiSnapshots",
                "sourceFile": "kpi_snapshots.csv",
                "type": "fact",
                "key": "ProcessID|Period|KPIName",
                "columns": [
                    "ProcessID",
                    "ProcessName",
                    "Period",
                    "KPIName",
                    "ActualValue",
                    "TargetValue",
                    "Tolerance",
                    "Status",
                    "OwnerRole",
                    "SourceSystems",
                ],
            },
            {
                "name": "DimProcess",
                "type": "dimension",
                "columns": ["ProcessID", "ProcessName", "Domain", "OwnerRole"],
            },
            {
                "name": "DimCalendar",
                "type": "dimension",
                "columns": ["Date", "Year", "Quarter", "Month", "FiscalPeriod"],
            },
        ],
        "relationships": [
            {
                "fromTable": "ProcessEvents",
                "fromColumn": "CaseID",
                "toTable": "ProcessCases",
                "toColumn": "CaseID",
                "cardinality": "many-to-one",
                "crossFilter": "single",
                "active": True,
            },
            {
                "fromTable": "ProcessKpiSnapshots",
                "fromColumn": "ProcessID",
                "toTable": "DimProcess",
                "toColumn": "ProcessID",
                "cardinality": "many-to-one",
                "crossFilter": "single",
                "active": True,
            },
            {
                "fromTable": "ProcessCases",
                "fromColumn": "ProcessID",
                "toTable": "DimProcess",
                "toColumn": "ProcessID",
                "cardinality": "many-to-one",
                "crossFilter": "single",
                "active": True,
            },
        ],
        "rls": [
            {
                "role": "ProcessOwner",
                "table": "ProcessCases",
                "filter": "[OwnerRole] = USERPRINCIPALNAME() or [OwnerName] = USERPRINCIPALNAME()",
                "note": "Replace with enterprise identity mapping before production.",
            }
        ],
    }


def build_report_pages(process: dict[str, object]) -> dict[str, object]:
    return {
        "processId": process["processId"],
        "processName": process["name"],
        "pages": [
            {
                "name": "Executive Overview",
                "purpose": "Show KPI status, value at risk, SLA breach rate, and action backlog.",
                "visuals": ["KPI cards", "Status trend", "Value at risk bar", "Top exceptions table"],
                "requiredMeasures": [safe_measure_name(kpi) for kpi in process["kpis"][:4]],
            },
            {
                "name": "Process Flow And Aging",
                "purpose": "Explain stage progress, bottlenecks, rework, and cycle-time aging.",
                "visuals": ["Stage funnel", "Cycle-time histogram", "Event sequence matrix", "Aging heatmap"],
                "requiredFields": ["CurrentStage", "ActualCycleDays", "EventName", "EventDate"],
            },
            {
                "name": "Exception And Root Cause",
                "purpose": "Prioritize SLA breaches, root causes, and financial exposure.",
                "visuals": ["Root cause matrix", "Exception list", "Risk scatter", "Owner ranking"],
                "requiredFields": ["SlaBreached", "RootCause", "RiskScore", "OwnerName"],
            },
            {
                "name": "Owner Action Cockpit",
                "purpose": "Turn insights into accountable process actions.",
                "visuals": ["Action backlog", "Owner workload", "High-risk cases", "Drillthrough case detail"],
                "requiredFields": ["ActionRequired", "OwnerRole", "OwnerName", "CaseID"],
            },
        ],
    }


def build_quality_gate(process: dict[str, object]) -> dict[str, object]:
    return {
        "processId": process["processId"],
        "processName": process["name"],
        "requiredChecks": [
            "demo_data_files_exist",
            "model_spec_valid",
            "dax_measures_present",
            "report_pages_present",
            "quality_gate_present",
            "native_source_pattern_declared",
            "no_ambiguous_relationship_paths",
            "visual_bindings_resolvable",
            "kpi_owner_acceptance_required",
        ],
        "acceptanceCriteria": [
            "All process KPIs have a generated DAX measure or documented mapping.",
            "All report pages have purpose, visuals, and required measures or fields.",
            "Model relationships are many-to-one or explicitly documented.",
            "Demo source path uses CSV files and production path requires native connector routing.",
            "Generated artifacts contain no tenant secrets or customer-sensitive data.",
        ],
        "manualPowerBIDesktopChecks": [
            "Open generated PBIP/PBIR when available.",
            "Refresh all demo CSV sources.",
            "Confirm no Frown errors.",
            "Confirm visuals bind to existing fields/measures.",
        ],
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_process_pack(process: dict[str, object], source_route: dict[str, object]) -> dict[str, object]:
    process_id = str(process["processId"])
    folder = PACK_ROOT / process_id
    folder.mkdir(parents=True, exist_ok=True)

    value_column = str(process["valueLabel"])
    dax_lines = [
        f"-- {process['name']} generated DAX measure catalog",
        f"-- Demo value column: ProcessCases[{value_column}]",
        "",
        "Case Count = COUNTROWS('ProcessCases')",
        "SLA Breach Count = CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[SlaBreached] = TRUE())",
        "SLA Breach Rate = DIVIDE([SLA Breach Count], [Case Count])",
        "Action Required Count = CALCULATE(COUNTROWS('ProcessCases'), 'ProcessCases'[ActionRequired] = TRUE())",
        f"Total {value_column} = SUM('ProcessCases'[{value_column}])",
        "",
    ]
    dax_lines.extend(dax_for_kpi(kpi, value_column) for kpi in process["kpis"])
    dax_lines.append("")

    write_json(folder / "model_spec.json", build_model_spec(process, source_route))
    (folder / "dax_measures.dax").write_text("\n".join(dax_lines), encoding="utf-8")
    write_json(folder / "report_pages.json", build_report_pages(process))
    write_json(folder / "quality_gate.json", build_quality_gate(process))
    (folder / "README.md").write_text(
        f"# {process['name']} Process Pack\n\n"
        f"Generated process-pack specification for `{process_id}`.\n\n"
        "## Files\n\n"
        "- `model_spec.json`: semantic model, source pattern, relationships, and RLS notes.\n"
        "- `dax_measures.dax`: generated DAX measure catalog for the process KPIs.\n"
        "- `report_pages.json`: report page and visual specification.\n"
        "- `quality_gate.json`: validation and acceptance requirements.\n\n"
        f"Demo data: `../industry-demo-data/{process_id}/`.\n",
        encoding="utf-8",
    )

    return {
        "ProcessID": process_id,
        "ProcessName": process["name"],
        "ModelSpec": f"outputs/industry-process-packs/{process_id}/model_spec.json",
        "DaxMeasures": f"outputs/industry-process-packs/{process_id}/dax_measures.dax",
        "ReportPages": f"outputs/industry-process-packs/{process_id}/report_pages.json",
        "QualityGate": f"outputs/industry-process-packs/{process_id}/quality_gate.json",
    }


def write_index(rows: list[dict[str, object]]) -> None:
    PACK_ROOT.mkdir(parents=True, exist_ok=True)
    with (PACK_ROOT / "index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (PACK_ROOT / "README.md").write_text(
        "# Industry Process Packs\n\n"
        "Generated Power BI process-pack specifications for every process in "
        "`data/industry_process_catalog.json`.\n\n"
        "Each process folder contains `model_spec.json`, `dax_measures.dax`, "
        "`report_pages.json`, `quality_gate.json`, and a README.\n",
        encoding="utf-8",
    )


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    source_routes = {
        route["processId"]: route
        for route in json.loads(SOURCE_ROUTING_PATH.read_text(encoding="utf-8"))["routes"]
    }
    rows = [write_process_pack(process, source_routes[str(process["processId"])]) for process in catalog["processes"]]
    write_index(rows)
    print(f"generated {len(rows)} process packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
