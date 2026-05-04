# Power BI Source Routing

Production source-routing recommendations for all industrial process packs.

- `process_source_routing.json`: full process-to-connector routing map.
- `process_source_routing.csv`: flat routing index for Power BI ingestion.

## Demo Versus Production Sources

Demo CSV folders are included for repeatable offline testing. They are not the production source strategy.

Production implementations must replace demo routing with validated native Power BI / Power Query connectors according to [powerbi_source_capability_matrix.json](../../data/powerbi_source_capability_matrix.json).

Every generated process pack declares:

- demo CSV path for offline tests,
- production native source-routing candidates,
- fallback source patterns,
- required source decisions for gateway, credentials, privacy, folding, refresh, schema drift, data quality, and reconciliation.

The process catalog is maintained in [industry_process_catalog.json](../../data/industry_process_catalog.json). Generated process packs are available in [industry-process-packs](../industry-process-packs/README.md).
