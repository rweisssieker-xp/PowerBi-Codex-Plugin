---
name: powerbi-nl-to-dax-guardrails
description: Use when natural-language requests should become DAX measures with KPI contracts, semantic context, tests, validation, and guardrails against incorrect filter or date logic.
---

# Power BI NL to DAX Guardrails

Use this skill before generating DAX from natural language.

## Guardrails

- Resolve fact grain, date role, filters, exclusions, and certified KPI definition.
- Generate DAX only against verified model objects.
- Add test cases through `powerbi-dax-test-harness`.
- Include source reconciliation and edge cases.
- Mark uncertain assumptions explicitly.

## Output Requirements

- Include business definition, DAX, dependencies, tests, validation source, and confidence.
- Treat untested generated DAX as draft.

