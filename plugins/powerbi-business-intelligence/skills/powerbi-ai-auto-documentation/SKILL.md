---
name: powerbi-ai-auto-documentation
description: Use when AI/KI should generate documentation from PBIP, TMDL, DAX, Power Query, report specs, semantic models, lineage, quality gates, or delivery artifacts.
---

# Power BI AI Auto Documentation

Use this skill to create documentation from actual artifacts.

**Required companion skill:** Use `powerbi-bilingual-documentation` for all substantial generated documentation.

## Inputs

- PBIP/TMDL/model metadata.
- DAX measures.
- Power Query/M.
- Report specs and page definitions.
- KPI contracts and glossary.
- Quality gate and validation evidence.

## Output Requirements

- Produce report docs, model docs, KPI docs, data flow, RLS matrix, refresh notes, and owner summary.
- Separate generated interpretation from artifact-backed facts.
- Provide matching `en-US` and `de-DE` documentation sections or paired files.
