---
name: powerbi-action-recommendation-engine
description: Use when Power BI analysis should produce prioritized actions such as customers to call, suppliers to escalate, materials to reduce, orders to prioritize, invoices to collect, or machines to inspect.
---

# Power BI Action Recommendation Engine

Use this skill when the business needs next actions, not only dashboards.

## Action Pattern

1. Define action owner and decision window.
2. Define impact metric: revenue, cash, cost, risk, service, quality, downtime.
3. Rank entities by impact, urgency, confidence, and controllability.
4. Attach reason codes and evidence.
5. Define action status, feedback loop, and outcome tracking.

## Output Requirements

- Include ranked action table fields, prioritization formula, reason codes, owner, SLA, and expected impact.
- Separate recommendations from automated decisions when human review is required.

