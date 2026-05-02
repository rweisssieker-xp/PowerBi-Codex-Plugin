# Governance and Quality

## Quality Gate Areas

Before a Power BI artifact is published, certified, migrated, or handed over, validate:

- KPI definitions.
- Source reconciliation.
- Semantic model grain.
- Relationship correctness.
- DAX correctness.
- Power Query reliability.
- Refresh and gateway behavior.
- RLS/OLS.
- Performance.
- Lineage.
- Documentation.
- Owner acceptance.

## KPI Contract

Each governed KPI should define:

- Business name.
- Description.
- Owner.
- Numerator.
- Denominator.
- Date basis.
- Grain.
- Filters and exclusions.
- Currency/unit handling.
- Reconciliation source.
- Tolerance.
- Refresh SLA.
- Certification status.

## AI/KI Quality Rules

AI-generated outputs must:

- State assumptions.
- Identify missing evidence.
- Avoid claiming causality without tested hypotheses.
- Use source metadata and KPI contracts.
- Include confidence level when insights are generated.
- Route unresolved issues to accountable owners.

## Release Evidence

Release packs should include:

- Test summary.
- Reconciliation results.
- Security review.
- Performance review.
- Known limitations.
- Business sign-off.
- Rollback or remediation plan.
