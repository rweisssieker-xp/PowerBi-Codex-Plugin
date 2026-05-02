---
name: powerbi-ai-causal-hypothesis-tester
description: Use when Power BI users suspect a business driver and need AI-assisted causal plausibility checks instead of simple correlation claims.
---

# Power BI AI Causal Hypothesis Tester

Test whether a proposed driver is plausible, not merely correlated.

## Output Contract

- Hypothesis, expected mechanism, affected KPI, segment, timeframe, and counterfactual.
- Evidence, counterevidence, confounders, lag effects, data gaps, and confidence.
- Recommended analysis: cohort, before/after, matched segment, decomposition, or experiment design.
- Conclusion: supported, weak, contradicted, or not testable.

## Checks

- Never claim causality from correlation alone.
- State what evidence would change the conclusion.
