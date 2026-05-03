#!/usr/bin/env python3
"""Generate a PBIP/TMDL-ready Order2Cash project scaffold."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_PACK = ROOT / "outputs" / "powerbi-order2cash-test"
OUT_DIR = ROOT / "outputs" / "powerbi-order2cash-pbip" / "Order2Cash"
SOURCE_XLSX = ROOT / "outputs" / "powerbi-industrial-demo" / "powerbi_industrial_demo_data.xlsx"


TABLES = [
    "Dim_Calendar",
    "Dim_Customer",
    "Dim_Product",
    "Dim_Plant",
    "Dim_Warehouse",
    "Fact_Leads",
    "Fact_Opportunities",
    "Fact_Quotes",
    "Fact_SalesOrders",
    "Fact_Deliveries",
    "Fact_Billing",
    "Fact_AR",
    "Fact_ServiceTickets",
    "Fact_Shipments",
    "Fact_GL_Postings",
    "Fact_Order2CashExceptions",
]


COLUMNS = {
    "Dim_Customer": ["CustomerID", "CustomerName", "Segment", "Industry", "Country", "SalesRegion", "RiskClass", "ActiveFlag"],
    "Dim_Product": ["ProductID", "ProductName", "ProductFamily", "ProductLine", "LifecycleStatus", "StandardCost", "ListPrice"],
    "Dim_Calendar": ["Date", "Year", "Quarter", "MonthNo", "MonthName", "FiscalYear", "FiscalPeriod", "IsWorkingDay"],
    "Dim_Plant": ["PlantID", "CompanyCode", "PlantName", "Country", "IndustryFocus"],
    "Dim_Warehouse": ["WarehouseID", "PlantID", "WarehouseType", "WarehouseName"],
    "Fact_SalesOrders": ["SalesOrderID", "QuoteID", "CustomerID", "ProductID", "PlantID", "OrderDate", "RequestedDate", "ConfirmedDate", "OrderQty", "NetPrice", "OrderValue", "Status", "ATPStatus"],
    "Fact_Deliveries": ["DeliveryID", "SalesOrderID", "CustomerID", "ProductID", "WarehouseID", "PickDate", "ShipDate", "DeliveryDate", "DeliveredQty", "OTIFStatus", "Carrier"],
    "Fact_Billing": ["InvoiceID", "DeliveryID", "SalesOrderID", "CustomerID", "InvoiceDate", "DueDate", "InvoiceAmount", "TaxAmount", "BillingBlockFlag"],
    "Fact_AR": ["InvoiceID", "CustomerID", "DueDate", "OpenAmount", "PaymentDate", "DisputeFlag", "DunningLevel"],
    "Fact_Quotes": ["QuoteID", "OpportunityID", "CustomerID", "QuoteDate", "QuoteStatus", "QuoteValue", "DiscountPct", "ApprovalCycleDays", "LegalLoopCount"],
    "Fact_Order2CashExceptions": ["ExceptionID", "ProblemType", "Severity", "CustomerID", "ProductID", "RelatedDocument", "EventDate", "AmountExposure", "Reason", "RecommendedAction", "OwnerRole"],
}


RELATIONSHIPS = [
    ("Fact_SalesOrders", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_SalesOrders", "ProductID", "Dim_Product", "ProductID"),
    ("Fact_SalesOrders", "PlantID", "Dim_Plant", "PlantID"),
    ("Fact_Deliveries", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_Deliveries", "ProductID", "Dim_Product", "ProductID"),
    ("Fact_Deliveries", "WarehouseID", "Dim_Warehouse", "WarehouseID"),
    ("Fact_Billing", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_AR", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_Quotes", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_Order2CashExceptions", "CustomerID", "Dim_Customer", "CustomerID"),
    ("Fact_Order2CashExceptions", "ProductID", "Dim_Product", "ProductID"),
]


PAGE_SPECS = [
    {
        "name": "p01_o2c_overview",
        "displayName": "O2C Executive Overview",
        "visuals": [
            ("v01_order_value", "card", "Order Value", "_Measures", "Order Value", 24, 24, 210, 110),
            ("v02_backlog", "card", "Open Backlog Value", "_Measures", "Open Backlog Value", 250, 24, 210, 110),
            ("v03_exception_count", "card", "O2C Exception Count", "_Measures", "O2C Exception Count", 476, 24, 210, 110),
            ("v04_exception_exposure", "card", "O2C Exception Exposure", "_Measures", "O2C Exception Exposure", 702, 24, 240, 110),
            ("v05_problem_mix", "clusteredBarChart", "Exceptions by problem type", "Fact_Order2CashExceptions", "ProblemType", 24, 170, 440, 300),
            ("v06_action_backlog", "tableEx", "Top O2C exception backlog", "Fact_Order2CashExceptions", "AmountExposure", 490, 170, 650, 300),
        ],
    },
    {
        "name": "p02_customer_churn",
        "displayName": "Customer Churn and Retention Risk",
        "visuals": [
            ("v01_churn_customers", "card", "Churn Risk Customers", "_Measures", "Churn Risk Customers", 24, 24, 220, 110),
            ("v02_customer_score", "tableEx", "Customer risk score detail", "Fact_Order2CashExceptions", "CustomerID", 24, 160, 620, 330),
            ("v03_customer_revenue", "clusteredBarChart", "High exposure churn customers", "Fact_Order2CashExceptions", "AmountExposure", 670, 160, 470, 330),
        ],
    },
    {
        "name": "p03_order_backlog",
        "displayName": "Order Intake and Backlog",
        "visuals": [
            ("v01_order_count", "card", "Order Count", "_Measures", "Order Count", 24, 24, 220, 110),
            ("v02_atp_rate", "card", "ATP Issue Rate", "_Measures", "ATP Issue Rate", 260, 24, 220, 110),
            ("v03_order_status", "clusteredColumnChart", "Order status and ATP", "Fact_SalesOrders", "Status", 24, 160, 540, 320),
            ("v04_backlog_table", "tableEx", "Backlog exceptions", "Fact_Order2CashExceptions", "RelatedDocument", 590, 160, 550, 320),
        ],
    },
    {
        "name": "p04_delivery_otif",
        "displayName": "Delivery and OTIF",
        "visuals": [
            ("v01_delivery_rate", "card", "Late Or Short Delivery Rate", "_Measures", "Late Or Short Delivery Rate", 24, 24, 260, 110),
            ("v02_late_count", "card", "Late Or Short Deliveries", "_Measures", "Late Or Short Deliveries", 300, 24, 230, 110),
            ("v03_carrier_otif", "clusteredBarChart", "Carrier and delivery exceptions", "Fact_Deliveries", "Carrier", 24, 160, 540, 320),
            ("v04_otif_backlog", "tableEx", "Late/short action backlog", "Fact_Order2CashExceptions", "ProblemType", 590, 160, 550, 320),
        ],
    },
    {
        "name": "p05_billing_cash",
        "displayName": "Billing and Cash",
        "visuals": [
            ("v01_invoice_amount", "card", "Invoice Amount", "_Measures", "Invoice Amount", 24, 24, 220, 110),
            ("v02_open_ar", "card", "Open AR Amount", "_Measures", "Open AR Amount", 260, 24, 220, 110),
            ("v03_billing_block", "card", "Billing Block Rate", "_Measures", "Billing Block Rate", 496, 24, 220, 110),
            ("v04_cash_exceptions", "tableEx", "Cash risk and disputes", "Fact_Order2CashExceptions", "AmountExposure", 24, 160, 1110, 340),
        ],
    },
    {
        "name": "p06_quote_margin",
        "displayName": "Quote and Margin Leakage",
        "visuals": [
            ("v01_quote_value", "card", "Quote Value", "_Measures", "Quote Value", 24, 24, 220, 110),
            ("v02_discount_leakage", "card", "Discount Leakage", "_Measures", "Discount Leakage", 260, 24, 220, 110),
            ("v03_approval_aging", "clusteredColumnChart", "Approval cycle and legal loops", "Fact_Quotes", "ApprovalCycleDays", 24, 160, 540, 320),
            ("v04_quote_table", "tableEx", "Quote leakage detail", "Fact_Quotes", "DiscountPct", 590, 160, 550, 320),
        ],
    },
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def tmdl_string(value: Path | str) -> str:
    return str(value).replace("\\", "/").replace('"', '\\"')


def data_type(column: str) -> str:
    if column.endswith("Flag"):
        return "boolean"
    if column.endswith("Date") or column == "Date":
        return "dateTime"
    if column in {
        "OrderQty",
        "DeliveredQty",
        "DunningLevel",
        "Year",
        "MonthNo",
        "FiscalYear",
        "FiscalPeriod",
        "ApprovalCycleDays",
        "LegalLoopCount",
    }:
        return "int64"
    if any(token in column for token in ["Amount", "Value", "Price", "Pct", "Cost", "Exposure"]):
        return "double"
    return "string"


def table_tmdl(table: str) -> str:
    pq = (TEST_PACK / "powerquery" / f"{table}.pq").read_text(encoding="utf-8")
    cols = COLUMNS.get(table, [])
    if not cols:
        cols = ["ID", "Name", "Date", "Amount"]
    lines = [f"table {table}", "\tlineageTag: generated-order2cash-demo", ""]
    for column in cols:
        lines.extend(
            [
                f"\tcolumn {column}",
                f"\t\tdataType: {data_type(column)}",
                f"\t\tsourceColumn: {column}",
                "",
            ]
        )
    lines.extend(
        [
            f"\tpartition {table} = m",
            "\t\tmode: import",
            "\t\tsource =",
        ]
    )
    for line in pq.splitlines():
        lines.append(f"\t\t\t{line}")
    lines.append("")
    return "\n".join(lines)


def measures_tmdl() -> str:
    raw = (TEST_PACK / "dax" / "order2cash_measures.dax").read_text(encoding="utf-8")
    blocks: list[tuple[str, str]] = []
    current_name: str | None = None
    current_expr: list[str] = []
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("--"):
            continue
        stripped = line.strip()
        is_measure_header = (
            line.endswith("=")
            and not line.startswith((" ", "\t"))
            and not stripped.upper().startswith(("VAR ", "RETURN"))
        )
        if is_measure_header:
            if current_name:
                blocks.append((current_name, "\n".join(current_expr).strip()))
            current_name = line[:-1].strip()
            current_expr = []
        else:
            current_expr.append(line)
    if current_name:
        blocks.append((current_name, "\n".join(current_expr).strip()))

    lines = ["table _Measures", "\tlineageTag: generated-order2cash-measures", ""]
    for name, expr in blocks:
        lines.append(f"\tmeasure '{name}' =")
        for line in expr.splitlines():
            lines.append(f"\t\t{line}")
        lines.append("\t\tformatString: #,0.00")
        lines.append("")
    return "\n".join(lines)


def relationships_tmdl() -> str:
    lines = ["// Generated Order2Cash relationships"]
    for idx, (from_table, from_col, to_table, to_col) in enumerate(RELATIONSHIPS, start=1):
        lines.extend(
            [
                f"relationship rel_{idx}_{from_table}_{to_table}",
                f"\tfromColumn: {from_table}.{from_col}",
                f"\ttoColumn: {to_table}.{to_col}",
                "\tcardinality: manyToOne",
                "\tcrossFilteringBehavior: oneDirection",
                "",
            ]
        )
    return "\n".join(lines)


def visual_json(name: str, visual_type: str, title: str, table: str, field: str, x: int, y: int, width: int, height: int) -> str:
    """Create a PBIR visual descriptor with both metadata and generation annotations."""
    is_measure = table == "_Measures"
    field_kind = "Measure" if is_measure else "Column"
    field_projection = {
        "field": {
            field_kind: {
                "Expression": {"SourceRef": {"Entity": table}},
                "Property": field,
            }
        },
        "queryRef": f"{table}.{field}",
        "nativeQueryRef": field,
    }
    if visual_type in {"clusteredBarChart", "clusteredColumnChart", "barChart"}:
        query_state = {
            "Category": {"projections": [field_projection]},
            "Y": {
                "projections": [
                    {
                        "field": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                "Property": "O2C Exception Count" if table == "Fact_Order2CashExceptions" else "Order Value",
                            }
                        },
                        "queryRef": "_Measures.O2C Exception Count" if table == "Fact_Order2CashExceptions" else "_Measures.Order Value",
                    }
                ]
            },
        }
    else:
        query_state = {"Values": {"projections": [field_projection]}}
    payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
        "name": name,
        "position": {
            "x": x,
            "y": y,
            "z": 0,
            "height": height,
            "width": width,
            "tabOrder": 0,
        },
        "visual": {
            "visualType": visual_type,
            "query": {"queryState": query_state},
            "drillFilterOtherVisuals": True,
            "objects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                        }
                    }
                ]
            },
        },
        "annotations": [
            {"name": "generatedBy", "value": "build_order2cash_pbip_project.py"},
            {"name": "businessPurpose", "value": title},
            {"name": "sourceTable", "value": table},
            {"name": "sourceFieldOrMeasure", "value": field},
        ],
    }
    return json.dumps(payload, indent=2)


def page_json(page: dict[str, object], ordinal: int) -> str:
    payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": page["name"],
        "displayName": page["displayName"],
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280,
        "ordinal": ordinal,
        "annotations": [
            {"name": "generatedBy", "value": "build_order2cash_pbip_project.py"},
            {"name": "businessProcess", "value": "Order2Cash"},
        ],
    }
    return json.dumps(payload, indent=2)


def pages_json() -> str:
    payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": [page["name"] for page in PAGE_SPECS],
        "activePageName": PAGE_SPECS[0]["name"],
    }
    return json.dumps(payload, indent=2)


def report_json() -> str:
    payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "themeCollection": {"baseTheme": {"name": "CY24SU10", "type": "SharedResources"}},
        "annotations": [
            {"name": "defaultPage", "value": PAGE_SPECS[0]["name"]},
            {"name": "generatedBy", "value": "build_order2cash_pbip_project.py"},
        ],
    }
    return json.dumps(payload, indent=2)


def write_report_pages(report_definition: Path) -> None:
    write(report_definition / "version.json", json.dumps({"version": "4.0.0"}, indent=2))
    write(report_definition / "report.json", report_json())
    write(report_definition / "pages" / "pages.json", pages_json())
    for ordinal, page in enumerate(PAGE_SPECS):
        page_dir = report_definition / "pages" / str(page["name"])
        write(page_dir / "page.json", page_json(page, ordinal))
        for visual in page["visuals"]:
            visual_name, visual_type, title, table, field, x, y, width, height = visual
            visual_dir = page_dir / "visuals" / visual_name
            write(visual_dir / "visual.json", visual_json(visual_name, visual_type, title, table, field, x, y, width, height))
            write(
                visual_dir / "mobile.json",
                json.dumps(
                    {
                        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainerMobileState/1.0.0/schema.json",
                        "name": visual_name,
                        "position": {"x": 0, "y": 0, "width": 300, "height": 120},
                    },
                    indent=2,
                ),
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    if args.out.exists():
        shutil.rmtree(args.out)

    project = args.out
    report = project / "Order2Cash.Report"
    semantic = project / "Order2Cash.SemanticModel"
    report_definition = report / "definition"
    definition = semantic / "definition"
    tables_dir = definition / "tables"
    expressions_dir = definition / "expressions"

    write(project / ".gitignore", "**/.pbi/localSettings.json\n**/.pbi/cache.abf\n")
    write(
        project / "Order2Cash.pbip",
        json.dumps(
            {
                "version": "1.0",
                "artifacts": [{"report": {"path": "Order2Cash.Report"}}],
            },
            indent=2,
        ),
    )
    write(
        report / "definition.pbir",
        json.dumps(
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
                "version": "4.0",
                "datasetReference": {"byPath": {"path": "../Order2Cash.SemanticModel"}},
            },
            indent=2,
        ),
    )
    write_report_pages(report_definition)
    write(
        report_definition / "pages" / "README.md",
        (TEST_PACK / "report" / "ORDER2CASH_REPORT_SPEC.md").read_text(encoding="utf-8"),
    )

    write(
        semantic / "definition.pbism",
        json.dumps(
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
                "version": "1.0",
            },
            indent=2,
        ),
    )
    write(
        definition / "model.tmdl",
        f"""model Order2Cash
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tdiscourageImplicitMeasures

annotation SourceWorkbook = "{tmdl_string(SOURCE_XLSX)}"
annotation BusinessProcess = "Order2Cash"
annotation Documentation = "Generated PBIP/TMDL scaffold from industrial demo data"
""",
    )
    for table in TABLES:
        write(tables_dir / f"{table}.tmdl", table_tmdl(table))
    write(tables_dir / "_Measures.tmdl", measures_tmdl())
    write(definition / "relationships.tmdl", relationships_tmdl())
    write(expressions_dir / "SourceWorkbook.tmdl", f"expression SourceWorkbook = \"{tmdl_string(SOURCE_XLSX)}\"\n")

    shutil.copytree(TEST_PACK / "docs", project / "docs")
    shutil.copytree(TEST_PACK / "data", project / "data")
    shutil.copytree(TEST_PACK / "powerquery", project / "powerquery")
    shutil.copy(TEST_PACK / "README.md", project / "README.md")
    with (project / "README.md").open("a", encoding="utf-8") as handle:
        handle.write(
            f"""

## Generated PBIP/PBIR Content

- `Order2Cash.pbip`: Power BI Project entry point.
- `Order2Cash.Report/definition.pbir`: report pointer with relative semantic model reference.
- `Order2Cash.Report/definition/pages`: generated PBIR page folders.
- `Order2Cash.Report/definition/pages/*/visuals/*/visual.json`: generated visual metadata and query placeholders.
- `Order2Cash.SemanticModel/definition`: generated TMDL model, table, measure, relationship, and expression files.

Generated pages: {len(PAGE_SPECS)}
Generated visuals: {sum(len(page['visuals']) for page in PAGE_SPECS)}

Note: Power BI Desktop may normalize or enrich PBIR JSON after opening/saving because PBIR is still a preview/developer format. This scaffold is designed so pages and visuals are always emitted alongside the semantic model.
"""
        )

    print(f"Wrote PBIP project scaffold to {project}")
    print(f"Open candidate: {project / 'Order2Cash.pbip'}")
    print(f"Report definition: {report / 'definition.pbir'}")
    print(f"Generated PBIR pages: {len(PAGE_SPECS)}")
    print(f"Generated PBIR visuals: {sum(len(page['visuals']) for page in PAGE_SPECS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
