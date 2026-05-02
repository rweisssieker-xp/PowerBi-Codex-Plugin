---
name: powerbi-powerquery-code-generator
description: Use when Power BI work needs Power Query M designs or code for APIs, SAP OData, SQL, files, pagination, incremental refresh, schema drift, error handling, typing, and folding.
---

# Power BI Power Query Code Generator

Generate Power Query/M extraction designs with refresh reliability and governance.

## Output Contract

- Connector, authentication pattern, gateway need, query folding expectation, privacy level, and refresh mode.
- M query structure, parameters, pagination, retry/error handling, type conversion, schema drift handling, and incremental refresh fields.
- Validation: row count, duplicate keys, null checks, source totals, freshness, and folding diagnostics.
- Security and PII handling notes.

## Checks

- Prefer foldable source-side filters for large sources.
- Never hardcode secrets in M.
