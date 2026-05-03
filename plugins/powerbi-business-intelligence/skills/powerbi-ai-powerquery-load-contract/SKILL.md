---
name: powerbi-ai-powerquery-load-contract
description: Use when Power Query queries need explicit load contracts for source object keys, columns, types, culture, refresh mode, gateway, privacy, folding, reconciliation, and failure handling.
---

# Power BI AI Power Query Load Contract

Use this skill for every production Power Query source.

## Contract Fields

- Source system, connector, object path, object kind, and credential owner.
- Required columns, optional columns, keys, data types, culture, nullability, and uniqueness rules.
- Refresh mode, incremental refresh policy, gateway, privacy level, and folding expectation.
- Row-count, amount-total, min/max date, and checksum-style reconciliation.
- Schema drift behavior and owner routing.

## Output Requirements

- Include a machine-readable load contract and human-readable en-US/de-DE notes.
- Mark hardcoded secrets and personal file paths as blockers.

