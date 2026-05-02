---
name: powerbi-powerquery-test-harness
description: Use when Power Query extraction or transformation needs tests for query folding, schema drift, nulls, duplicates, pagination, type conversion, incremental refresh, privacy levels, or source reconciliation.
---

# Power BI Power Query Test Harness

Use this skill before accepting extraction logic.

## Test Areas

- Query folding and native query pushdown.
- Schema drift: missing, renamed, added, type-changed columns.
- Nulls, duplicates, orphan keys, invalid dates.
- API pagination, throttling, retry, and delta behavior.
- Incremental refresh boundary correctness.
- Privacy levels, gateway identity, and credential scope.
- Row counts and source totals.

## Output Requirements

- Include test input, expected output, failure mode, owner, and remediation.
- Mark non-folding transformations as risks when data volume is high.

