"""Generate synthetic but realistic demo data for industrial process analytics.

The output is intentionally CSV-based so Power BI can load it through native
folder/file connectors without requiring proprietary source access.
"""

from __future__ import annotations

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
OUTPUT_ROOT = ROOT / "outputs" / "industry-demo-data"

PROCESS_CATALOG = [
    {
        "processId": "lead2order",
        "name": "Lead2Order",
        "domain": "Commercial",
        "ownerRole": "Lead-to-Order Process Owner",
        "caseName": "Lead",
        "valueLabel": "PipelineValue",
        "sourceSystems": ["CRM", "Marketing Automation", "CPQ", "ERP Sales"],
        "kpis": ["Lead Volume", "MQL Rate", "SQL Rate", "Order Conversion Rate", "Lead-to-Order Cycle Time", "Pipeline Value"],
        "stages": ["Lead Created", "Qualified", "Opportunity Created", "Quote Sent", "Order Booked"],
        "tables": ["Fact_Leads", "Fact_LeadStageHistory", "Fact_Opportunities", "Fact_Quotes", "Fact_Orders"],
    },
    {
        "processId": "order2cash",
        "name": "Order2Cash",
        "domain": "Commercial",
        "ownerRole": "Order-to-Cash Process Owner",
        "caseName": "Sales Order",
        "valueLabel": "OrderValue",
        "sourceSystems": ["ERP SD", "WMS", "TMS", "ERP FI-AR"],
        "kpis": ["Order Value", "Backlog Value", "OTIF %", "Billing Block Value", "Open AR", "DSO"],
        "stages": ["Order Created", "ATP Confirmed", "Delivered", "Billed", "Cash Collected"],
        "tables": ["Fact_SalesOrders", "Fact_Deliveries", "Fact_Billing", "Fact_AR", "Fact_Order2CashExceptions"],
    },
    {
        "processId": "source2contract",
        "name": "Source2Contract",
        "domain": "Procurement",
        "ownerRole": "Source-to-Contract Process Owner",
        "caseName": "Sourcing Event",
        "valueLabel": "ContractValue",
        "sourceSystems": ["Sourcing Suite", "CLM", "Supplier Portal", "ERP MM"],
        "kpis": ["Sourcing Cycle Time", "Contract Value At Risk", "Supplier Compliance %", "Legal Loop Count", "Savings Value"],
        "stages": ["Event Created", "RFx Published", "Supplier Selected", "Legal Review", "Contract Signed"],
        "tables": ["Fact_SourcingEvents", "Fact_Contracts", "Fact_SupplierRisk", "Fact_Source2ContractExceptions"],
    },
    {
        "processId": "procure2pay",
        "name": "Procure2Pay",
        "domain": "Procurement",
        "ownerRole": "Procure-to-Pay Process Owner",
        "caseName": "Purchase Order",
        "valueLabel": "SpendValue",
        "sourceSystems": ["ERP MM", "Supplier Portal", "WMS", "ERP FI-AP"],
        "kpis": ["Spend Value", "Invoice Block Value", "GR/IR Aging", "Discount Capture %", "Supplier On-Time %"],
        "stages": ["Requisition Approved", "PO Created", "Goods Received", "Invoice Posted", "Paid"],
        "tables": ["Fact_Requisitions", "Fact_PurchaseOrders", "Fact_GoodsReceipts", "Fact_Invoices", "Fact_Payments"],
    },
    {
        "processId": "forecast2plan",
        "name": "Forecast2Plan",
        "domain": "Supply Chain",
        "ownerRole": "Demand Planning Process Owner",
        "caseName": "Planning Item",
        "valueLabel": "ForecastValue",
        "sourceSystems": ["Demand Planning", "IBP", "ERP PP", "Data Warehouse"],
        "kpis": ["Forecast Accuracy", "Forecast Bias", "S&OP Gap", "Inventory Target Gap", "Demand Volatility"],
        "stages": ["Demand Signal Captured", "Baseline Forecast", "Consensus Forecast", "S&OP Approved", "Plan Released"],
        "tables": ["Fact_DemandSignals", "Fact_Forecasts", "Fact_InventoryTargets", "Fact_PlanGaps"],
    },
    {
        "processId": "plan2produce",
        "name": "Plan2Produce",
        "domain": "Manufacturing",
        "ownerRole": "Plan-to-Produce Process Owner",
        "caseName": "Production Order",
        "valueLabel": "ProductionValue",
        "sourceSystems": ["ERP PP", "MES", "QMS", "Historian"],
        "kpis": ["Schedule Adherence", "Yield %", "Scrap Value", "Capacity Utilization", "Production Variance"],
        "stages": ["Order Released", "Materials Staged", "Production Started", "Quality Checked", "Order Confirmed"],
        "tables": ["Fact_ProductionOrders", "Fact_Operations", "Fact_Yield", "Fact_Scrap", "Fact_Capacity"],
    },
    {
        "processId": "make_strategy",
        "name": "Make2Stock / Make2Order / Engineer2Order",
        "domain": "Manufacturing",
        "ownerRole": "Manufacturing Strategy Process Owner",
        "caseName": "Manufacturing Commitment",
        "valueLabel": "CommitmentValue",
        "sourceSystems": ["ERP PP", "PLM", "MES", "APS"],
        "kpis": ["Lead Time", "WIP Value", "Stock Cover", "Milestone Adherence", "Expedite Count"],
        "stages": ["Demand Assigned", "Strategy Selected", "Material Checked", "Build Started", "Customer Commitment Met"],
        "tables": ["Fact_MakeStrategyCases", "Fact_WIP", "Fact_Milestones", "Fact_InventoryCover"],
    },
    {
        "processId": "idea2launch",
        "name": "Idea2Launch / Engineer2Release",
        "domain": "Engineering",
        "ownerRole": "Product Lifecycle Process Owner",
        "caseName": "Product Initiative",
        "valueLabel": "LaunchValue",
        "sourceSystems": ["PLM", "PPM", "QMS", "ERP Engineering"],
        "kpis": ["Gate Adherence", "Change Backlog", "Launch Risk", "Ramp-Up Readiness", "Engineering Cycle Time"],
        "stages": ["Idea Logged", "Concept Approved", "Design Frozen", "Release Approved", "Launch Ready"],
        "tables": ["Fact_ProductInitiatives", "Fact_EngineeringChanges", "Fact_Gates", "Fact_LaunchReadiness"],
    },
    {
        "processId": "maintain2operate",
        "name": "Maintain2Operate",
        "domain": "Maintenance",
        "ownerRole": "Maintenance Process Owner",
        "caseName": "Work Order",
        "valueLabel": "DowntimeCost",
        "sourceSystems": ["EAM", "CMMS", "MES", "Historian"],
        "kpis": ["PM Compliance", "Downtime Cost", "MTBF", "MTTR", "Maintenance Backlog"],
        "stages": ["Notification Created", "Work Order Planned", "Parts Available", "Work Completed", "Asset Released"],
        "tables": ["Fact_WorkOrders", "Fact_AssetDowntime", "Fact_PreventiveMaintenance", "Fact_MaintenanceBacklog"],
    },
    {
        "processId": "issue2resolution",
        "name": "Issue2Resolution",
        "domain": "Service",
        "ownerRole": "Issue Resolution Process Owner",
        "caseName": "Customer Issue",
        "valueLabel": "IssueCost",
        "sourceSystems": ["CRM Service", "Warranty", "QMS", "Field Service"],
        "kpis": ["Issue Aging", "SLA Breach %", "Warranty Cost", "Repeat Issue Rate", "Corrective Action Aging"],
        "stages": ["Issue Logged", "Triaged", "Root Cause Assigned", "Corrective Action Created", "Resolved"],
        "tables": ["Fact_CustomerIssues", "Fact_WarrantyClaims", "Fact_CorrectiveActions", "Fact_IssueResolution"],
    },
    {
        "processId": "record2report",
        "name": "Record2Report",
        "domain": "Finance",
        "ownerRole": "Record-to-Report Process Owner",
        "caseName": "Close Task",
        "valueLabel": "FinancialImpact",
        "sourceSystems": ["ERP FI/CO", "EPM", "Consolidation", "GRC"],
        "kpis": ["Close Cycle Time", "Late Posting Count", "Reconciliation Breaks", "Journal Error Rate", "Audit Finding Count"],
        "stages": ["Subledger Closed", "Journal Posted", "Reconciled", "Consolidated", "Reported"],
        "tables": ["Fact_CloseTasks", "Fact_Journals", "Fact_Reconciliations", "Fact_Controls"],
    },
    {
        "processId": "hire2retire",
        "name": "Hire2Retire",
        "domain": "Workforce",
        "ownerRole": "Hire-to-Retire Process Owner",
        "caseName": "Employee Lifecycle Case",
        "valueLabel": "WorkforceCost",
        "sourceSystems": ["HCM", "Time Management", "Learning", "EHS"],
        "kpis": ["Time To Hire", "Absence Rate", "Skill Gap", "Training Compliance", "Safety Incident Rate"],
        "stages": ["Requisition Opened", "Candidate Hired", "Onboarded", "Trained", "Role Changed"],
        "tables": ["Fact_Recruiting", "Fact_Workforce", "Fact_Absence", "Fact_Training", "Fact_Safety"],
    },
    {
        "processId": "market2lead",
        "name": "Market2Lead",
        "domain": "Commercial",
        "ownerRole": "Marketing Process Owner",
        "caseName": "Campaign Lead",
        "valueLabel": "CampaignSpend",
        "sourceSystems": ["Marketing Automation", "CRM", "Web Analytics", "Ad Platforms"],
        "kpis": ["Campaign ROI", "MQL Conversion", "CAC", "Lead Velocity", "Qualified Pipeline"],
        "stages": ["Campaign Launched", "Lead Captured", "MQL Scored", "SQL Accepted", "Opportunity Created"],
        "tables": ["Fact_Campaigns", "Fact_Leads", "Fact_ChannelSpend", "Fact_MarketingAttribution"],
    },
    {
        "processId": "lead2quote",
        "name": "Lead2Quote / Configure2Quote",
        "domain": "Commercial",
        "ownerRole": "Quote Process Owner",
        "caseName": "Quote",
        "valueLabel": "QuoteValue",
        "sourceSystems": ["CRM", "CPQ", "Pricing", "ERP Sales"],
        "kpis": ["Quote Cycle Time", "Configuration Error Rate", "Approval Aging", "Discount Leakage", "Quote Win Rate"],
        "stages": ["Need Captured", "Configured", "Priced", "Approved", "Quote Sent"],
        "tables": ["Fact_Quotes", "Fact_Configurations", "Fact_Approvals", "Fact_Discounts"],
    },
    {
        "processId": "quote2contract",
        "name": "Quote2Contract",
        "domain": "Commercial",
        "ownerRole": "Quote-to-Contract Process Owner",
        "caseName": "Contract",
        "valueLabel": "ContractValue",
        "sourceSystems": ["CRM", "CPQ", "CLM", "E-Signature"],
        "kpis": ["Contract Cycle Time", "Redline Loops", "Term Deviation Count", "Value At Risk", "Signature Aging"],
        "stages": ["Quote Accepted", "Draft Created", "Legal Review", "Customer Redline", "Signed"],
        "tables": ["Fact_Contracts", "Fact_Redlines", "Fact_TermDeviations", "Fact_Signatures"],
    },
    {
        "processId": "contract2revenue",
        "name": "Contract2Revenue",
        "domain": "Finance",
        "ownerRole": "Revenue Process Owner",
        "caseName": "Revenue Contract",
        "valueLabel": "RevenueValue",
        "sourceSystems": ["CLM", "ERP SD", "Billing", "Revenue Recognition"],
        "kpis": ["Billing Readiness", "Revenue Leakage", "Deferred Revenue", "Renewal Risk", "Missing Billing Data"],
        "stages": ["Contract Effective", "Billing Data Complete", "Fulfilled", "Billed", "Revenue Recognized"],
        "tables": ["Fact_RevenueContracts", "Fact_BillingReadiness", "Fact_RevenueRecognition", "Fact_Renewals"],
    },
    {
        "processId": "demand2supply",
        "name": "Demand2Supply",
        "domain": "Supply Chain",
        "ownerRole": "Demand-to-Supply Process Owner",
        "caseName": "Demand-Supply Match",
        "valueLabel": "ShortageValue",
        "sourceSystems": ["Demand Planning", "ERP ATP", "APS", "Inventory"],
        "kpis": ["Shortage Value", "ATP Failure Rate", "Lost Sales", "Supply Gap", "Allocation Aging"],
        "stages": ["Demand Captured", "ATP Checked", "Supply Matched", "Allocated", "Committed"],
        "tables": ["Fact_Demand", "Fact_ATP", "Fact_Supply", "Fact_Shortages", "Fact_Allocations"],
    },
    {
        "processId": "sop_ibp2execution",
        "name": "S&OP / IBP2Execution",
        "domain": "Supply Chain",
        "ownerRole": "IBP Process Owner",
        "caseName": "Plan Commitment",
        "valueLabel": "PlanGapValue",
        "sourceSystems": ["IBP", "ERP PP", "MES", "Inventory"],
        "kpis": ["Plan Adherence", "Constrained Gap", "Capacity Overload", "Inventory Target Adherence", "Plan Change Count"],
        "stages": ["Plan Approved", "Constraint Published", "Execution Released", "Progress Reviewed", "Variance Closed"],
        "tables": ["Fact_Plans", "Fact_Constraints", "Fact_Execution", "Fact_PlanVariance"],
    },
    {
        "processId": "design2cost",
        "name": "Design2Cost / Design2Source",
        "domain": "Engineering",
        "ownerRole": "Design-to-Cost Process Owner",
        "caseName": "Design Item",
        "valueLabel": "CostVariance",
        "sourceSystems": ["PLM", "Costing", "Sourcing", "ERP MM"],
        "kpis": ["Target Cost Variance", "Part Reuse %", "Single-Source Exposure", "Sourcing Readiness", "Engineering Cost Risk"],
        "stages": ["Concept Created", "BOM Estimated", "Supplier Checked", "Cost Reviewed", "Design Released"],
        "tables": ["Fact_DesignItems", "Fact_TargetCosts", "Fact_SourcingReadiness", "Fact_PartReuse"],
    },
    {
        "processId": "project2cash",
        "name": "Engineer2Order / Project2Cash",
        "domain": "Projects",
        "ownerRole": "Project-to-Cash Process Owner",
        "caseName": "Customer Project",
        "valueLabel": "ProjectValue",
        "sourceSystems": ["Project System", "ERP CO", "Billing", "PLM"],
        "kpis": ["Milestone Adherence", "Project Margin", "WIP Value", "Billing Readiness", "Cash Exposure"],
        "stages": ["Project Created", "Engineering Released", "Milestone Achieved", "Billed", "Cash Collected"],
        "tables": ["Fact_Projects", "Fact_Milestones", "Fact_ProjectMargin", "Fact_ProjectBilling"],
    },
    {
        "processId": "dock2stock",
        "name": "Dock2Stock",
        "domain": "Warehouse",
        "ownerRole": "Inbound Warehouse Process Owner",
        "caseName": "Inbound Receipt",
        "valueLabel": "InboundValue",
        "sourceSystems": ["WMS", "ERP MM", "QMS", "Yard Management"],
        "kpis": ["Dock-to-Stock Time", "GR Accuracy", "Inspection Aging", "Putaway Backlog", "Blocked Stock Value"],
        "stages": ["ASN Received", "Truck Arrived", "Goods Received", "Quality Released", "Putaway Complete"],
        "tables": ["Fact_ASN", "Fact_GoodsReceipts", "Fact_Inspection", "Fact_Putaway", "Fact_BlockedStock"],
    },
    {
        "processId": "pick2pack2ship",
        "name": "Pick2Pack2Ship",
        "domain": "Warehouse",
        "ownerRole": "Outbound Warehouse Process Owner",
        "caseName": "Shipment",
        "valueLabel": "ShipmentValue",
        "sourceSystems": ["WMS", "ERP SD", "TMS", "Carrier Portal"],
        "kpis": ["Pick Accuracy", "Lines Per Hour", "Wave Adherence", "Pack Backlog", "Cut-Off Misses"],
        "stages": ["Wave Released", "Picked", "Packed", "Staged", "Shipped"],
        "tables": ["Fact_Waves", "Fact_Picks", "Fact_Packs", "Fact_Shipments"],
    },
    {
        "processId": "return2disposition",
        "name": "Return2Disposition",
        "domain": "Service",
        "ownerRole": "Returns Process Owner",
        "caseName": "Return",
        "valueLabel": "RecoveryValue",
        "sourceSystems": ["RMA", "WMS", "QMS", "ERP SD"],
        "kpis": ["Return Rate", "Disposition Aging", "Recovery Value", "Scrap Rate", "Resale Rate"],
        "stages": ["Return Authorized", "Received", "Inspected", "Disposition Decided", "Value Recovered"],
        "tables": ["Fact_Returns", "Fact_Inspections", "Fact_Dispositions", "Fact_Recovery"],
    },
    {
        "processId": "complaint2capa",
        "name": "Complaint2CAPA",
        "domain": "Quality",
        "ownerRole": "Complaint-to-CAPA Process Owner",
        "caseName": "Complaint",
        "valueLabel": "QualityCost",
        "sourceSystems": ["QMS", "CRM Service", "Warranty", "ERP QM"],
        "kpis": ["Complaint Rate", "CAPA Aging", "Repeat Defect Rate", "Cost Of Poor Quality", "CAPA Effectiveness"],
        "stages": ["Complaint Logged", "Investigation Opened", "Root Cause Confirmed", "CAPA Assigned", "Effectiveness Checked"],
        "tables": ["Fact_Complaints", "Fact_CAPA", "Fact_Defects", "Fact_QualityCost"],
    },
    {
        "processId": "nonconformance2disposition",
        "name": "Nonconformance2Disposition",
        "domain": "Quality",
        "ownerRole": "Nonconformance Process Owner",
        "caseName": "Nonconformance",
        "valueLabel": "BlockedValue",
        "sourceSystems": ["QMS", "ERP QM", "WMS", "Supplier Portal"],
        "kpis": ["Defect Rate", "Blocked Stock Value", "Rework Cost", "Supplier PPM", "Disposition Aging"],
        "stages": ["Defect Logged", "Stock Blocked", "Review Board", "Disposition Decided", "Released Or Scrapped"],
        "tables": ["Fact_Nonconformance", "Fact_BlockedStock", "Fact_Rework", "Fact_SupplierQuality"],
    },
    {
        "processId": "incident2action",
        "name": "Incident2Action",
        "domain": "EHS",
        "ownerRole": "Incident-to-Action Process Owner",
        "caseName": "Incident",
        "valueLabel": "RiskValue",
        "sourceSystems": ["EHS", "GRC", "Action Tracking", "HR"],
        "kpis": ["Incident Rate", "Severity Score", "Response Time", "Overdue Actions", "Risk Exposure"],
        "stages": ["Incident Reported", "Triage Complete", "Investigation Complete", "Action Assigned", "Action Closed"],
        "tables": ["Fact_Incidents", "Fact_EHSActions", "Fact_RiskAssessments", "Fact_ActionAging"],
    },
    {
        "processId": "asset2reliability",
        "name": "Asset2Reliability",
        "domain": "Maintenance",
        "ownerRole": "Asset Reliability Process Owner",
        "caseName": "Asset Reliability Case",
        "valueLabel": "DowntimeCost",
        "sourceSystems": ["EAM", "MES", "Historian", "CMMS"],
        "kpis": ["OEE", "MTBF", "MTTR", "Downtime Cost", "PM Compliance"],
        "stages": ["Asset Monitored", "Failure Detected", "Work Planned", "Repair Complete", "Reliability Reviewed"],
        "tables": ["Fact_AssetPerformance", "Fact_Downtime", "Fact_Reliability", "Fact_PMCompliance"],
    },
    {
        "processId": "installedbase2servicerevenue",
        "name": "InstalledBase2ServiceRevenue",
        "domain": "Service",
        "ownerRole": "Installed Base Service Process Owner",
        "caseName": "Installed Base Account",
        "valueLabel": "ServiceRevenue",
        "sourceSystems": ["Installed Base", "CRM Service", "FSM", "Billing"],
        "kpis": ["Attach Rate", "SLA Adherence", "Service Margin", "Renewal Opportunity", "Coverage Gap"],
        "stages": ["Asset Installed", "Contract Offered", "Service Delivered", "Renewal Proposed", "Revenue Captured"],
        "tables": ["Fact_InstalledBase", "Fact_ServiceContracts", "Fact_FieldService", "Fact_ServiceRevenue"],
    },
    {
        "processId": "supplieronboarding2risk",
        "name": "SupplierOnboarding2Risk",
        "domain": "Procurement",
        "ownerRole": "Supplier Risk Process Owner",
        "caseName": "Supplier Onboarding",
        "valueLabel": "RiskExposure",
        "sourceSystems": ["Supplier Portal", "GRC", "Sourcing", "ERP Vendor Master"],
        "kpis": ["Qualification Status", "Audit Score", "ESG Risk", "Onboarding Aging", "Supplier Risk Exposure"],
        "stages": ["Supplier Invited", "Documents Submitted", "Audit Completed", "Risk Approved", "Supplier Activated"],
        "tables": ["Fact_SupplierOnboarding", "Fact_Audits", "Fact_ESGRisk", "Fact_SupplierRisk"],
    },
    {
        "processId": "control2evidence",
        "name": "Control2Evidence",
        "domain": "Governance",
        "ownerRole": "Control-to-Evidence Process Owner",
        "caseName": "Control",
        "valueLabel": "ControlRiskValue",
        "sourceSystems": ["GRC", "ERP", "IAM", "Audit Management"],
        "kpis": ["Control Effectiveness", "Evidence Coverage", "SoD Violations", "Remediation Aging", "Audit Gap Count"],
        "stages": ["Control Defined", "Evidence Requested", "Evidence Collected", "Tested", "Remediated"],
        "tables": ["Fact_Controls", "Fact_Evidence", "Fact_SoDViolations", "Fact_Remediation"],
    },
    {
        "processId": "close2report_plan2perform",
        "name": "Close2Report / Plan2Perform",
        "domain": "Finance",
        "ownerRole": "Close and Planning Process Owner",
        "caseName": "Close Or Plan Cycle",
        "valueLabel": "VarianceValue",
        "sourceSystems": ["ERP FI/CO", "EPM", "Planning", "Consolidation"],
        "kpis": ["Close Cycle", "Late Postings", "Reconciliation Breaks", "Forecast Variance", "Planning Assumption Drift"],
        "stages": ["Cycle Opened", "Data Loaded", "Reviewed", "Approved", "Reported"],
        "tables": ["Fact_CloseCycles", "Fact_Planning", "Fact_ForecastVariance", "Fact_Reconciliation"],
    },
    {
        "processId": "data2insight2action",
        "name": "Data2Insight2Action",
        "domain": "Analytics",
        "ownerRole": "Data-to-Action Process Owner",
        "caseName": "Insight",
        "valueLabel": "RealizedValue",
        "sourceSystems": ["Power BI", "Action Tracker", "Data Catalog", "Business Apps"],
        "kpis": ["Insight Adoption", "Action Conversion", "Decision Latency", "Realized Value", "Action Overdue Count"],
        "stages": ["Insight Generated", "Owner Assigned", "Action Created", "Decision Made", "Value Realized"],
        "tables": ["Fact_Insights", "Fact_Actions", "Fact_Decisions", "Fact_ValueRealization"],
    },
]


OWNERS = ["Alex Chen", "Maria Garcia", "Priya Rao", "Thomas Weber", "Nina Patel", "Jon Miller", "Sara Novak", "Kenji Tanaka"]
REGIONS = ["EMEA", "AMER", "APAC"]
PLANTS = ["DE10", "DE20", "US10", "SG10", "PL10"]
CUSTOMERS = ["Apex Industries", "Global Components", "Nova Mobility", "Atlas Systems", "Orion Technologies"]
SUPPLIERS = ["Meyer Metals", "Summit Supply", "Pacific Electronics", "Euro Logistics", "Zenith Precision"]
CAUSES = ["Missing master data", "Capacity constraint", "Approval delay", "Quality hold", "Supplier delay", "Pricing exception", "System integration gap"]


def slug(value: str) -> str:
    return value.lower().replace(" ", "_").replace("/", "_").replace("&", "and").replace("-", "_")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def money(rng: random.Random, low: int, high: int) -> float:
    return round(rng.uniform(low, high), 2)


def make_cases(process: dict[str, object], rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    base_date = date(2025, 1, 1)
    stages = process["stages"]
    for idx in range(1, 37):
        start = base_date + timedelta(days=rng.randint(0, 450))
        current_stage = rng.choice(stages)
        target_days = rng.choice([3, 5, 7, 10, 14, 21, 30])
        actual_days = max(1, int(rng.gauss(target_days * 1.15, max(1, target_days / 2))))
        rows.append(
            {
                "ProcessID": process["processId"],
                "ProcessName": process["name"],
                "CaseID": f"{str(process['processId']).upper()}-{idx:05d}",
                "CaseName": process["caseName"],
                "Domain": process["domain"],
                "OwnerRole": process["ownerRole"],
                "OwnerName": rng.choice(OWNERS),
                "Region": rng.choice(REGIONS),
                "PlantID": rng.choice(PLANTS),
                "BusinessPartner": rng.choice(CUSTOMERS if process["domain"] in ["Commercial", "Service"] else SUPPLIERS),
                "CurrentStage": current_stage,
                "StartDate": start.isoformat(),
                "TargetDate": (start + timedelta(days=target_days)).isoformat(),
                "ActualOrForecastDate": (start + timedelta(days=actual_days)).isoformat(),
                "TargetCycleDays": target_days,
                "ActualCycleDays": actual_days,
                "SlaBreached": actual_days > target_days,
                "RootCause": rng.choice(CAUSES) if actual_days > target_days or rng.random() < 0.25 else "",
                str(process["valueLabel"]): money(rng, 5000, 750000),
                "RiskScore": rng.randint(5, 100),
                "ActionRequired": actual_days > target_days or rng.random() < 0.18,
            }
        )
    return rows


def make_events(process: dict[str, object], cases: list[dict[str, object]], rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    stages = list(process["stages"])
    for case in cases:
        current_date = date.fromisoformat(str(case["StartDate"]))
        for sequence, stage in enumerate(stages, start=1):
            current_date += timedelta(days=rng.randint(0, 6))
            rows.append(
                {
                    "ProcessID": process["processId"],
                    "ProcessName": process["name"],
                    "CaseID": case["CaseID"],
                    "EventSequence": sequence,
                    "EventName": stage,
                    "EventDate": current_date.isoformat(),
                    "SourceSystem": rng.choice(process["sourceSystems"]),
                    "TouchedBy": rng.choice(OWNERS),
                    "AutomationFlag": rng.random() > 0.45,
                    "ReworkFlag": rng.random() < 0.12,
                    "EventCost": money(rng, 50, 8000),
                }
            )
    return rows


def make_kpi_snapshots(process: dict[str, object], cases: list[dict[str, object]], rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    periods = [f"2025-{month:02d}" for month in range(1, 13)]
    breached = sum(1 for case in cases if case["SlaBreached"])
    breach_rate = breached / len(cases)
    for period in periods:
        for kpi in process["kpis"]:
            target = round(rng.uniform(75, 98), 2) if "%" in kpi or "Rate" in kpi else round(rng.uniform(10, 60), 2)
            actual = round(target * rng.uniform(0.82, 1.08) - breach_rate * rng.uniform(1, 8), 2)
            rows.append(
                {
                    "ProcessID": process["processId"],
                    "ProcessName": process["name"],
                    "Period": period,
                    "KPIName": kpi,
                    "ActualValue": actual,
                    "TargetValue": target,
                    "Tolerance": round(target * 0.05, 2),
                    "Status": "Red" if actual < target * 0.9 else "Amber" if actual < target else "Green",
                    "OwnerRole": process["ownerRole"],
                    "SourceSystems": "; ".join(process["sourceSystems"]),
                }
            )
    return rows


def build_catalog() -> None:
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "1.0",
        "description": "Industrial process catalog for Power BI Expert-Replacement Factory demo data and process-pack coverage.",
        "processCount": len(PROCESS_CATALOG),
        "processes": PROCESS_CATALOG,
    }
    CATALOG_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_demo_data() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    index_rows: list[dict[str, object]] = []
    for process in PROCESS_CATALOG:
        rng = random.Random(str(process["processId"]))
        folder = OUTPUT_ROOT / str(process["processId"])
        cases = make_cases(process, rng)
        events = make_events(process, cases, rng)
        kpis = make_kpi_snapshots(process, cases, rng)
        write_csv(folder / "cases.csv", cases)
        write_csv(folder / "events.csv", events)
        write_csv(folder / "kpi_snapshots.csv", kpis)
        index_rows.append(
            {
                "ProcessID": process["processId"],
                "ProcessName": process["name"],
                "Domain": process["domain"],
                "OwnerRole": process["ownerRole"],
                "CaseRows": len(cases),
                "EventRows": len(events),
                "KpiRows": len(kpis),
                "Folder": f"outputs/industry-demo-data/{process['processId']}",
            }
        )
    write_csv(OUTPUT_ROOT / "index.csv", index_rows)
    (OUTPUT_ROOT / "README.md").write_text(
        "# Industry Demo Data\n\n"
        "Synthetic demo data for all industrial process chains in `data/industry_process_catalog.json`.\n\n"
        "Each process folder contains:\n\n"
        "- `cases.csv`: case-level process records.\n"
        "- `events.csv`: process event log for cycle-time and bottleneck analytics.\n"
        "- `kpi_snapshots.csv`: monthly KPI target/actual/status snapshots.\n\n"
        "The files are designed for native Power BI file/folder ingestion and contain no customer-sensitive data.\n",
        encoding="utf-8",
    )


def main() -> int:
    build_catalog()
    build_demo_data()
    print(f"generated {len(PROCESS_CATALOG)} process demo datasets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
