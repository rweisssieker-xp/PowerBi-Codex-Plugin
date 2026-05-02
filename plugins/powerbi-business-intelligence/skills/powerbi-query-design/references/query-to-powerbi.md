# Query to Power BI Pattern

## Output Structure

- Business question and decision action.
- Source entities and connector type.
- Grain and filters.
- Required fields and joins.
- Incremental refresh column and historical backfill.
- Power Query transformation plan.
- Semantic model table and relationships.
- DAX measures.
- Report pages and visuals.
- Validation and security checks.

## Connector Notes

- SQL: prefer source views for complex joins; keep folding; parameterize date ranges.
- OData: verify entity names, expand/navigation limits, paging, and service throttling.
- REST: document pagination, auth, rate limits, schema drift, and retry behavior.
- Files: document folder conventions, schema drift, encoding, and archival rules.
- SAP: clarify extractor/CDS/BW/HANA path, fiscal calendar, currency, and authorization.
- Fabric/Lakehouse: prefer curated Delta tables and semantic model ownership boundaries.

