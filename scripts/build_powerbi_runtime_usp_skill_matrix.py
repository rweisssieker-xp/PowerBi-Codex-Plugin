"""Build the Runtime Max USP to plugin skill routing matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "powerbi_runtime_max_catalog.json"
OUT_PATH = ROOT / "data" / "powerbi_runtime_usp_skill_matrix.json"


ROUTES = {
    "question_to_model_autopilot": ("powerbi-requirement-to-model-autopilot", ["report-package"], ["report package manifest"]),
    "source_discovery_autopilot": ("powerbi-source-metadata-discovery", ["report-package"], ["source_profile.json"]),
    "ai_field_mapping_runtime": ("powerbi-ai-source-mapping-agent", ["report-package"], ["model_build_plan.json"]),
    "kpi_ontology_runtime": ("powerbi-enterprise-kpi-ontology", ["runtime-max-plan"], ["kpi ontology records"]),
    "root_cause_path_builder": ("powerbi-ai-root-cause-playbook-generator", ["report-package"], ["report_pages_plan.json"]),
    "narrative_insight_writer": ("powerbi-executive-narrative-generator", ["report-package"], ["report_pages_plan.json"]),
    "tmdl_compiler": ("powerbi-pbip-tmdl-generator", ["report-package"], ["PBIP/TMDL project"]),
    "full_pbip_generator": ("powerbi-pbip-tmdl-generator", ["report-package"], ["PBIP project"]),
    "pbir_visual_materializer": ("powerbi-visual-layout-spec-generator", ["report-package"], ["PBIR report pages"]),
    "dax_measure_factory": ("powerbi-dax", ["report-package"], ["dax_measure_plan.json"]),
    "dax_expected_result_runner": ("powerbi-dax-test-harness", ["dax-query-request"], ["DAX expected-result request"]),
    "power_query_m_factory": ("powerbi-powerquery-code-generator", ["report-package"], ["power_query_m_plan.json"]),
    "real_connector_runner_contracts": ("powerbi-live-connector-toolkit", ["report-package"], ["source_profile.json"]),
    "credential_safe_runtime": ("powerbi-compliance-evidence-pack", ["runtime-max-plan"], ["credential-safe evidence"]),
    "semantic_auto_repair": ("powerbi-ai-autonomous-remediation-agent", ["validate"], ["model_improvement_plan.json"]),
    "desktop_frown_log_parser": ("powerbi-ai-frown-to-fix-triage", ["hardening-plan"], ["Frown triage evidence"]),
    "model_graph_quality_gate": ("powerbi-ai-model-graph-validator", ["validate"], ["validation_result.json"]),
    "visual_binding_quality_gate": ("powerbi-ai-visual-binding-validator", ["validate"], ["validation_result.json"]),
    "report_layout_scoring_runtime": ("powerbi-report-ux-decision-coach", ["report-package"], ["report_pages_plan.json"]),
    "rls_role_generator": ("powerbi-rls-ols-pattern-library", ["report-package"], ["model_build_plan.json"]),
    "process_mining_eventlog_runtime": ("powerbi-process-mining", ["report-package"], ["process event log contract"]),
    "action_cockpit_generator": ("powerbi-role-based-cockpit-factory", ["report-package"], ["report_pages_plan.json"]),
    "tenant_readiness_runtime": ("powerbi-tenant-governance-scanner", ["tenant-scan-request"], ["tenant scan request"]),
    "deployment_pipeline_runtime": ("powerbi-devops-cicd", ["rest-deploy-request"], ["REST deployment request"]),
    "fabric_scaffold_runtime": ("powerbi-fabric-deployment-blueprint", ["rest-deploy-request"], ["Fabric deployment blueprint"]),
    "documentation_publisher_runtime": ("powerbi-documentation-generator", ["report-package"], ["report package docs"]),
    "acceptance_evidence_packager": ("powerbi-acceptance-test-pack-generator", ["report-package"], ["validation_plan.json"]),
    "process_owner_acceptance_runtime": ("powerbi-business-owner-acceptance", ["report-package"], ["owner acceptance pack"]),
    "release_decision_copilot": ("powerbi-ai-powerbi-release-evidence-pack", ["rest-deploy-request"], ["release evidence"]),
    "continuous_improvement_backlog": ("powerbi-ai-continuous-improvement-agent", ["report-package"], ["model_improvement_plan.json"]),
    "dashboard_consolidation_autopilot": ("powerbi-report-consolidation-ai", ["runtime-max-plan"], ["consolidation plan"]),
    "legacy_report_reverse_engineer": ("powerbi-migration-factory", ["pbix-intake"], ["PBIX intake manifest"]),
    "business_question_simulator": ("powerbi-ai-business-question-generator", ["report-package"], ["question coverage matrix"]),
    "kpi_dispute_resolver": ("powerbi-kpi-conflict-war-room", ["runtime-max-plan"], ["KPI conflict record"]),
    "semantic_model_refactoring_autopilot": ("powerbi-ai-semantic-model-refactor-agent", ["validate"], ["model_improvement_plan.json"]),
    "executive_board_pack_generator": ("powerbi-ai-executive-boardroom-autopilot", ["report-package"], ["board pack"]),
    "powerbi_performance_engineer": ("powerbi-performance-refresh-optimizer", ["validate"], ["performance plan"]),
    "refresh_failure_triage_agent": ("powerbi-automated-refresh-failure-triage", ["hardening-plan"], ["refresh triage request"]),
    "data_contract_negotiator": ("powerbi-ai-data-contract-negotiator", ["report-package"], ["source_profile.json"]),
    "report_ux_critic": ("powerbi-ai-report-ux-critic", ["report-package"], ["report_pages_plan.json"]),
    "dax_explainability_layer": ("powerbi-ai-dax-explainability-agent", ["dax-query-request"], ["DAX explanation evidence"]),
    "measure_dependency_impact_analyzer": ("powerbi-ai-lineage-blast-radius", ["validate"], ["impact map"]),
    "rls_ols_attack_simulator": ("powerbi-ai-security-exposure-analyzer", ["tenant-scan-request"], ["security findings"]),
    "powerbi_coe_certification_bot": ("powerbi-semantic-model-certification-bot", ["validate"], ["certification evidence"]),
    "fabric_cost_guardrail": ("powerbi-cost-capacity-optimizer", ["tenant-scan-request"], ["cost guardrail evidence"]),
    "natural_language_data_mart_builder": ("powerbi-natural-language-verified-report", ["report-package"], ["data mart plan"]),
    "process_benchmark_pack": ("powerbi-industrial-kpi-benchmark-pack", ["report-package"], ["benchmark evidence"]),
    "audit_ready_evidence_vault": ("powerbi-audit-ready-ai-evidence-trail", ["report-package"], ["audit evidence"]),
    "user_adoption_tracker": ("powerbi-report-usage-telemetry-optimizer", ["tenant-scan-request"], ["adoption evidence"]),
    "autonomous_bi_sprint_manager": ("powerbi-ai-autonomous-bi-sprint", ["report-package"], ["sprint plan"]),
    "pbix_binary_intake": ("powerbi-migration-factory", ["pbix-intake"], ["PBIX intake manifest"]),
    "live_tenant_scanner": ("powerbi-live-metadata-scanner", ["tenant-scan-request"], ["tenant scan request"]),
    "powerbi_rest_deployer": ("powerbi-devops-cicd", ["rest-deploy-request"], ["REST deployment request"]),
    "tabular_editor_tom_bridge": ("powerbi-devops-cicd", ["rest-deploy-request"], ["TOM/TMSL bridge request"]),
    "dax_query_runner": ("powerbi-dax-unit-test-runner", ["dax-query-request"], ["DAX query request"]),
    "query_folding_verifier": ("powerbi-powerquery-test-harness", ["report-package"], ["Power Query validation plan"]),
    "incremental_refresh_designer": ("powerbi-performance-refresh-optimizer", ["report-package"], ["incremental refresh plan"]),
    "composite_model_advisor": ("powerbi-fabric-architecture-advisor", ["report-package"], ["composite model recommendation"]),
    "deployment_rollback_executor": ("powerbi-devops-cicd", ["rest-deploy-request"], ["rollback request"]),
    "gateway_configuration_auditor": ("powerbi-admin-api-playbook", ["gateway-audit-request"], ["gateway audit request"]),
    "sensitivity_purview_classifier": ("powerbi-compliance-evidence-pack", ["tenant-scan-request"], ["classification evidence"]),
    "data_quality_profiler_runtime": ("powerbi-data-quality-rule-library", ["report-package"], ["data quality profile"]),
    "anomaly_detection_pack": ("powerbi-anomaly-to-explanation", ["report-package"], ["anomaly findings"]),
    "forecast_what_if_builder": ("powerbi-planning-simulation", ["report-package"], ["forecast scenario plan"]),
    "metric_store_connector": ("powerbi-enterprise-kpi-ontology", ["runtime-max-plan"], ["metric store mapping"]),
    "enterprise_glossary_sync": ("powerbi-business-glossary-generator", ["runtime-max-plan"], ["glossary sync record"]),
    "ticketing_integration": ("powerbi-closed-loop-bi", ["report-package"], ["ticket payloads"]),
    "access_review_automation": ("powerbi-automated-security-exposure-scan", ["tenant-scan-request"], ["access review report"]),
    "usage_based_refactoring_agent": ("powerbi-report-usage-telemetry-optimizer", ["tenant-scan-request"], ["refactor priority list"]),
    "multi_tenant_msp_mode": ("powerbi-multi-tenant-msp-mode", ["tenant-scan-request", "gateway-audit-request"], ["tenant isolation manifest"]),
}


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    entries = []
    for capability in catalog["capabilities"]:
        skill, commands, artifacts = ROUTES[capability["id"]]
        entries.append(
            {
                "capabilityId": capability["id"],
                "capabilityName": capability["name"],
                "replacementRole": capability["replacementRole"],
                "primarySkill": skill,
                "cliEntrypoints": commands,
                "outputArtifacts": artifacts,
            }
        )
    payload = {
        "version": "2026-05-04",
        "description": "Runtime Max USP to plugin skill and CLI routing matrix.",
        "capabilityCount": len(entries),
        "entries": entries,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"generated {OUT_PATH.relative_to(ROOT)} with {len(entries)} mappings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
