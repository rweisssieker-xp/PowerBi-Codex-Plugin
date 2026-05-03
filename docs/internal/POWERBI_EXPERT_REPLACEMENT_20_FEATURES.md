# Power BI Expert-Replacement 20 Feature Rollout

<!-- bilingual-doc-header -->
## en-US Documentation

This document tracks the first 20 feature skills that make the expert-replacement product operational and testable.

## de-DE Dokumentation

Dieses Dokument verfolgt die ersten 20 Feature-Skills, die das Expert-Replacement-Produkt operativ nutzbar und testbar machen.

<!-- /bilingual-doc-header -->


## Purpose

This document tracks the first 20 concrete features added to make the Power BI Expert-Replacement Factory operationally credible. Each feature is implemented as a dedicated Codex skill so it can be triggered, documented, tested, and expanded independently.

## de-DE Kurzfassung

Dieses Dokument beschreibt die ersten 20 konkreten Features der Power BI Expert-Replacement Factory. Jedes Feature ist als eigener Codex-Skill angelegt, damit es auffindbar, triggerbar, dokumentiert und spaeter technisch weiter ausbaubar ist.

## Implemented Feature Skills

| # | Feature | Skill |
| --- | --- | --- |
| 1 | Power BI Desktop Smoke Test Runner | `powerbi-ai-powerbi-desktop-smoke-tester` |
| 2 | Frown-to-Fix Agent | `powerbi-ai-frown-to-fix-triage` |
| 3 | Model Graph Validator | `powerbi-ai-model-graph-validator` |
| 4 | Native Source Router | `powerbi-ai-native-source-router` |
| 5 | Visual Binding Validator | `powerbi-ai-visual-binding-validator` |
| 6 | DAX Measure Test Harness | `powerbi-ai-dax-measure-test-harness` |
| 7 | KPI Contract Compiler | `powerbi-ai-kpi-contract-compiler` |
| 8 | Power Query Load Contract | `powerbi-ai-powerquery-load-contract` |
| 9 | Semantic Model Diff and Regression | `powerbi-ai-semantic-model-diff-regression` |
| 10 | Report UX Critic Agent | `powerbi-ai-report-ux-critic` |
| 11 | Process Owner Interview Wizard | `powerbi-process-owner-interview-wizard` |
| 12 | Business Question to Model | `powerbi-ai-business-question-to-model` |
| 13 | Exception-to-Action Workflow | `powerbi-ai-exception-to-action-workflow` |
| 14 | Process Pack Generator | `powerbi-ai-process-pack-generator` |
| 15 | Owner Acceptance Pack | `powerbi-ai-owner-acceptance-pack` |
| 16 | Certification Readiness Bot | `powerbi-ai-certification-readiness-bot` |
| 17 | Tenant Cleanup and Consolidation Agent | `powerbi-ai-tenant-cleanup-consolidation-agent` |
| 18 | Power BI Release Evidence Pack | `powerbi-ai-powerbi-release-evidence-pack` |
| 19 | Governed Role Prompt Packs | `powerbi-ai-governed-role-prompt-packs` |
| 20 | Expert Replacement Scorecard | `powerbi-ai-expert-replacement-scorecard` |

## Implementation Standard

Each feature skill defines:

- when to use it;
- what expert work it replaces;
- checks, fields, or workflow steps;
- required outputs;
- quality or evidence requirements.

## Executable Trust Layer

The first real implementation layer now exists and should be used by the trust-layer skills before claiming a generated artifact is release-ready:

- `scripts/powerbi_expert_factory.py validate` parses PBIP/TMDL/PBIR projects and validates model graph, native sources, visual bindings, and static DAX risk.
- `scripts/powerbi_expert_factory.py evidence` writes compact release evidence events.
- `scripts/powerbi_desktop_smoke_test.ps1` opens a PBIP in Power BI Desktop and checks whether a new Frown snapshot appears.
- `schemas/kpi_contract.schema.json`, `schemas/evidence_event.schema.json`, `schemas/orchestration_handoff.schema.json`, `schemas/rls_test_case.schema.json`, and `schemas/golden_acceptance.schema.json` define contracts for governed expert replacement.
- `data/powerbi_connector_matrix.json` provides a real connector decision source for native Power Query routing.
- `templates/process_packs/*.json`, `templates/refactor_pipeline.json`, `templates/report_visual_qa_checklist.json`, and `templates/admin_api_tenant_scan_plan.json` make process packs, refactoring, visual QA, and tenant scanning machine-readable.
