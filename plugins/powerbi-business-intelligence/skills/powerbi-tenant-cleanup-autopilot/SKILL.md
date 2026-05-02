---
name: powerbi-tenant-cleanup-autopilot
description: Use when Power BI tenants need cleanup of orphaned workspaces, stale reports, broken refreshes, duplicate datasets, risky sharing, capacity waste, or unmanaged assets.
---

# Power BI Tenant Cleanup Autopilot

Create a governed cleanup plan for Power BI/Fabric tenants.

## Output Contract

- Workspace, report, dataset, refresh, owner, sharing, sensitivity label, gateway, and capacity inventory.
- Findings: orphaned, stale, duplicate, failing, risky, expensive, uncertified, or unmanaged.
- Action plan: fix, assign owner, consolidate, certify, archive, delete candidate, or migrate.
- Communication plan, retention rule, and sign-off workflow.

## Checks

- Treat deletion as a candidate until business owner approval exists.
- Preserve evidence for audit and rollback.
