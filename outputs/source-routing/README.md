# Power BI Source Routing

Production source-routing recommendations for all industrial process packs.

- `process_source_routing.json`: full process-to-connector routing map.
- `process_source_routing.csv`: flat routing index for Power BI ingestion.

Demo CSV folders are included for repeatable offline testing. Production implementations must replace demo routing with validated native Power BI / Power Query connectors according to `data/powerbi_source_capability_matrix.json`.
