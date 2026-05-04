---
name: powerbi-report-package-runtime
description: Use when a user asks to generate, build, or improve a Power BI report/model package from a process request, source description, or business question using the executable report-package path.
---

# Power BI Report Package Runtime

Use this skill as the default executable path when the user asks to generate a Power BI report, build a semantic model, create DAX/Power Query plans, or improve an existing model/report package.

## Runtime Command

Prefer the repository executor:

```powershell
python scripts\powerbi_expert_factory.py report-package --process <process-id> --sources "<source description>" --goal "<report goal>" --out outputs\report-packages\<process-id>
```

## Output Contract

- PBIP/PBIR/TMDL project package.
- Source profile and native connector recommendation.
- Model build plan with facts, dimensions, relationships, RLS, and owner roles.
- DAX measure plan and expected-result policy.
- Power Query/M plan with connector, typing, folding, and drift checks.
- Report page plan with executive overview, flow/aging, exceptions/root cause, action cockpit, and trust page.
- Model improvement plan and validation plan.
- Report package manifest with next validation/deployment commands.

## Checks

- Do not invent source credentials or store secrets.
- Keep connector, table, and column names provisional until source metadata is verified.
- Always include validation and improvement artifacts, not only report layout.
