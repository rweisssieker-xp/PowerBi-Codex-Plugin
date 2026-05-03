# Power BI Expert-Replacement Factory Gesamtplan

<!-- bilingual-doc-header -->
## en-US Documentation

This is the master plan for the AI/KI Power BI Expert-Replacement Factory. It defines target roles, replacement scope, skill clusters, trust layer, executable engine layer, O2C proof, roadmap, and governance boundary.

## de-DE Dokumentation

Dies ist der Gesamtplan fuer die AI/KI Power BI Expert-Replacement Factory. Er definiert Zielrollen, Ersatzumfang, Skill-Cluster, Trust Layer, ausfuehrbare Engine-Schicht, O2C-Proof, Roadmap und Governance-Grenzen.

<!-- /bilingual-doc-header -->


## en-US Positioning

The product is an AI/KI Power BI Expert-Replacement Factory. It enables Process Owners and Process Managers to create complete governed Power BI solutions without a dedicated expert team for every analysis request. The tool replaces repeatable expert work normally performed by Power BI consultants, semantic modelers, DAX experts, Power Query developers, report designers, data analysts, BI testers, CoE reviewers, and BI documentation owners.

The operating promise is: business or process question in, validated Power BI artifact out. The artifact includes source analysis, native connector design, semantic model, KPI contracts, measures, DAX, Power Query/M, report pages, visuals, root-cause paths, action cockpit, governance evidence, tests, documentation, and Power BI Desktop-validated PBIP/PBIR/TMDL output.

## de-DE Positionierung

Das Produkt ist eine AI/KI Power BI Expert-Replacement Factory. Process Owner und Process Manager koennen vollstaendige, governance-faehige Power-BI-Loesungen erzeugen, ohne fuer jede Analyse ein separates Power-BI-Expertenteam zu benoetigen. Das Tool ersetzt wiederholbare Expertenarbeit von Power BI Consultants, Semantic Modelern, DAX Experts, Power Query/M Developers, Report Designern, Data Analysts, BI Testern, CoE Reviewern und BI Documentation Ownern.

Das Leistungsversprechen lautet: Business- oder Prozessfrage rein, validiertes Power-BI-Artefakt raus. Das Ergebnis umfasst Quellenanalyse, natives Connector-Design, semantisches Modell, KPI Contracts, Measures, DAX, Power Query/M, Reportseiten, Visuals, Root-Cause-Pfade, Action Cockpit, Governance Evidence, Tests, Dokumentation und Power-BI-Desktop-validierte PBIP/PBIR/TMDL-Ausgabe.

## Expert Roles Replaced

| Expert role replaced | Replacement outcome | Existing coverage | Planned AI/KI expert agents |
| --- | --- | --- | --- |
| Power BI Consultant | Scope, delivery plan, stakeholder framing, artifact backlog | `powerbi-business-problem-factory`, `powerbi-requirement-to-model-autopilot`, `powerbi-intake-router`, `powerbi-delivery-factory` | `powerbi-ai-powerbi-consultant-agent`, `powerbi-ai-solution-scope-agent`, `powerbi-ai-requirement-to-delivery-plan` |
| Data Analyst | Business-question decomposition, insight plan, analysis narrative, root-cause logic | `powerbi-ai-business-question-generator`, `powerbi-ai-insight-prioritization-engine`, `powerbi-ai-data-story-generator`, `powerbi-ai-root-cause-investigator` | `powerbi-ai-data-analyst-agent`, `powerbi-ai-analysis-plan-builder`, `powerbi-ai-insight-to-measure-translator`, `powerbi-ai-statistical-interpretation-guard` |
| Power BI Designer | Report layout, visual choice, drill paths, storytelling, mobile view | `powerbi-reporting`, `powerbi-auto-report-layout-generator`, `powerbi-visual-layout-spec-generator`, `powerbi-report-ux-decision-coach`, `powerbi-ai-report-reviewer` | `powerbi-ai-powerbi-designer-agent`, `powerbi-ai-visual-binding-validator`, `powerbi-ai-report-page-composer`, `powerbi-ai-drillthrough-designer`, `powerbi-ai-mobile-layout-designer` |
| Semantic Modeler | Facts, dimensions, relationships, RLS/OLS, calculation patterns | `powerbi-modelling`, `powerbi-auto-semantic-model-builder`, `powerbi-automated-semantic-model-drafting`, `powerbi-semantic-model-regression` | `powerbi-ai-semantic-modeler-agent`, `powerbi-ai-model-graph-validator`, `powerbi-ai-ambiguous-path-preventer`, `powerbi-ai-star-schema-coach`, `powerbi-ai-relationship-cardinality-advisor` |
| DAX Expert | KPI-to-measure generation, test cases, explanation, optimization | `powerbi-dax`, `powerbi-process-dax-pattern-library`, `powerbi-dax-unit-test-runner`, `powerbi-ai-dax-explainability-agent`, `powerbi-ai-measure-deduplication-agent` | `powerbi-ai-dax-expert-agent`, `powerbi-ai-dax-risk-scorer`, `powerbi-ai-measure-regression-tester`, `powerbi-ai-kpi-to-dax-generator` |
| Power Query/M Developer | Native source routing, M generation, folding, refresh contract | `powerbi-query-design`, `powerbi-powerquery-code-generator`, `powerbi-powerquery-test-harness`, `powerbi-native-source-connector-factory`, `powerbi-connector-capability-matrix` | `powerbi-ai-powerquery-expert-agent`, `powerbi-ai-native-source-router`, `powerbi-ai-powerquery-load-contract`, `powerbi-ai-query-folding-verifier`, `powerbi-ai-refresh-contract-builder` |
| Fabric Architect | Storage mode, Fabric architecture, capacity, deployment blueprint | `powerbi-fabric-architecture-advisor`, `powerbi-fabric-deployment-blueprint`, `powerbi-cost-capacity-optimizer`, `powerbi-ai-capacity-optimization-agent` | `powerbi-ai-fabric-architect-agent`, `powerbi-ai-storage-mode-advisor`, `powerbi-ai-directlake-readiness-advisor`, `powerbi-ai-capacity-cost-architect` |
| BI Tester and Reviewer | Quality gates, regression, Desktop smoke tests, PBIP validation | `powerbi-quality-gate`, `powerbi-expert-review`, `powerbi-automated-report-review-rubric`, `powerbi-acceptance-test-pack-generator`, `powerbi-semantic-model-certification-bot` | `powerbi-ai-bi-qa-agent`, `powerbi-ai-powerbi-desktop-smoke-tester`, `powerbi-ai-frown-to-fix-triage`, `powerbi-ai-pbip-compatibility-validator`, `powerbi-ai-pbir-visual-validator` |
| CoE and Governance Reviewer | Certification, tenant guardrails, evidence, release readiness | `powerbi-coe-copilot`, `powerbi-coe-operating-handbook`, `powerbi-tenant-governance-scanner`, `powerbi-audit-ready-ai-evidence-trail`, `powerbi-ai-model-governance` | `powerbi-ai-coe-reviewer-agent`, `powerbi-ai-certification-decision-agent`, `powerbi-ai-release-evidence-builder`, `powerbi-ai-process-owner-signoff-pack` |
| BI Documentation Owner | Bilingual handover, model docs, KPI docs, release evidence | `powerbi-documentation-generator`, `powerbi-bilingual-documentation`, `powerbi-ai-auto-documentation`, `powerbi-automated-documentation-refresh` | `powerbi-ai-bi-documentation-owner-agent`, `powerbi-ai-model-documentation-auditor`, `powerbi-ai-release-notes-evidence-agent` |

## Product USPs

- Fully replaces repeatable Power BI expert-team work through governed AI/KI skills.
- Process Owner to Power BI without manual expert handoff.
- Data Analyst Agent for business-question decomposition and insight generation.
- Power BI Designer Agent for report layout, visual choice, drilldowns, mobile layout, and storytelling.
- Semantic Modeler Agent for facts, dimensions, relationships, RLS/OLS, and calculation patterns.
- DAX Expert Agent for KPI-to-measure generation, test cases, explanation, deduplication, and optimization.
- Power Query Expert Agent for native connector routing, M generation, query folding, refresh design, and load contracts.
- Fabric Architect Agent for Import, DirectQuery, Direct Lake, Lakehouse, Warehouse, Dataflow, capacity, and deployment choices.
- BI QA Agent for model graph, visual bindings, DAX tests, M tests, PBIP/TMDL/PBIR checks, and Desktop smoke validation.
- Frown-to-Fix Agent for Power BI Desktop error diagnosis and repair planning.
- CoE Reviewer Agent for certification, governance, tenant risk, evidence, and release readiness.
- BI Documentation Owner Agent for bilingual documentation, release notes, handover, lineage, and owner acceptance.

## AI/KI Factory Architecture

1. **Intake and Scope Factory** converts vague process language into scope, users, process chains, source assumptions, KPIs, delivery artifacts, risks, and backlog.
2. **Source and Power Query Factory** resolves source systems, chooses native Power Query connectors, generates M extraction patterns, and defines refresh, privacy, folding, and gateway requirements.
3. **Semantic Model Factory** generates facts, dimensions, relationships, measures, RLS/OLS, display folders, naming standards, and certification metadata.
4. **KPI and DAX Factory** turns KPI contracts into tested DAX measures with date basis, filters, denominator/numerator rules, tolerances, and reconciliation.
5. **Report Design Factory** creates report pages, visual bindings, drilldowns, tooltips, role cockpits, action views, and executive narratives.
6. **Root-Cause and Action Factory** classifies exceptions, creates hypotheses, routes owners, proposes actions, and tracks impact and closed-loop ROI.
7. **Trust and Governance Factory** runs hallucination checks, evidence trails, confidence gates, security review, owner acceptance, certification, and release readiness.
8. **Power BI Desktop Validation Factory** validates PBIP/TMDL/PBIR structure, model graph, native sources, visual bindings, Desktop load, and Frown-free smoke tests.

## Technical Trust Layer

The expert replacement promise is only valid when generated artifacts are technically trustworthy. Therefore every production-grade artifact must pass:

- Native source routing uses real Power Query connector patterns; embedded `DATATABLE` is only an offline demo or smoke-test fixture.
- Semantic model graph has no ambiguous paths, unsupported DirectQuery/OLAP edits, circular filter paths, or accidental fact-to-fact chains.
- DAX measures map to KPI contracts and have reconciliation or unit-test evidence.
- Power Query queries define source keys, type maps, culture, privacy, gateway, refresh, and known connector limits.
- Visual bindings resolve to valid model fields or measures.
- PBIP/PBIR/TMDL structure is compatible with the target Power BI Desktop release.
- Power BI Desktop opens the reference PBIP without a new Frown snapshot.

## Real Engine Layer: 15 Implemented Capabilities

The first executable layer turns the expert-replacement promise into inspectable artifacts. These capabilities are local-first and credential-free unless tenant/API access is explicitly required.

| # | Real capability | Implemented artifact | Expert work replaced |
| --- | --- | --- | --- |
| 1 | Executable validators | `scripts/powerbi_expert_factory.py validate` | BI QA reviewer for PBIP/TMDL/PBIR static checks |
| 2 | Power BI Desktop automation harness | `scripts/powerbi_desktop_smoke_test.ps1` | Desktop smoke tester and Frown monitor |
| 3 | TMDL/PBIR parser library | `parse_model()` and visual binding traversal in `scripts/powerbi_expert_factory.py` | Semantic modeler and report binding reviewer |
| 4 | DAX test execution entry point | `validate_dax_static()` plus KPI contract schema | DAX reviewer baseline before full XMLA/DAX execution |
| 5 | Power Query/M test execution entry point | `validate_native_sources()` | Power Query reviewer for connector and brittle navigation risks |
| 6 | KPI contract schema | `schemas/kpi_contract.schema.json` | KPI definition owner and DAX handoff reviewer |
| 7 | Evidence store event schema | `schemas/evidence_event.schema.json` and `powerbi_expert_factory.py evidence` | CoE evidence and release audit preparation |
| 8 | Skill orchestrator handoff | `schemas/orchestration_handoff.schema.json` | BI delivery manager handoff discipline |
| 9 | Real connector matrix | `data/powerbi_connector_matrix.json` | Power Query connector routing advisor |
| 10 | Report screenshot / visual QA checklist | `templates/report_visual_qa_checklist.json` | Report designer QA checklist |
| 11 | PBIX/PBIP import/refactor pipeline | `templates/refactor_pipeline.json` | Migration and refactor consultant |
| 12 | Process pack templates as data | `templates/process_packs/*.json` | Reusable process BI solution architect |
| 13 | Admin API / tenant scanner plan | `templates/admin_api_tenant_scan_plan.json` | CoE tenant governance analyst |
| 14 | Security/RLS test harness schema | `schemas/rls_test_case.schema.json` | Security and RLS test reviewer |
| 15 | Golden acceptance schema | `schemas/golden_acceptance.schema.json` | Release manager and certification gatekeeper |

Minimum command-line acceptance for a PBIP folder:

```powershell
python scripts\powerbi_expert_factory.py validate --project outputs\powerbi-order2cash-pbip\Order2Cash_NativeExcel --out outputs\powerbi-order2cash-pbip\expert_factory_validation.json
```

Desktop smoke validation, when Power BI Desktop is available locally:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\powerbi_desktop_smoke_test.ps1 -PbipPath outputs\powerbi-order2cash-pbip\Order2Cash_NativeExcel\Order2Cash.pbip -OutJson outputs\powerbi-order2cash-pbip\desktop_smoke.json
```

## O2C Reference Proof

Order2Cash is the first proof process for expert replacement credibility. It must demonstrate:

- Source routing across native Excel/CSV patterns and future enterprise connectors.
- Clean star-schema semantic model without ambiguous relationship paths.
- KPI contracts for backlog, order value, ATP, OTIF, billing block, AR, churn risk, quote leakage, and exceptions.
- DAX measures with test and reconciliation strategy.
- Report pages for overview, customer churn, order backlog, delivery/OTIF, billing/cash, and quote/margin leakage.
- Root-cause paths by customer, product, plant, warehouse, carrier, status, and owner role.
- Desktop validation with no new Power BI Frown and no broken visuals.

## Roadmap

### Phase 1: Narrative and Documentation

- Create this Gesamtplan and the expert replacement skill map.
- Reframe README, plugin README, Expert Reduction USPs, Process Owner AI/KI USPs, and Skills Catalog around Power BI Expert-Replacement Factory.
- Keep Process Owner empowerment as user-facing benefit and expert replacement as delivery mechanism.

### Phase 2: Expert-Agent Skill Roadmap

- Add planned skill sections for each replaced expert role.
- Keep existing skills as current coverage.
- Mark new AI/KI expert-agent skills as planned capabilities until implemented.
- Define minimum input/output expectations for every planned skill.

### Phase 3: Technical Trust Layer

- Prioritize `powerbi-ai-model-graph-validator`.
- Prioritize `powerbi-ai-native-source-router`.
- Prioritize `powerbi-ai-visual-binding-validator`.
- Prioritize `powerbi-ai-powerbi-desktop-smoke-tester`.
- Prioritize `powerbi-ai-frown-to-fix-triage`.

### Phase 4: O2C Reference Delivery

- Use Order2Cash as the reference delivery pack.
- Validate source routing, model graph, DAX, Power Query, report pages, visual bindings, and Desktop load.
- Treat each discovered Power BI Desktop error as a required improvement to the trust layer.

### Phase 5: Process Pack Expansion

- Expand to Procure2Pay, Record2Report, Plan2Produce, Dock2Stock, Complaint2CAPA, Maintain2Operate, and Control2Evidence.
- Each process pack must include skill mapping, KPI library, source candidates, model template, DAX catalog, report layout, quality gates, and owner acceptance.

## Governance Boundary

The tool replaces repeatable expert work, not business accountability. Human Process Owners still approve KPI meaning, source ownership, and action accountability. CoE/IT still own tenant policy, credentials, external sharing, security boundaries, and production release authority. The product makes expert work repeatable, governed, and testable instead of informal and person-dependent.
