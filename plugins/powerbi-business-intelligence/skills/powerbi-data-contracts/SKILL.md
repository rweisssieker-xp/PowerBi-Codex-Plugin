---
name: powerbi-data-contracts
description: Use when Power BI delivery needs enforceable source data requirements, required fields, keys, history, quality thresholds, SLAs, schema ownership, blocking conditions, or source-to-model contracts.
---

# Power BI Data Contracts

Use this skill to reduce failed report builds caused by unclear source expectations.

## Contract Sections

- Source owner and consuming model owner.
- Required entities, fields, keys, data types, and relationships.
- Grain, history, update frequency, latency, retention.
- Quality thresholds: completeness, uniqueness, referential integrity, timeliness.
- Security: PII, RLS attributes, masking, export restrictions.
- Change management: schema changes, deprecations, notification SLA.
- Blocking conditions for build or certification.

## Output Requirements

- Produce a contract table and explicit pass/fail criteria.
- Mark missing keys, missing history, unstable schema, or unresolved PII as blockers.

