---
name: powerbi-ai-powerbi-desktop-smoke-tester
description: Use when generated PBIP, PBIR, TMDL, report, or semantic model artifacts must be opened and smoke-tested in the installed Power BI Desktop version with Frown, process, and load checks.
---

# Power BI AI Desktop Smoke Tester

Use this skill before claiming a generated Power BI artifact works in Desktop.

## Checks

- Detect installed Power BI Desktop version and target artifact path.
- Open the `.pbip` or `.pbir` artifact in Power BI Desktop.
- Compare latest Frown snapshot timestamp before and after opening.
- Verify Power BI Desktop process is alive and responsive.
- Verify main window title and expected artifact name when available.
- Check local Analysis Services workspace when accessible.
- Report tables, relationships, measures, columns, and obvious load failures.

## Output Requirements

- Include Power BI Desktop version, artifact path, Frown before/after, process state, and result.
- Mark the artifact as `passed`, `failed`, or `inconclusive`.
- If failed, route to `powerbi-ai-frown-to-fix-triage`.

## Executable Support

- Use `scripts/powerbi_desktop_smoke_test.ps1 -PbipPath <path-to.pbip> -OutJson <evidence.json>` when Power BI Desktop is installed locally.
- The result is release blocking when a new `FrownSnapShot*.zip` appears after opening the PBIP.
