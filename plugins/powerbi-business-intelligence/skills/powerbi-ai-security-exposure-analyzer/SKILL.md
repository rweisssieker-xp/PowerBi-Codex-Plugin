---
name: powerbi-ai-security-exposure-analyzer
description: Use when Power BI security exposure must be analyzed across RLS, OLS, sharing, export, sensitivity labels, external guests, PII, groups, workspaces, and tenant settings.
---

# Power BI AI Security Exposure Analyzer

Find risky combinations that expose sensitive BI data.

## Output Contract

- Asset, user/group, workspace, data class, RLS/OLS, label, sharing, export, and guest access context.
- Exposure findings, severity, attack/misuse path, impacted data, and owner.
- Remediation: revoke, relabel, restrict export, add RLS/OLS, split model, review groups, or escalate.
- Audit evidence and exception log.

## Checks

- Treat external sharing plus PII/export as high-risk until reviewed.
