---
name: powerbi-ai-schema-drift-resolver
description: Use when source schema changes break or threaten Power Query, semantic models, DAX, refresh, data contracts, tests, or report visuals.
---

# Power BI AI Schema Drift Resolver

Resolve source changes before they become production failures.

## Output Contract

- Drift event: changed/missing/renamed field, type change, new status, new key, changed API, or table/view replacement.
- Impact on Power Query, model, DAX, visuals, data contracts, tests, and docs.
- Fix plan, backward compatibility, validation, owner, and release path.
- Blocking severity and rollback option.

## Checks

- Do not silently map renamed fields without source-owner confirmation.
- Update tests and documentation with the fix.
