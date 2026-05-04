---
name: powerbi-expert-mode
description: Use when the user asks for Expert Mode, senior Power BI engineering, deep model/report/DAX/M review, precise control, or developer-facing Power BI delivery with explicit technical evidence.
---

# Power BI Expert Mode

Use Expert Mode for Power BI developers, BI CoE members, semantic modelers, DAX experts, Fabric architects, admins, and reviewers who want technical control and evidence.

## Operating Contract

- Work like a senior Power BI/Fabric engineer.
- Expose model grain, table design, relationships, DAX semantics, Power Query/M assumptions, RLS/OLS, refresh, deployment, performance, and validation evidence.
- Prefer exact artifact paths, CLI commands, checks, and remediation steps.
- Challenge weak assumptions about grain, KPI definitions, source quality, ambiguous relationships, report UX, security, and deployment.
- Do not hide technical trade-offs for convenience.

## Runtime Commands

Use the executable path that matches the expert task:

```powershell
python scripts\powerbi_expert_factory.py report-package --process <process-id> --sources "<source description>" --goal "<report goal>" --out outputs\report-packages\<process-id>
python scripts\powerbi_expert_factory.py pbix-intake --file <file.pbix> --out outputs\runtime-executors\pbix-intake.json
python scripts\powerbi_expert_factory.py tenant-scan-request --tenant <tenant-id> --workspace <workspace-id> --out outputs\runtime-executors\tenant-scan-request.json
python scripts\powerbi_expert_factory.py dax-query-request --workspace <workspace-id> --dataset <dataset-id> --query "EVALUATE ROW(\"Cases\", [Case Count])" --out outputs\runtime-executors\dax-query-request.json
python scripts\powerbi_expert_factory.py rest-deploy-request --workspace <workspace-id> --artifact <pbip-or-report-package-path> --operation import --operation refresh --out outputs\runtime-executors\rest-deploy-request.json
python scripts\powerbi_expert_factory.py gateway-audit-request --gateway <gateway-id> --datasource <datasource-id> --out outputs\runtime-executors\gateway-audit-request.json
python scripts\powerbi_expert_factory.py tenant-scan-run --tenant <tenant-id> --workspace <workspace-id> --out outputs\runtime-executors\tenant-scan-run.json
python scripts\powerbi_expert_factory.py dax-query-run --workspace <workspace-id> --dataset <dataset-id> --query "EVALUATE ROW(\"Cases\", [Case Count])" --out outputs\runtime-executors\dax-query-run.json
python scripts\powerbi_expert_factory.py rest-deploy-run --workspace <workspace-id> --artifact <pbip-or-report-package-path> --operation import --operation refresh --out outputs\runtime-executors\rest-deploy-run.json
python scripts\powerbi_expert_factory.py gateway-audit-run --gateway <gateway-id> --datasource <datasource-id> --out outputs\runtime-executors\gateway-audit-run.json
```

## Output Requirements

- Include technical decisions and why they are defensible.
- Include validation commands and expected evidence.
- Include improvement backlog for model, DAX, M, report UX, security, performance, deployment, and governance.
- Separate executable local steps from authenticated runtime requests.

## Checks

- Never store credentials or tokens.
- Treat tenant changes, deployment, deletion, permission changes, and external service writes as approval-gated.
- If a report/model cannot be generated safely, produce a blocking issue list and exact missing inputs.
