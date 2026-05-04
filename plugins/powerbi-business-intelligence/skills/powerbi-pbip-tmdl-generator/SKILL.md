---
name: powerbi-pbip-tmdl-generator
description: Use when a Power BI design should become PBIP or TMDL-ready structures, model folders, table specs, measure files, calculation groups, perspectives, roles, and deployment-ready artifacts.
---

# Power BI PBIP TMDL Generator

Turn approved designs into PBIP/TMDL implementation artifacts.

## Output Contract

- PBIP folder plan, semantic model objects, tables, columns, relationships, measures, calculation groups, perspectives, roles, and annotations.
- Naming convention, display folders, descriptions, translations, and certification metadata.
- Deployment notes for Git, Tabular Editor, Fabric workspace, and release pipeline.
- Validation checklist for model load, measure tests, RLS, and source reconciliation.

## Checks

- Generate implementation artifacts only after KPI contracts and grain are explicit.
- Preserve `en-US` and `de-DE` descriptions when documentation is required.

## Runtime Executor

For a complete generated PBIP/PBIR/TMDL package, use:

```powershell
python scripts\powerbi_expert_factory.py report-package --process <process-id> --sources "<source description>" --goal "<report goal>" --out outputs\report-packages\<process-id>
```
