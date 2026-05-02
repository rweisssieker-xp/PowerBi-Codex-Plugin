---
name: powerbi-admin-api-playbook
description: Use when Power BI tenant administration needs Admin API playbooks for workspace inventory, usage metrics, refresh failures, endorsements, sensitivity labels, sharing risk, gateways, and capacity.
---

# Power BI Admin API Playbook

Plan tenant scans and governance actions using Power BI/Fabric admin APIs.

## Output Contract

- Admin question, required permissions, API families, scan scope, frequency, and output tables.
- Inventory fields for workspaces, reports, datasets, refresh, users, gateways, capacities, labels, endorsements, and sharing.
- Risk rules and remediation actions.
- Privacy, rate-limit, and audit handling notes.

## Checks

- Confirm required admin permissions.
- Treat delete/removal actions as approval-gated.
