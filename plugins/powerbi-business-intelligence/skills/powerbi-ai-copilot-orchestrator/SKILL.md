---
name: powerbi-ai-copilot-orchestrator
description: Use when AI/KI should route Power BI work across virtual agents, expert roles, source systems, semantic modelling, DAX, reports, quality gates, governance, and evidence checks.
---

# Power BI AI Copilot Orchestrator

Use this skill as the AI front door for complex Power BI requests.

## Orchestration Pattern

- Classify intent: question, build, review, fix, govern, explain, automate.
- Select expert roles: SAP/source, model, DAX, report, process, finance, quality, security, CoE.
- Define evidence required before claims are accepted.
- Route to the smallest set of skills needed.
- Merge outputs into one decision-ready answer.

## Output Requirements

- Include selected agents/skills, reason, required evidence, blockers, and final synthesis.
- Never let a generated answer bypass quality gate, source metadata, KPI contract, or test evidence when those are material.

