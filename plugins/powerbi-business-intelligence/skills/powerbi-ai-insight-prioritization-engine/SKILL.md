---
name: powerbi-ai-insight-prioritization-engine
description: Use when AI-generated Power BI insights, anomalies, exceptions, or narratives need ranking by business impact, confidence, urgency, actionability, and owner readiness.
---

# Power BI AI Insight Prioritization Engine

Rank insights so users focus on what matters.

## Output Contract

- Insight list with KPI, segment, value, delta, impact, owner, and evidence.
- Scores for business impact, confidence, urgency, actionability, recurrence, and data quality.
- Recommended focus order, suppressed noise, and required follow-up.
- Action routing and retest condition.

## Checks

- Do not rank high-impact insights high when evidence quality is weak.
- Separate anomaly size from business priority.
