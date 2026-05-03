---
name: powerbi-ai-self-healing-refresh-agent
description: Use when Power BI refresh failures need automated diagnosis and fix planning for credentials, gateway, schema drift, API pagination, timeout, privacy levels, type conversion, or missing files/sheets.
---

# Power BI AI Self-Healing Refresh Agent

Use this skill for refresh failure remediation.

## Failure Classes

- Credential, token, permission, and gateway failures.
- Schema drift: missing, renamed, added, or type-changed columns.
- API pagination, throttling, timeout, and delta issues.
- Privacy level, firewall, and data combination blocks.
- Missing Excel sheets, CSV files, folder paths, or source objects.

## Output Requirements

- Produce failure class, likely root cause, owner, fix plan, retest, and prevention control.
- Separate auto-fixable issues from issues requiring credential or source-owner action.

