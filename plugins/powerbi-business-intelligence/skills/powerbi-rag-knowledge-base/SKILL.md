---
name: powerbi-rag-knowledge-base
description: Use when AI/KI answers should retrieve from enterprise BI knowledge such as KPI catalogs, semantic models, report docs, source metadata, glossary, tickets, acceptance evidence, CoE standards, or process documentation.
---

# Power BI RAG Knowledge Base

Use this skill when an AI answer must be grounded in enterprise BI artifacts.

## Knowledge Sources

- KPI contracts and glossary.
- Semantic model/TMDL/PBIP/DAX/Power Query.
- Report specs and screenshots.
- Source metadata and data contracts.
- Quality gates, acceptance packs, compliance evidence.
- Tickets, incidents, data quality issues, CoE rules.

## Output Requirements

- Include retrieved evidence, source artifact, confidence, and unresolved gaps.
- Distinguish retrieved facts from model inference.
- Do not answer source-specific questions without retrieval or an explicit assumption label.

