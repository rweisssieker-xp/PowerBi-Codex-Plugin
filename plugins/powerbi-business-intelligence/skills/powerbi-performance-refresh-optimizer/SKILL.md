---
name: powerbi-performance-refresh-optimizer
description: Diagnose and optimize Power BI DAX performance, Power Query folding, refresh reliability, incremental refresh, gateway behavior, schema drift, API pagination, model size, and slow visuals.
---

# Power BI Performance and Refresh Optimizer

Use this skill for slow reports, failed refreshes, expensive DAX, non-folding Power Query, gateway bottlenecks, large models, and unstable APIs.

## Review Areas

1. DAX: expensive iterators, context transition, high-cardinality filters, repeated expressions, poor time intelligence.
2. Model: relationships, cardinality, unused columns, auto date/time, aggregation opportunities, calculation groups.
3. Power Query: folding, type conversion order, custom functions, joins, buffering, incremental refresh boundaries.
4. Refresh: gateway, credentials, privacy levels, API pagination, throttling, schema drift, timeout handling.
5. Capacity: memory, CPU, visual query load, dataset size, refresh concurrency.

## Output Requirements

- Separate quick wins, structural fixes, and architecture changes.
- Include expected impact, risk, and verification method.

## Assets

- `assets/performance-refresh-checklist.md`: optimizer checklist.

