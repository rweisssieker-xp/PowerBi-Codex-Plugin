---
name: powerbi-connector-capability-matrix
description: Use when selecting Power BI data-source connectors and comparing Import, DirectQuery, Direct Lake, incremental refresh, gateway, SSO, folding, privacy, and refresh limitations.
---

# Power BI Connector Capability Matrix

Choose connector and storage mode based on capability, data volume, security, and latency.

## Output Contract

- Source type and connector candidates.
- Capability matrix: Import, DirectQuery, Direct Lake, composite, folding, incremental refresh, gateway, SSO, OAuth, service principal, and privacy level.
- Recommended pattern with tradeoffs, blockers, fallback, and validation.
- Refresh, performance, and security implications.

## Checks

- Verify connector capabilities against current Microsoft documentation when exact behavior matters.
- Do not assume folding for custom SQL, APIs, or complex transformations.
