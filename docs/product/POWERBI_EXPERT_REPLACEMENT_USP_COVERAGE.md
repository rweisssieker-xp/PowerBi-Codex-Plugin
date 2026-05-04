# Power BI Expert-Replacement USP Coverage

The product differentiates through 20 generated and testable USP capabilities. The catalog is maintained in [powerbi_usp_capability_catalog.json](../../data/powerbi_usp_capability_catalog.json).

Coverage evidence is generated for every industrial process pack in [usp-capability-coverage](../../outputs/usp-capability-coverage/README.md).

Executable feature contracts are generated in [powerbi-feature-factory](../../outputs/powerbi-feature-factory/README.md). Each USP has a machine-readable input/output contract, CLI recipe, validation contract, and process mapping.

The concrete execution layer is generated in [powerbi-execution-layer](../../outputs/powerbi-execution-layer/README.md). It materializes all 20 feature contracts for every process into source profiles, native M templates, schema drift contracts, semantic compile plans, report materialization plans, DAX expected-result plans, lineage, security plans, performance budgets, acceptance packs, and build manifests.

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
