---
name: powerbi-ai-governance-drift-detector
description: Use when Power BI reports, measures, semantic models, RLS, sources, labels, ownership, or KPI definitions may have drifted away from approved standards.
---

# Power BI AI Governance Drift Detector

Detect where BI assets no longer match governance standards.

## Output Contract

- Asset scope, approved standard, observed state, drift type, severity, and owner.
- Drift categories: KPI, DAX, model, source, RLS/OLS, label, sharing, refresh, documentation, certification, or ownership.
- Impacted reports, downstream decisions, remediation, and recertification need.
- Evidence and false-positive notes.

## Checks

- Compare against explicit standards, not personal preference.
- Distinguish allowed local variant from drift.
