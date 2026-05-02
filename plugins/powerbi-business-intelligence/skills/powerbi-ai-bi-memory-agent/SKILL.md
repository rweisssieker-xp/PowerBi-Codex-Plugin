---
name: powerbi-ai-bi-memory-agent
description: Use when Power BI decisions, KPI definitions, model patterns, source mappings, incidents, fixes, and best practices must be retained across projects and reused safely.
---

# Power BI AI BI Memory Agent

Maintain reusable enterprise BI memory without storing secrets.

## Output Contract

- Memory item: decision, KPI definition, mapping, pattern, incident, fix, exception, or lesson learned.
- Context, source evidence, owner, applicability, expiry/review date, and confidentiality class.
- Reuse recommendation and conflicting memory entries.
- `en-US` and `de-DE` summary for durable enterprise knowledge.

## Checks

- Do not store credentials, customer-sensitive extracts, or undocumented assumptions as facts.
- Mark stale memory for review.
