---
name: powerbi-ai-visual-binding-validator
description: Use when PBIR report visuals must be validated against actual semantic model tables, columns, measures, visual roles, query references, and supported visual types.
---

# Power BI AI Visual Binding Validator

Use this skill before claiming report pages are usable.

## Validation Areas

- Visual `queryState` references existing model tables, columns, and measures.
- Visual roles match the visual type and field kind.
- Query references and native query references are coherent.
- Visual type is supported by the target PBIR/Desktop version.
- Report pages do not point to deleted measure tables or renamed fields.
- Broken bindings are mapped to model or report fixes.

## Output Requirements

- Include page, visual, referenced field, validation result, and fix recommendation.
- Mark report as `pass`, `pass-with-risk`, or `fail`.

## Executable Support

- Use `scripts/powerbi_expert_factory.py validate --project <pbip-folder>` to parse PBIR `visual.json` files and verify table/column/measure bindings against TMDL.
- Treat missing visual fields or measures as release-blocking defects.
