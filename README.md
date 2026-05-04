# AI-native Power BI Expert-Replacement Factory

[![CI](https://github.com/rweisssieker-xp/PowerBi-Codex-Plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/rweisssieker-xp/PowerBi-Codex-Plugin/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python tests](https://img.shields.io/badge/tests-unittest-blue.svg)](tests/test_powerbi_expert_factory.py)
[![Power BI validation](https://img.shields.io/badge/Power%20BI%20validation-PBIP%20static%20checks-blueviolet.svg)](scripts/powerbi_expert_factory.py)

Codex plugin for replacing repeatable Power BI expert, designer, data analyst, semantic modeling, DAX, Power Query/M, QA, governance, and documentation work with governed AI skills.

The product turns business and process questions into validated Power BI delivery artifacts: source analysis, semantic models, KPI contracts, DAX measures, Power Query/M designs, report layouts, root-cause paths, action cockpits, governance evidence, tests, documentation, and PBIP/PBIR/TMDL output.

## What It Does

- Converts process questions into Power BI blueprints, semantic models, KPI contracts, DAX catalogs, report layouts, and validation packs.
- Supports Process Owners and Process Managers without requiring a dedicated Power BI expert team for every analysis request.
- Replaces repeatable delivery work from Power BI consultants, report designers, data analysts, semantic modelers, DAX experts, Power Query/M developers, Fabric architects, BI testers, CoE reviewers, and documentation owners.
- Generates native Power BI / Power Query connector designs for real sources. Excel uses native `Excel.Workbook(File.Contents(...), null, true)` or SharePoint/OneDrive binary-to-`Excel.Workbook` patterns.
- Covers industrial process chains such as Lead2Order, Order2Cash, Procure2Pay, Plan2Produce, Record2Report, Maintain2Operate, Market2Lead, Dock2Stock, Complaint2CAPA, Control2Evidence, and Data2Insight2Action.
- Provides a machine-readable industrial process catalog and synthetic demo data for 32 process chains under `data/industry_process_catalog.json` and `outputs/industry-demo-data/`.
- Provides generated Power BI process-pack specifications for all 32 process chains under `outputs/industry-process-packs/`.
- Provides production source-routing recommendations for native Power BI sources under `data/powerbi_source_capability_matrix.json` and `outputs/source-routing/`.
- Provides a 20-USP capability catalog and process-level coverage evidence under `data/powerbi_usp_capability_catalog.json` and `outputs/usp-capability-coverage/`.
- Provides executable feature contracts for all 20 USPs under `data/powerbi_feature_catalog.json` and `outputs/powerbi-feature-factory/`.
- Provides a concrete execution layer for all 20 features and all 32 processes under `outputs/powerbi-execution-layer/`, including source profiles, M templates, schema drift contracts, semantic compile plans, report materialization plans, DAX test plans, lineage, performance budgets, process-owner acceptance packs, and build manifests.
- Provides a 25-capability Premium USP layer under `data/powerbi_premium_usp_catalog.json` and `outputs/powerbi-premium-usp-layer/`, including connector runtime, credential-safe profiling, AI field mapping, PBIP generation, PBIR materialization, Desktop log parsing, report scoring, deployment automation, data contracts, compliance packs, and Fabric scaffolds.
- Provides a 70-USP Runtime Max layer under `data/powerbi_runtime_max_catalog.json` and `outputs/powerbi-runtime-max-layer/`, including analyst/developer replacement contracts, generated PBIP/PBIR/TMDL skeletons for all 32 processes, intake-to-model autopilot, source discovery, KPI ontology, DAX/M factories, validation gates, semantic auto-repair, RLS, action cockpits, deployment, documentation, acceptance evidence, release decisions, continuous improvement backlogs, legacy reverse engineering, dashboard consolidation, performance engineering, certification, benchmarks, cost guardrails, adoption tracking, autonomous BI sprint management, PBIX intake, tenant scanning, REST deployment, TOM/TMSL bridges, DAX execution, query folding, gateway audit, Purview classification, data quality, anomaly detection, forecasting, ticketing, access review, and multi-tenant MSP operations.
- Maps all 70 Runtime Max USPs to plugin skills, CLI entrypoints, and output artifacts in `data/powerbi_runtime_usp_skill_matrix.json`.
- Provides two operating modes: `Experten Mode` for senior Power BI/Fabric engineering control and `Generalisten Mode` for Process Managers / Process Owners who want autonomous request-to-report delivery.
- Provides a 15-capability Production Hardening layer under `data/powerbi_production_hardening_catalog.json` and `outputs/powerbi-production-hardening/`, including Desktop smoke contracts, live connector execution contracts, credential-safe runtime policy, PBIP/PBIR schema validation, DAX evaluation contracts, layout scoring, auto-repair patches, Frown ZIP parsing, source-to-PBIP evidence, plugin UX workflow, Fabric deployment, RLS role generation, process-mining adapters, data contract enforcement, and release dashboards.
- Provides a 30-USP Market Differentiator layer under `data/powerbi_market_differentiator_usp_catalog.json` and `outputs/powerbi-market-differentiator-usps/`, including process digital twin, KPI contract negotiation, root-cause narrative, value-at-risk prioritization, autonomous action boards, benchmark twins, evidence vaults, process mining bridges, predictive SLA radar, what-if simulation, governance-by-design, and board-to-action cascade evidence.
- Provides a concrete Lead2Order Power BI analysis package under `outputs/lead2order-powerbi-analysis/`, including PBIP/PBIR/TMDL output, 30 governed DAX measures, 10 process-owner problem questions, 6 report pages, and zero-warning static validation evidence.
- Adds executable trust checks for model graph quality, native source routing, visual bindings, DAX static checks, and Power BI Desktop smoke validation workflows.

## Repository Structure

```text
.
├── .agents/plugins/marketplace.json
├── .github/
├── plugins/powerbi-business-intelligence/
│   ├── .codex-plugin/plugin.json
│   ├── README.md
│   ├── assets/
│   ├── docs/
│   └── skills/
├── docs/
│   ├── product/
│   └── internal/
├── schemas/
├── templates/
├── scripts/
├── tests/
├── data/
├── outputs/
├── DOCUMENTATION.md
├── LICENSE
└── *.md
```

## Documentation

Start with [DOCUMENTATION.md](DOCUMENTATION.md). It is the single navigation index for repository-level documentation. Detailed product documentation lives under [docs/product](docs/product/README.md); maintainer-oriented internal notes live under [docs/internal](docs/internal/README.md).

Key guides:

- [Installation](INSTALLATION.md)
- [Usage](USAGE.md)
- [Architecture](ARCHITECTURE.md)
- [Process Chain KPIs](docs/product/PROCESS_CHAIN_KPIS.md)
- [Industry Demo Data](outputs/industry-demo-data/README.md)
- [Industry Process Packs](outputs/industry-process-packs/README.md)
- [Power BI Source Routing](outputs/source-routing/README.md)
- [USP Capability Coverage](outputs/usp-capability-coverage/README.md)
- [Power BI Feature Factory](outputs/powerbi-feature-factory/README.md)
- [Power BI Execution Layer](outputs/powerbi-execution-layer/README.md)
- [Power BI Premium USP Layer](outputs/powerbi-premium-usp-layer/README.md)
- [Power BI Runtime Max Layer](outputs/powerbi-runtime-max-layer/README.md)
- [Power BI Production Hardening](outputs/powerbi-production-hardening/README.md)
- [Power BI Market Differentiator USPs](outputs/powerbi-market-differentiator-usps/README.md)
- [Lead2Order Power BI Analysis Package](outputs/lead2order-powerbi-analysis/README.md)
- [Skills Catalog](docs/product/SKILLS_CATALOG.md)
- [Power BI Expert-Replacement Factory Plan](docs/product/POWERBI_EXPERT_REPLACEMENT_FACTORY_GESAMTPLAN.md)
- [Power BI Expert-Replacement Skill Map](docs/product/POWERBI_EXPERT_REPLACEMENT_SKILL_MAP.md)

## Quickstart

1. Clone the repository.
2. Open it in Codex.
3. Register the local marketplace from `.agents/plugins/marketplace.json`.
4. Install or enable the `powerbi-business-intelligence` plugin.
5. Start with a process analytics request.

Example prompts:

```text
Create a Power BI model and dashboard for customer churn.
Plan a Power BI reporting solution for SAP FiCO with data model, DAX, and page layout.
Build a source-aware Order2Cash analytics pack for SAP, CRM, WMS, and Finance.
Create a Control2Evidence cockpit with KPI contracts, DAX measures, and validation gates.
Run an autonomous BI sprint for Order2Cash from intake to quality gate.
```

## Validation

Run the core test suite:

```powershell
python -m unittest tests\test_powerbi_expert_factory.py -v
```

Run repository checks:

```powershell
python scripts\ci_repository_checks.py
```

Regenerate industrial process demo data and pack specifications:

```powershell
python scripts\build_industry_process_demo_data.py
python scripts\build_industry_process_packs.py
python scripts\build_powerbi_source_routing.py
python scripts\build_usp_capability_coverage.py
python scripts\build_powerbi_feature_factory.py
python scripts\build_powerbi_execution_layer.py
python scripts\build_powerbi_premium_usp_layer.py
python scripts\build_powerbi_runtime_max_layer.py
python scripts\build_powerbi_production_hardening_layer.py
python scripts\build_powerbi_market_differentiator_usps.py
python scripts\build_lead2order_powerbi_analysis.py
```

Run the sample PBIP validation:

```powershell
python scripts\powerbi_expert_factory.py validate --project outputs\powerbi-order2cash-pbip\Order2Cash_NativeExcel --out outputs\powerbi-order2cash-pbip\expert_factory_validation.json
python scripts\powerbi_expert_factory.py report-package --process lead-to-order --sources "Excel export and SAP CRM opportunity extract" --goal "Process owner cockpit for conversion, aging, SLA breaches, and next actions" --out outputs\report-packages\lead-to-order
python scripts\powerbi_expert_factory.py feature-plan --process lead-to-order --out outputs\powerbi-feature-factory\lead-to-order-feature-plan.json
python scripts\powerbi_expert_factory.py build --process lead-to-order --source demo --out outputs\local-builds\lead-to-order
python scripts\powerbi_expert_factory.py premium-usp-plan --process lead-to-order --out outputs\powerbi-premium-usp-layer\lead-to-order-premium-usp-plan.json
python scripts\powerbi_expert_factory.py runtime-max-plan --process lead-to-order --out outputs\powerbi-runtime-max-layer\lead-to-order-runtime-max-plan.json
python scripts\powerbi_expert_factory.py hardening-plan --process lead-to-order --out outputs\powerbi-production-hardening\lead-to-order-hardening-plan.json
python scripts\powerbi_expert_factory.py market-usp-plan --process lead-to-order --out outputs\powerbi-market-differentiator-usps\lead-to-order-market-usp-plan.json
python scripts\powerbi_expert_factory.py validate --project outputs\lead2order-powerbi-analysis\pbip\Lead2OrderAnalysis --out outputs\lead2order-powerbi-analysis\validation_result.json
```

Create credential-safe runtime executor evidence and API request payloads:

```powershell
python scripts\powerbi_expert_factory.py pbix-intake --file .\sample.pbix --out outputs\runtime-executors\sample-pbix-intake.json
python scripts\powerbi_expert_factory.py tenant-scan-request --tenant <tenant-id> --workspace <workspace-id> --out outputs\runtime-executors\tenant-scan-request.json
python scripts\powerbi_expert_factory.py dax-query-request --workspace <workspace-id> --dataset <dataset-id> --query "EVALUATE ROW(\"Cases\", [Case Count])" --out outputs\runtime-executors\dax-query-request.json
python scripts\powerbi_expert_factory.py rest-deploy-request --workspace <workspace-id> --artifact outputs\powerbi-runtime-max-layer\processes\lead2order\pbip\Lead2Order --operation import --operation refresh --out outputs\runtime-executors\rest-deploy-request.json
python scripts\powerbi_expert_factory.py gateway-audit-request --gateway <gateway-id> --datasource <datasource-id> --out outputs\runtime-executors\gateway-audit-request.json
```

Run authenticated executors when `POWERBI_ACCESS_TOKEN` is set; otherwise they return dry-run evidence:

```powershell
python scripts\powerbi_expert_factory.py generalist-autopilot-run --process lead-to-order --sources "Excel export and SAP CRM opportunity extract" --goal "Process owner cockpit for conversion, aging, SLA breaches, and next actions" --out outputs\autopilot-runs\lead-to-order
python scripts\powerbi_expert_factory.py generalist-prompt-run --prompt "O2C has constant operational pressure. Orders are stuck, deliveries are late, cash is not coming in, invoices are blocked, sources are SAP export, Excel disputes, and warehouse CSV. Build a Monday cockpit for process owners." --out outputs\autopilot-runs\human-o2c-monday-cockpit
python scripts\powerbi_expert_factory.py tenant-scan-run --tenant <tenant-id> --workspace <workspace-id> --out outputs\runtime-executors\tenant-scan-run.json
python scripts\powerbi_expert_factory.py dax-query-run --workspace <workspace-id> --dataset <dataset-id> --query "EVALUATE ROW(\"Cases\", [Case Count])" --out outputs\runtime-executors\dax-query-run.json
python scripts\powerbi_expert_factory.py rest-deploy-run --workspace <workspace-id> --artifact outputs\report-packages\lead-to-order\pbip\Lead2Order --operation import --operation refresh --out outputs\runtime-executors\rest-deploy-run.json
python scripts\powerbi_expert_factory.py gateway-audit-run --gateway <gateway-id> --datasource <datasource-id> --out outputs\runtime-executors\gateway-audit-run.json
```

## Design Principles

- Governed reuse beats one-off reports.
- Expert replacement requires validation evidence, not only generated content.
- KPI contracts come before DAX measures.
- Source-system semantics must be validated before modeling.
- Star-schema model quality comes before report design.
- Every exception KPI needs an accountable owner and action path.
- AI-generated insights must be grounded in metadata, source totals, tests, and documented assumptions.

## License

MIT. See [LICENSE](LICENSE).
