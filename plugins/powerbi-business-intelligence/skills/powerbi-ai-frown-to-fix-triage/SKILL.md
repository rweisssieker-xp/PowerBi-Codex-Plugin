---
name: powerbi-ai-frown-to-fix-triage
description: Use when Power BI Desktop produces a Frown error, PBIP load failure, model validation error, visual error, DirectQuery error, Power Query load error, or Desktop crash that must be mapped to likely fixes.
---

# Power BI AI Frown-to-Fix Triage

Use this skill to translate Power BI Desktop Frown output into a concrete repair plan.

## Triage Pattern

1. Capture error message, timestamp, Desktop version, session id, and failing artifact.
2. Classify failure domain: PBIP/PBIR structure, TMDL model, relationship graph, DAX, Power Query/M, native source, DirectQuery/live connection, visual binding, or Desktop compatibility.
3. Extract named tables, measures, relationships, queries, pages, and visuals.
4. Map symptoms to likely source files and validators.
5. Produce a fix plan and retest command sequence.

## Output Requirements

- Include failure class, evidence, likely root cause, affected files, fix plan, and retest path.
- Do not guess silently; mark low-confidence diagnoses and required evidence.

## Executable Support

- Use `scripts/powerbi_desktop_smoke_test.ps1` to capture before/after Frown evidence.
- Use `scripts/powerbi_expert_factory.py validate` first to catch common causes before reopening Desktop: ambiguous paths, missing visual bindings, brittle M navigation, and unsupported demo source patterns.
