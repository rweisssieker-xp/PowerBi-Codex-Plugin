---
name: powerbi-quality-gate
description: Run Power BI release quality gates. Use before publishing, certifying, migrating, or changing reports and semantic models to verify KPI definitions, RLS, refresh, performance, ownership, documentation, and acceptance.
---

# Power BI Quality Gate

Use this skill before a Power BI artifact goes live.

## Gate Checks

- Business owner and data owner assigned.
- KPI contracts approved and reconciled.
- Fact grain and model relationships documented.
- RLS/OLS tested with allowed and denied cases.
- Refresh successful and monitored.
- Performance acceptable for target users.
- Sensitivity label and sharing policy applied.
- Documentation and support owner complete.
- Acceptance pack signed off.

## Output Requirements

- Return pass, conditional pass, or fail.
- For conditional pass or fail, list blockers, required evidence, owner, and due date.

