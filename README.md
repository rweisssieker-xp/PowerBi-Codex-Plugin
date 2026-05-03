# AI-native Power BI Expert-Replacement Factory

AI-native Codex plugin for replacing repeatable Power BI expert, designer, data analyst, semantic modeling, DAX, Power Query/M, QA, governance, and documentation work with governed AI/KI skills.

Process Owners and Process Managers can create complete Power BI solutions without needing a dedicated expert team for every analysis request. The tool turns business and process questions into validated semantic models, KPIs, measures, DAX, Power Query/M, report pages, root-cause analysis, action cockpits, governance evidence, tests, documentation, and Power BI Desktop-validated PBIP/PBIR/TMDL artifacts.

## de-DE Kurzfassung

Dieses Repository enthaelt eine AI-native Power BI Expert-Replacement Factory. Process Owner und Process Manager koennen vollstaendige Power-BI-Loesungen erstellen, ohne fuer jede Analyse ein separates Expertenteam aus Power BI Consultant, Designer, Data Analyst, Semantic Modeler, DAX Developer, Power Query Developer, BI Tester und CoE Reviewer zu benoetigen.

Das Tool uebersetzt Business- und Prozessfragen in validierte semantische Modelle, KPI Contracts, Measures, DAX, Power Query/M, Reportseiten, Root-Cause-Analysen, Action Cockpits, Governance Evidence, Tests, Dokumentation und Power-BI-Desktop-validierte PBIP/PBIR/TMDL-Artefakte.

## What It Does

- Converts business questions into Power BI blueprints, semantic models, DAX catalogs, report layouts, validation plans, and delivery packs.
- Replaces repeatable work from Power BI consultants, report designers, data analysts, semantic modelers, DAX experts, Power Query/M developers, Fabric architects, BI testers, CoE reviewers, and BI documentation owners.
- Enables Process Owners and Process Managers to create complete Power BI process analytics from process questions, KPI definitions, source metadata, and improvement goals.
- Generates process-aligned semantic models, KPI contracts, DAX measures, Power Query sources, report pages, root-cause drilldowns, exception cockpits, and action tracking artifacts.
- Supports any Power BI-compatible source pattern: ERP, CRM, MES, PLM, WMS/WHS, QMS, EHS, EPM, treasury, ESG, data warehouses, lakehouses, APIs, files, and SaaS platforms.
- Generates native Power BI / Power Query connector designs for real sources. Excel uses the native Excel Workbook connector pattern (`Excel.Workbook(File.Contents(...), null, true)` or SharePoint/OneDrive binary-to-`Excel.Workbook`), while embedded `DATATABLE` output is reserved for offline demos and smoke tests.
- Understands industrial process chains such as Lead2Order, Order2Cash, Procure2Pay, Plan2Produce, Record2Report, Maintain2Operate, Market2Lead, Dock2Stock, Complaint2CAPA, Control2Evidence, and Data2Insight2Action.
- Adds AI/KI guardrails for NL-to-DAX, NL-to-PowerQuery, RAG grounding, hallucination checks, insight confidence, autonomous BI sprints, and process recommendations.
- Adds advanced AI/KI agents for KPI discovery, business-question generation, semantic-model refactoring, measure deduplication, DAX explainability, report personalization, insight prioritization, causal hypothesis testing, data storytelling, exception-to-action routing, forecast explanation, scenario recommendations, data-contract negotiation, source mapping, compliance review, tenant-risk prediction, adoption coaching, self-service guardrails, process digital twins, and expert-replacement scoring.
- Adds autonomous AI/KI operations for continuous improvement, BI memory, governance drift, schema drift, KPI lifecycle, remediation, business impact simulation, decision audits, data product ownership, report retirement, semantic contract validation, cross-process dependencies, root-cause playbooks, internal benchmark learning, test case mining, data stewardship, security exposure, capacity optimization, multi-agent BI orchestration, and boardroom preparation.
- Adds expert-reduction USPs for requirement-to-model automation, ERP object resolution, KPI conflict resolution, report consolidation, model certification, tenant cleanup, role prompt packs, value realization, and audit-ready AI evidence trails.
- Adds executable-factory capabilities for live metadata scanning, PBIP/TMDL generation, DAX test execution, Power Query/M generation, visual layout specs, Fabric deployment blueprints, connector capability decisions, golden semantic model templates, RLS/OLS patterns, Admin API playbooks, synthetic demo data, acceptance testing, migration cost estimates, CoE handbooks, and machine-readable skill indexing.
- Adds automation features for intake triage, requirements interviews, source metadata scans, KPI contract generation, semantic model drafting, DAX test generation, Power Query review, UX review, refresh-failure triage, schema-drift alerts, tenant cleanup, certification pipelines, release notes, documentation refresh, UAT packs, action creation, adoption monitoring, capacity optimization, security exposure scans, and executive briefings.
- Requires substantial delivery artifacts to include aligned `en-US` and `de-DE` documentation.

## Repository Structure

```text
.
├── .agents/plugins/marketplace.json
├── plugins/powerbi-business-intelligence/
│   ├── .codex-plugin/plugin.json
│   ├── README.md
│   ├── assets/
│   ├── docs/
│   └── skills/
├── docs/
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── GOVERNANCE.md
├── MAINTAINERS.md
├── RELEASE.md
├── CHANGELOG.md
├── LICENSE
└── SECURITY.md
```

## Quickstart

1. Clone the repository.
2. Open it in Codex.
3. Register the local marketplace from `.agents/plugins/marketplace.json`.
4. Install or enable the `powerbi-business-intelligence` plugin.
5. Start with one of the example prompts below.

Example prompts:

```text
Erstelle ein Power BI Modell und Dashboard fuer Customer Churn.
Plane ein Power BI Reporting fuer SAP FiCO mit Datenmodell, DAX und Seitenlayout.
Loese eine Order2Cash Fragestellung quellsystemabhaengig fuer SAP, CRM, WMS und Finance.
Baue Dock2Stock, Pick2Pack2Ship und Return2Disposition als Power BI Data Product.
Erzeuge ein Control2Evidence Cockpit mit en-US/de-DE Dokumentation.
Fuehre einen autonomen BI Sprint fuer Order2Cash von Intake bis Quality Gate durch.
```

## Core Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Skills Catalog](docs/SKILLS_CATALOG.md)
- [Process Chain KPIs](docs/PROCESS_CHAIN_KPIS.md)
- [Source System Coverage](docs/SOURCE_SYSTEM_COVERAGE.md)
- [Power BI Native Connector Coverage](docs/POWERBI_NATIVE_CONNECTOR_COVERAGE.md)
- [Expert Reduction USPs](docs/EXPERT_REDUCTION_USPS.md)
- [Process Owner AI/KI USPs](docs/PROCESS_OWNER_AI_KI_USPS.md)
- [Power BI Expert-Replacement Factory Gesamtplan](docs/POWERBI_EXPERT_REPLACEMENT_FACTORY_GESAMTPLAN.md)
- [Power BI Expert-Replacement Skill Map](docs/POWERBI_EXPERT_REPLACEMENT_SKILL_MAP.md)
- [Power BI Expert-Replacement 20 Feature Rollout](docs/POWERBI_EXPERT_REPLACEMENT_20_FEATURES.md)
- [Power BI Expert-Replacement Advanced USP Rollout](docs/POWERBI_EXPERT_REPLACEMENT_ADVANCED_USPS.md)
- [Bilingual Documentation](docs/BILINGUAL_DOCUMENTATION.md)
- [Bilingual Documentation Matrix](docs/BILINGUAL_DOCUMENTATION_MATRIX.md)
- [GitHub Documentation](docs/GITHUB_DOCUMENTATION.md)
- [GitHub Workflow](docs/GITHUB_WORKFLOW.md)
- [Governance and Quality Gates](docs/GOVERNANCE_AND_QUALITY.md)
- [Examples](docs/EXAMPLES.md)
- [Simulation Test Report](docs/SIMULATION_TEST_REPORT.md)

## Main Capability Areas

- Power BI reporting, modelling, DAX, Power Query, and Fabric architecture.
- Executable trust layer: `scripts/powerbi_expert_factory.py` for PBIP/TMDL/PBIR validation, `scripts/powerbi_desktop_smoke_test.ps1` for Desktop/Frown smoke checks, schemas for KPI/evidence/RLS/acceptance, and process-pack templates as machine-readable delivery assets.
- Expert replacement for Power BI consultants, designers, data analysts, semantic modelers, DAX experts, Power Query/M developers, Fabric architects, BI QA, CoE reviewers, and documentation owners.
- Process Owner and Process Manager self-service analytics for process performance, bottlenecks, exceptions, root cause, and action management.
- Business problem factory for Customer Churn, Material Churn, FiCO, sales, supply chain, procurement, service, HR, risk, operations, and executive reporting.
- Industrial process intelligence and source-system-aware process adapters.
- ERP/CRM/source-product catalog for SAP, Microsoft Dynamics, Salesforce, Oracle, NetSuite, Infor, IFS, Epicor, QAD, Sage, Workday, ServiceNow, HubSpot, Zendesk, Siemens, PTC, Dassault, MES/SCADA/historians, and modern data platforms.
- QM/QMS/EHS, WHS/WMS, EPM, treasury, ESG, subscription billing, field service, logistics visibility, MDM, ETL/ELT, data quality, lakehouse, ECM, OCR/IDP, RPA, and identity/security source packs.
- AI-native BI delivery with Copilot orchestration, RAG, prompt governance, hallucination guard, insight confidence, root-cause investigation, and autonomous BI sprints.

## Design Principles

- Governed reuse beats one-off reports.
- Expert replacement requires validation evidence, not only generated content.
- Process Owner autonomy beats ticket-based report queues when protected by model, DAX, M, source, and governance guardrails.
- KPI contracts come before DAX measures.
- Source-system semantics must be validated before modelling.
- Every exception KPI needs an accountable owner and action path.
- AI-generated insights must be grounded in metadata, source totals, tests, and documented assumptions.
- Large industrial BI artifacts should be documented in both `en-US` and `de-DE`.

## License

MIT. See [LICENSE](LICENSE).
