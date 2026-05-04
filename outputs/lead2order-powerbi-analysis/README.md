# Lead2Order Power BI Analysis Package

Concrete Power BI analysis package for the Lead2Order process owner. The package contains a PBIP project, a governed DAX measure catalog, KPI-to-problem-question mapping, and a report blueprint.

## Contents

- `pbip/Lead2OrderAnalysis/`: generated PBIP/PBIR/TMDL project using local demo CSV data.
- `measure_catalog.json`: complete measure and KPI catalog with business questions and decisions.
- `kpi_problem_questions.json`: process-owner questions mapped to measures, drilldowns, and actions.
- `report_blueprint.json`: recommended pages and visuals for Power BI implementation.
- `dax_measures.dax`: DAX catalog for review and copy into the semantic model.

## Validation

Run `python scripts\powerbi_expert_factory.py validate --project outputs\lead2order-powerbi-analysis\pbip\Lead2OrderAnalysis`.
