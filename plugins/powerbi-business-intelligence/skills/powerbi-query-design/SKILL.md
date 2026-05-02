---
name: powerbi-query-design
description: Translate business questions into Power BI-ready source extraction plans, Power Query steps, SQL/OData/API queries, semantic model requirements, DAX definitions, validation checks, and report requirements for any supported Power BI data source.
---

# Power BI Query Design

Use this skill to turn a reporting question into an implementable source-to-model specification.

## Workflow

1. Restate the business question as facts, dimensions, filters, date logic, grain, and decision action.
2. Identify source path: file/folder, SQL/database, data warehouse, Fabric lakehouse, SAP, SaaS connector, OData, REST API, GraphQL/custom connector, streaming, or manual input.
3. Draft source artifacts: entity/table, filters, joins, pagination, incremental boundaries, selected fields, and privacy constraints.
4. Define Power BI model impact: fact table, dimensions, relationships, DAX measures, RLS, refresh, validation.
5. Include reconciliation checks against trusted source totals or extracts.
6. Flag source-specific assumptions: field names, status values, fiscal calendars, currency, PII, security, and latency.

## References

- Load `references/query-to-powerbi.md` for translation patterns and output structure.
- Load `references/business-question-examples.md` for common business problem examples.

## Assets

- `assets/query-powerbi-spec-template.md`: implementation spec template.

## Scripts

- `scripts/new_query_powerbi_spec.py`: Generate a starter spec from a business question.

