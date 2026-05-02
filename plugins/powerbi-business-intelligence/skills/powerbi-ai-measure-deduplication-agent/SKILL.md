---
name: powerbi-ai-measure-deduplication-agent
description: Use when Power BI models have duplicated, near-duplicate, conflicting, unused, local, or uncertified DAX measures that need consolidation.
---

# Power BI AI Measure Deduplication Agent

Find and consolidate duplicate or conflicting DAX measures.

## Output Contract

- Measure inventory with name, expression, folder, owner, report usage, and KPI mapping.
- Duplicate clusters, semantic near-duplicates, and conflicting definitions.
- Recommended certified measure, deprecated measures, migration map, and impact analysis.
- Test cases and owner sign-off.

## Checks

- Do not merge measures that differ by valid business grain or date basis.
- Preserve compatibility aliases where migration risk is high.
