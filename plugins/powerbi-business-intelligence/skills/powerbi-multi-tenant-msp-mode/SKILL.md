---
name: powerbi-multi-tenant-msp-mode
description: Use when Power BI work spans multiple customers, tenants, business units, or MSP-style delivery boundaries and requires isolated policies, artifacts, evidence, rollout status, and governance.
---

# Power BI Multi-Tenant / MSP Mode

Use this skill when a request must keep tenants, customers, workspaces, policies, evidence, credentials, or rollout states separated.

## Runtime Commands

Create tenant and gateway request payloads without storing credentials:

```powershell
python scripts\powerbi_expert_factory.py tenant-scan-request --tenant <tenant-id> --workspace <workspace-id> --out outputs\runtime-executors\<tenant-id>-tenant-scan-request.json
python scripts\powerbi_expert_factory.py gateway-audit-request --gateway <gateway-id> --datasource <datasource-id> --out outputs\runtime-executors\<tenant-id>-gateway-audit-request.json
```

## Output Contract

- Tenant isolation manifest.
- Customer/workspace policy matrix.
- Per-tenant source, report, model, gateway, and deployment evidence.
- Cross-tenant leakage checks.
- Rollout status board and owner signoff queue.

## Checks

- Never mix tenant credentials, evidence, source paths, or output folders.
- Make tenant boundary explicit in every generated artifact.
- Treat cross-tenant deployment, deletion, sharing, and permission changes as approval-gated.
