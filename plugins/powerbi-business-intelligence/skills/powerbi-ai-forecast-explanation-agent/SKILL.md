---
name: powerbi-ai-forecast-explanation-agent
description: Use when Power BI forecasts or plan variances need AI explanations by mix, volume, price, capacity, supply, demand, seasonality, backlog, and data quality.
---

# Power BI AI Forecast Explanation Agent

Explain why forecast, plan, or actuals differ.

## Output Contract

- Forecast object, horizon, baseline, actual/plan comparison, and variance.
- Driver decomposition: volume, price, mix, capacity, supply, demand, backlog, timing, seasonality, and data quality.
- Confidence, evidence, counterevidence, and missing data.
- Recommended scenario or action.

## Checks

- Separate forecast error from execution variance.
- Flag where model features or source history are insufficient.
