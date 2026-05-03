# Power BI Order2Cash Test Pack

This pack uses the generated industrial Excel workbook as a Power BI source and provides a complete Order2Cash implementation blueprint.

## Contents

- `powerquery/*.pq`: one Power Query M import per required sheet.
- `data/Fact_Order2CashExceptions.csv`: consolidated action backlog for all detected O2C problems.
- `dax/order2cash_measures.dax`: KPI measures for O2C problems and customer churn risk.
- `model/relationships.md`: semantic model relationship plan.
- `report/ORDER2CASH_REPORT_SPEC.md`: report pages, KPI values from the demo workbook, and top-risk customers.
- `docs/order2cash.en-US.md` and `docs/order2cash.de-DE.md`: bilingual business documentation.

## Source Workbook

`C:\tmp\PowerBi-Codex-Plugin\outputs\powerbi-industrial-demo\powerbi_industrial_demo_data.xlsx`

## How To Use In Power BI Desktop

1. Open Power BI Desktop.
2. Import the Excel workbook.
3. Load the sheets listed in `powerquery/`.
4. Create relationships from `model/relationships.md`.
5. Add measures from `dax/order2cash_measures.dax`.
6. Build pages from `report/ORDER2CASH_REPORT_SPEC.md`.

## Test Outcome

The current demo data produces 9 high-risk churn customers, 526 O2C exception rows, 75.0% ATP issue rate, 96.8% late/short delivery rate, and 3.951.156 EUR open AR amount.
