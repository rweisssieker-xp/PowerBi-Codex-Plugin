# GitHub Workflow

<!-- bilingual-doc-header -->
## en-US Documentation

This document defines how GitHub issues, pull requests, reviews, and repository governance should be used for the Power BI Expert-Replacement Factory.

## de-DE Dokumentation

Dieses Dokument definiert, wie GitHub Issues, Pull Requests, Reviews und Repository-Governance fuer die Power BI Expert-Replacement Factory genutzt werden sollen.

<!-- /bilingual-doc-header -->

## en-US

## Issue Types

- Use `Bug report` for reproducible defects in docs, skills, scripts, schemas, templates, or generated Power BI artifacts.
- Use `Feature request` for new capabilities, validators, skills, or documentation improvements.
- Use `Process pack request` for Lead2Order, Order2Cash, Procure2Pay, Record2Report, and other process analytics packs.
- Do not open public issues for secrets, vulnerabilities, customer data, tenant IDs, credentials, or confidential screenshots.

## Pull Request Rules

- Keep PR scope narrow and explain the Power BI expert-replacement capability being changed.
- Include `en-US` and `de-DE` documentation for substantial changes.
- Run relevant validation before review:
  - JSON parse checks.
  - Markdown link checks.
  - Skill frontmatter checks.
  - Relevant unit tests.
  - PBIP/TMDL/PBIR validation when Power BI artifacts are touched.
- Add evidence for generated artifacts and quality gates.

## Review Focus

Reviewers should prioritize:

- Correct Power BI modelling patterns.
- DAX and Power Query/M risks.
- Native source routing and credential safety.
- Broken visual bindings.
- Ambiguous relationship paths.
- Bilingual documentation completeness.
- No secrets or customer-sensitive data.

## de-DE

## Issue-Typen

- Nutze `Bug report` fuer reproduzierbare Fehler in Doku, Skills, Scripts, Schemas, Templates oder generierten Power-BI-Artefakten.
- Nutze `Feature request` fuer neue Faehigkeiten, Validatoren, Skills oder Dokumentationsverbesserungen.
- Nutze `Process pack request` fuer Lead2Order, Order2Cash, Procure2Pay, Record2Report und weitere Process-Analytics-Packs.
- Oeffne keine oeffentlichen Issues fuer Secrets, Vulnerabilities, Kundendaten, Tenant IDs, Credentials oder vertrauliche Screenshots.

## Pull-Request-Regeln

- Halte PRs eng geschnitten und erklaere, welche Power-BI-Expert-Replacement-Faehigkeit geaendert wird.
- Ergaenze `en-US` und `de-DE` Dokumentation fuer wesentliche Aenderungen.
- Fuehre vor dem Review relevante Validierung aus:
  - JSON-Parse-Checks.
  - Markdown-Link-Checks.
  - Skill-Frontmatter-Checks.
  - Relevante Unit Tests.
  - PBIP/TMDL/PBIR-Validierung, wenn Power-BI-Artefakte betroffen sind.
- Fuege Evidence fuer generierte Artefakte und Quality Gates hinzu.

## Review-Fokus

Reviewer priorisieren:

- Korrekte Power-BI-Modellierungsmuster.
- DAX- und Power-Query/M-Risiken.
- Native Source Routing und Credential Safety.
- Defekte Visual Bindings.
- Ambiguous Relationship Paths.
- Vollstaendige zweisprachige Dokumentation.
- Keine Secrets oder kundensensitiven Daten.

