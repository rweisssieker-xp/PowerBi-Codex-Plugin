# Bilingual Documentation Matrix

<!-- bilingual-doc-header -->
## en-US Documentation

This matrix shows the bilingual coverage status for repository documentation. Markdown documents must contain explicit `en-US` and `de-DE` sections. Technical object names, file paths, script names, skill IDs, table names, measure IDs, DAX, M, JSON keys, and API scopes remain language-neutral.

## de-DE Dokumentation

Diese Matrix zeigt den Status der zweisprachigen Dokumentationsabdeckung im Repository. Markdown-Dokumente muessen explizite `en-US`- und `de-DE`-Abschnitte enthalten. Technische Objektnamen, Dateipfade, Scriptnamen, Skill-IDs, Tabellennamen, Measure-IDs, DAX, M, JSON-Keys und API-Scopes bleiben sprachneutral.

<!-- /bilingual-doc-header -->

## Coverage Rules

| Rule | en-US | de-DE |
| --- | --- | --- |
| Markdown documentation | Must include an explicit `en-US` section or bilingual header | Muss einen expliziten `de-DE`-Abschnitt oder bilingualen Kopf enthalten |
| Generated delivery artifacts | Must use aligned sections and matching structure | Muss abgestimmte Abschnitte und gleiche Struktur verwenden |
| Technical IDs | Remain unchanged | Bleiben unveraendert |
| Business explanations | Written in English | Werden auf Deutsch bereitgestellt |
| Acceptance and governance evidence | Available for international review | Fuer deutschsprachige Abnahme verfuegbar |

## Repository Documentation

Same Markdown paths as [DOCUMENTATION.md](DOCUMENTATION.md); this table tracks **bilingual coverage only** (not navigation).

| Document | Bilingual status | Notes |
| --- | --- | --- |
| `README.md` | Required | Repository entry point; includes English and German positioning |
| `DOCUMENTATION.md` | Complete | Root documentation navigation |
| `INSTALLATION.md` | Complete | Root installation entry point |
| `USAGE.md` | Complete | Root usage entry point |
| `ARCHITECTURE.md` | Complete | Root architecture entry point |
| `BILINGUAL_DOCUMENTATION.md` | Complete | Bilingual documentation standard |
| `BILINGUAL_DOCUMENTATION_MATRIX.md` | Complete | Coverage matrix |
| `EXAMPLES.md` | Complete | Example usage scope |
| `EXPERT_REDUCTION_USPS.md` | Complete | Expert replacement/reduction summary |
| `GITHUB_DOCUMENTATION.md` | Complete | GitHub standard document and template inventory |
| `GITHUB_WORKFLOW.md` | Complete | GitHub issue, PR, review, and repository governance workflow |
| `GOVERNANCE_AND_QUALITY.md` | Complete | Governance summary |
| `POWERBI_EXPERT_REPLACEMENT_20_FEATURES.md` | Complete | Feature rollout summary |
| `POWERBI_EXPERT_REPLACEMENT_ADVANCED_USPS.md` | Complete | Advanced USP rollout summary |
| `POWERBI_EXPERT_REPLACEMENT_FACTORY_GESAMTPLAN.md` | Complete | Master plan summary |
| `POWERBI_EXPERT_REPLACEMENT_SKILL_MAP.md` | Complete | Skill map summary |
| `POWERBI_NATIVE_CONNECTOR_COVERAGE.md` | Complete | Native connector rules |
| `PROCESS_CHAIN_KPIS.md` | Complete | Process-chain KPI summary |
| `PROCESS_OWNER_AI_KI_USPS.md` | Complete | Process-owner AI/KI USP summary |
| `SIMULATION_TEST_REPORT.md` | Complete | Simulation test report |
| `SKILLS_CATALOG.md` | Complete | Skills catalog |
| `SOURCE_SYSTEM_COVERAGE.md` | Complete | Source-system coverage summary |
| `plugins/powerbi-business-intelligence/README.md` | Required | Plugin entry point; includes English and German positioning |
| `CODE_OF_CONDUCT.md` | Complete | Collaboration and enforcement standard |
| `AUTHORS.md` | Complete | Maintainer and contributor authorship note |
| `NOTICE.md` | Complete | Product and trademark notice |
| `FAQ.md` | Complete | Root frequently asked questions |
| `GOVERNANCE.md` | Complete | Repository decision and maintainer governance |
| `MAINTAINERS.md` | Complete | Maintainer model and review expectations |
| `RELEASE.md` | Complete | Release readiness and release-note process |
| `ROADMAP.md` | Complete | Root roadmap entry point |
| `SUPPORT.md` | Complete | Support and escalation guidance |

## Machine-Readable Artifacts

| Artifact | Language handling | Reason |
| --- | --- | --- |
| `schemas/*.schema.json` | Language-neutral | JSON schema keys must remain stable |
| `data/powerbi_connector_matrix.json` | Language-neutral with English labels | Connector names and M functions are technical identifiers |
| `templates/process_packs/*.json` | Language-neutral with business labels | Process pack fields are consumed by automation |
| `scripts/*.py`, `scripts/*.ps1` | Language-neutral | Executable scripts use stable command and JSON names |

## de-DE Hinweise

- Fachliche Erklaerungen werden deutsch ergaenzt.
- Technische Namen werden nicht uebersetzt, damit Power BI, TMDL, PBIR, DAX und M stabil bleiben.
- Fuer Kundenartefakte sollen `artifact.en-US.md` und `artifact.de-DE.md` parallel erzeugt werden.
