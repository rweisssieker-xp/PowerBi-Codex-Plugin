# Power BI Expert-Replacement USP Coverage

The product differentiates through 20 generated and testable USP capabilities. The catalog is maintained in [powerbi_usp_capability_catalog.json](../../data/powerbi_usp_capability_catalog.json).

Coverage evidence is generated for every industrial process pack in [usp-capability-coverage](../../outputs/usp-capability-coverage/README.md).

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
