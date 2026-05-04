# Power BI Expert-Replacement USP Coverage

The product differentiates through 20 generated and testable USP capabilities. The catalog is maintained in [powerbi_usp_capability_catalog.json](../../data/powerbi_usp_capability_catalog.json).

Coverage evidence is generated for every industrial process pack in [usp-capability-coverage](../../outputs/usp-capability-coverage/README.md).

Executable feature contracts are generated in [powerbi-feature-factory](../../outputs/powerbi-feature-factory/README.md). Each USP has a machine-readable input/output contract, CLI recipe, validation contract, and process mapping.

The concrete execution layer is generated in [powerbi-execution-layer](../../outputs/powerbi-execution-layer/README.md). It materializes all 20 feature contracts for every process into source profiles, native M templates, schema drift contracts, semantic compile plans, report materialization plans, DAX expected-result plans, lineage, security plans, performance budgets, acceptance packs, and build manifests.

The premium USP layer is generated in [powerbi-premium-usp-layer](../../outputs/powerbi-premium-usp-layer/README.md). It adds 25 higher-order differentiators such as real connector runtime, credential-safe profiling, AI field mapping, process-mining import, KPI ontology, PBIR materialization, full PBIP generation, Power BI Desktop log parsing, report scoring, tenant readiness, deployment automation, data contracts, compliance packs, and Fabric scaffolds.

The runtime max layer is generated in [powerbi-runtime-max-layer](../../outputs/powerbi-runtime-max-layer/README.md). It expands the product to 70 maximum expert-replacement USPs for repeatable Data Analyst, Power BI Expert, and Power BI Developer work: intake-to-model autopilot, source discovery, field mapping, KPI ontology, root-cause paths, insight narratives, generated PBIP/PBIR/TMDL skeletons for every process, DAX/M factories, validation gates, semantic auto-repair, RLS, action cockpits, deployment, documentation, acceptance evidence, release decisions, continuous improvement backlogs, legacy reverse engineering, dashboard consolidation, business-question simulation, KPI dispute resolution, semantic refactoring, executive board packs, performance engineering, refresh triage, data contracts, UX critique, DAX explainability, impact analysis, RLS/OLS attack simulation, CoE certification, Fabric cost guardrails, data marts, benchmarks, audit evidence, adoption tracking, autonomous BI sprint management, PBIX intake, tenant scanning, REST deployment, TOM/TMSL bridges, DAX execution, query folding, incremental refresh, composite models, rollback, gateway audit, Purview classification, data quality profiling, anomaly detection, forecasting, metric-store sync, enterprise glossary sync, ticketing, access review, usage-based refactoring, and multi-tenant MSP operations.

The production hardening layer is generated in [powerbi-production-hardening](../../outputs/powerbi-production-hardening/README.md). It turns the remaining release-readiness gaps into process-level evidence for Desktop smoke automation, live connector execution, credential-safe sessions, PBIP/PBIR schema validation, DAX evaluation, report layout scoring, semantic repair patches, Frown ZIP parsing, source-to-PBIP E2E evidence, plugin UX, Fabric deployment, RLS role generation, process-mining adapters, data contract enforcement, and release dashboards.

## The 20 USP Capabilities

1. One-Click Process-to-PBIP
2. Connector-Aware Source Interview
3. KPI Contract Negotiator
4. Ambiguous-Path Prevention Engine
5. Frown-to-Fix Knowledge Loop
6. Visual Binding Compiler
7. Measure Test Harness
8. Process Digital Twin Layer
9. Action Cockpit Generator
10. RLS/OLS Policy Generator
11. Source-to-KPI Lineage
12. Process Pack Marketplace
13. Industry Variant Packs
14. Power BI CoE Certification Bot
15. Report Consolidation AI
16. Semantic Model Refactoring
17. Query Folding Verifier
18. Refresh Failure Triage
19. Business Value Realization Tracker
20. Boardroom Narrative Generator

## Evidence Model

Each USP defines:

- capability ID,
- name,
- summary,
- required artifacts,
- evidence expected from generated files.

Each process coverage file maps all 20 capabilities to the generated factory artifacts for that process. CI fails if a process has incomplete USP coverage.

## Executable Feature Layer

The feature layer turns every USP into a testable delivery unit:

- `data/powerbi_feature_catalog.json`: all 20 executable USP features.
- `outputs/powerbi-feature-factory/feature_index.csv`: feature index for tooling.
- `outputs/powerbi-feature-factory/process_feature_matrix.csv`: all 20 features mapped to every industrial process.
- `outputs/powerbi-feature-factory/<feature>/feature_contract.json`: feature inputs, outputs, artifacts, evidence, and commands.
- `outputs/powerbi-feature-factory/<feature>/validation_contract.json`: release-readiness checks.
- `outputs/powerbi-feature-factory/<feature>/cli_recipe.md`: local execution recipe.

Use the CLI to create a process-specific delivery plan:

```powershell
python scripts\powerbi_expert_factory.py feature-plan --process lead-to-order --out outputs\powerbi-feature-factory\lead-to-order-feature-plan.json
```

Use the CLI to create a local delivery bundle from the execution layer:

```powershell
python scripts\powerbi_expert_factory.py build --process lead-to-order --source demo --out outputs\local-builds\lead-to-order
```

Use the CLI to create a process-specific premium USP plan:

```powershell
python scripts\powerbi_expert_factory.py premium-usp-plan --process lead-to-order --out outputs\powerbi-premium-usp-layer\lead-to-order-premium-usp-plan.json
```

Use the CLI to inspect a process-specific runtime max build:

```powershell
python scripts\powerbi_expert_factory.py runtime-max-plan --process lead-to-order --out outputs\powerbi-runtime-max-layer\lead-to-order-runtime-max-plan.json
```

Use the CLI to inspect production-hardening readiness:

```powershell
python scripts\powerbi_expert_factory.py hardening-plan --process lead-to-order --out outputs\powerbi-production-hardening\lead-to-order-hardening-plan.json
```
