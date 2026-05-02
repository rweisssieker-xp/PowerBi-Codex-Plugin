---
name: powerbi-nl-to-powerquery-generator
description: Use when natural-language source extraction requirements should become Power Query/M designs for APIs, OData, SQL, files, pagination, incremental refresh, typing, error handling, or schema drift.
---

# Power BI NL to Power Query Generator

Use this skill before generating Power Query/M.

## Generation Requirements

- Resolve connector, endpoint/table/entity, auth mode, parameters, and privacy level.
- Define pagination, retry, throttling, and delta/incremental refresh.
- Type columns deliberately and handle schema drift.
- Add tests through `powerbi-powerquery-test-harness`.

## Output Requirements

- Include M design, parameters, expected schema, tests, refresh constraints, and security notes.
- Do not include secrets or hard-coded credentials.

