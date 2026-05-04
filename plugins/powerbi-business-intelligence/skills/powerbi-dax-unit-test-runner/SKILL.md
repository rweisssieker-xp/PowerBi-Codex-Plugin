---
name: powerbi-dax-unit-test-runner
description: Use when DAX measures require executable or semi-executable unit tests, query-based assertions, XMLA or Tabular Editor validation, edge cases, totals, RLS contexts, and reconciliation evidence.
---

# Power BI DAX Unit Test Runner

Design DAX tests that can be executed through DAX queries, XMLA, Tabular Editor workflows, or documented manual evidence.

## Output Contract

- Measure under test, KPI contract, expected result, filter context, date context, and RLS context.
- Test cases for totals, blanks, zero denominators, many-to-many risk, time intelligence, currency, and segment filters.
- Execution route: DAX query, Tabular Editor script, XMLA endpoint, Performance Analyzer export, or manual reconciliation.
- Pass/fail criteria, evidence capture, owner, and remediation.

## Checks

- Do not treat visual inspection as sufficient for certified measures.

## Runtime Executor

For dataset-backed DAX validation, create a credential-safe DAX query request:

```powershell
python scripts\powerbi_expert_factory.py dax-query-request --workspace <workspace-id> --dataset <dataset-id> --query "EVALUATE ROW(\"Cases\", [Case Count])" --out outputs\runtime-executors\dax-query-request.json
```
