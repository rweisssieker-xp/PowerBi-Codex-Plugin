---
name: powerbi-automated-security-exposure-scan
description: Use when Power BI needs automated scanning for RLS, sharing, export, external guests, PII, sensitivity labels, groups, workspaces, and tenant security exposure.
---

# Power BI Automated Security Exposure Scan

Scan for risky BI security exposure patterns.

## Output Contract

- Asset, workspace, users/groups, RLS/OLS, labels, export settings, guest access, PII, and sharing mode.
- Risk findings, severity, affected data, owner, and remediation.
- Exception workflow and audit evidence.

## Checks

- Treat external guests plus export plus sensitive data as high risk.
