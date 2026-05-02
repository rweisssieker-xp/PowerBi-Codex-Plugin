---
name: powerbi-bilingual-documentation
description: Use when Power BI artifacts, skills, delivery packs, reports, governance documents, training, acceptance evidence, or AI/KI outputs need matching documentation in en-US and de-DE.
---

# Power BI Bilingual Documentation

Use this skill whenever the plugin creates or updates documentation, specs, delivery packs, report text, glossary terms, training, acceptance packs, governance artifacts, prompts, or AI/KI outputs.

## Required Languages

- `en-US`: primary international enterprise documentation.
- `de-DE`: German documentation for German-speaking stakeholders.

## Required Structure

Every substantial artifact should include:

1. English section/file: purpose, scope, owners, inputs, outputs, assumptions, validation, risks, next steps.
2. German section/file: same content, adapted terminology, not a partial summary.
3. Terminology table: business terms, KPI names, source-system terms, approved translations.
4. Non-translatable terms: source object names, system IDs, table names, field names, DAX names, API names.

## Output Requirements

- Use headings `## en-US` and `## de-DE` for compact artifacts.
- Use paired files for larger artifacts: `README.en-US.md` and `README.de-DE.md`, or `<artifact>.en-US.md` and `<artifact>.de-DE.md`.
- Keep KPI names, glossary terms, report titles, acceptance criteria, quality gates, and owner responsibilities aligned across both languages.
- Mark untranslated or disputed terms as `Translation review required`.

