# Industry Process Packs

Generated Power BI process-pack specifications for every process in [industry_process_catalog.json](../../data/industry_process_catalog.json).

Each process folder contains `model_spec.json`, `dax_measures.dax`, `report_pages.json`, `quality_gate.json`, and a README.

Each `model_spec.json` separates:

- demo CSV routing for repeatable offline tests,
- production native source-routing recommendations,
- fallback source patterns,
- required source decisions for gateway, credentials, privacy, folding, refresh, schema drift, data quality, and reconciliation.

Production source-routing details are generated in [source-routing](../source-routing/README.md).
