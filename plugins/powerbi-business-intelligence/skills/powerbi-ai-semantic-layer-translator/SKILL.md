---
name: powerbi-ai-semantic-layer-translator
description: Use when business language must be translated into semantic model objects, facts, dimensions, date roles, filters, measures, source fields, or certified KPI terms.
---

# Power BI AI Semantic Layer Translator

Use this skill when terms like revenue, backlog, churn, margin, delivery reliability, or cash need precise model mapping.

## Translation Pattern

1. Identify business term and synonyms.
2. Resolve domain, process, source system, and certified KPI if available.
3. Map to fact table, dimension, date role, measure, filter, and security context.
4. Identify ambiguity and competing definitions.
5. Return the accepted semantic interpretation or required clarification.

## Output Requirements

- Include term, mapped object, confidence, alternatives, and owner.
- Do not create new KPI semantics when a certified definition exists.

