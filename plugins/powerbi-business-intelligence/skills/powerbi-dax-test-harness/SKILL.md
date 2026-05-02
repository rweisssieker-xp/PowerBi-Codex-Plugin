---
name: powerbi-dax-test-harness
description: Use when DAX measures need test cases, expected totals, edge cases, time-intelligence validation, RLS context checks, or reconciliation against source totals.
---

# Power BI DAX Test Harness

Use this skill before accepting generated or refactored DAX.

## Test Areas

- Base totals against source totals.
- Edge cases: blanks, zero denominator, inactive records, future dates, missing dimensions.
- Time intelligence: YTD, MTD, rolling periods, fiscal calendars, prior year.
- Filter context: slicers, drillthrough, hierarchy levels.
- RLS contexts: allowed user, restricted user, denied user.
- Regression: before/after measure result comparisons.

## Output Requirements

- Provide test name, filter context, expected result, tolerance, source of truth, and pass/fail criteria.
- Treat untested DAX as draft.

