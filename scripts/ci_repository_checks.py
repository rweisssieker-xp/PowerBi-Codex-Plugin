"""Repository checks used by local validation and GitHub Actions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - handled as a clear CI failure
    yaml = None


ROOT_ENGLISH_MARKERS = (
    "de-DE",
    "deutsch",
    "Dokumentation",
    "Kurzfassung",
    "fuer",
    "koennen",
    "muessen",
    "Zusammenfassung",
    "Sicherheit",
    "Sicherheitsproblem",
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def check_json(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - CI should report the exact file
            errors.append(f"{path}: invalid JSON: {exc}")
    return errors


def check_github_yaml(root: Path) -> list[str]:
    errors: list[str] = []
    if yaml is None:
        return ["PyYAML is required for GitHub YAML validation"]
    for path in sorted((root / ".github").rglob("*.yml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - CI should report the exact file
            errors.append(f"{path}: invalid YAML: {exc}")
    return errors


def check_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            raw = target.strip("<>").split("#", 1)[0]
            if raw and not (path.parent / raw).resolve().exists():
                errors.append(f"{path}: missing local link target {target}")
    return errors


def check_root_english(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        hits = [marker for marker in ROOT_ENGLISH_MARKERS if marker.lower() in text.lower()]
        if hits:
            errors.append(f"{path}: root GitHub doc contains non-English markers: {', '.join(hits)}")
    return errors


def check_required_files(root: Path) -> list[str]:
    required = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "SUPPORT.md",
        "CHANGELOG.md",
        "DOCUMENTATION.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/process_pack.yml",
        ".github/dependabot.yml",
        ".github/workflows/ci.yml",
    ]
    return [f"{item}: required file is missing" for item in required if not (root / item).exists()]


def check_industry_demo_data(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return ["data/industry_process_catalog.json: required process catalog is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    processes = catalog.get("processes", [])
    if len(processes) < 32:
        errors.append(f"{catalog_path}: expected at least 32 industrial processes, found {len(processes)}")

    for process in processes:
        process_id = process.get("processId")
        if not process_id:
            errors.append(f"{catalog_path}: process without processId")
            continue
        folder = root / "outputs" / "industry-demo-data" / str(process_id)
        for filename, min_rows in {
            "cases.csv": 10,
            "events.csv": 30,
            "kpi_snapshots.csv": 12,
        }.items():
            path = folder / filename
            if not path.exists():
                errors.append(f"{path}: required demo data file is missing")
                continue
            row_count = max(0, len(path.read_text(encoding="utf-8").splitlines()) - 1)
            if row_count < min_rows:
                errors.append(f"{path}: expected at least {min_rows} data rows, found {row_count}")

    index_path = root / "outputs" / "industry-demo-data" / "index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: industry demo data index is missing")
    return errors


def check_powerbi_source_routing(root: Path) -> list[str]:
    errors: list[str] = []
    matrix_path = root / "data/powerbi_source_capability_matrix.json"
    routing_path = root / "outputs/source-routing/process_source_routing.json"
    if not matrix_path.exists():
        return [f"{matrix_path}: Power BI source capability matrix is missing"]
    if not routing_path.exists():
        return [f"{routing_path}: process source-routing map is missing"]

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    expected_categories = {
        "File",
        "Database",
        "Microsoft Fabric",
        "Power Platform",
        "Azure",
        "Online Services",
        "Other",
    }
    categories = {category.get("category") for category in matrix.get("sourceCategories", [])}
    missing_categories = expected_categories - categories
    if missing_categories:
        errors.append(f"{matrix_path}: missing source categories: {', '.join(sorted(missing_categories))}")

    connector_count = sum(len(category.get("connectors", [])) for category in matrix.get("sourceCategories", []))
    if connector_count < 80:
        errors.append(f"{matrix_path}: expected broad Power BI connector coverage, found {connector_count} connectors")

    routing = json.loads(routing_path.read_text(encoding="utf-8")).get("routes", [])
    catalog = json.loads((root / "data/industry_process_catalog.json").read_text(encoding="utf-8"))
    if len(routing) != len(catalog.get("processes", [])):
        errors.append(f"{routing_path}: expected one source route per process")
    for route in routing:
        connectors = route.get("productionSourceRouting", [])
        if len(connectors) < 3:
            errors.append(f"{routing_path}: {route.get('processId')} has fewer than 3 production connectors")
        categories_for_route = {connector.get("category") for connector in connectors}
        if not categories_for_route:
            errors.append(f"{routing_path}: {route.get('processId')} has no production source categories")
        for decision in ["native connector", "gateway and credential owner", "schema drift handling"]:
            if decision not in route.get("requiredSourceDecisions", []):
                errors.append(f"{routing_path}: {route.get('processId')} missing source decision '{decision}'")
    return errors


def check_industry_process_packs(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return ["data/industry_process_catalog.json: required process catalog is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    for process in catalog.get("processes", []):
        process_id = process.get("processId")
        if not process_id:
            continue
        folder = root / "outputs" / "industry-process-packs" / str(process_id)
        required_files = [
            "model_spec.json",
            "dax_measures.dax",
            "report_pages.json",
            "quality_gate.json",
            "README.md",
        ]
        for filename in required_files:
            path = folder / filename
            if not path.exists():
                errors.append(f"{path}: required process-pack file is missing")

        model_path = folder / "model_spec.json"
        if model_path.exists():
            model = json.loads(model_path.read_text(encoding="utf-8"))
            if len(model.get("tables", [])) < 5:
                errors.append(f"{model_path}: expected at least 5 semantic model tables")
            if not model.get("relationships"):
                errors.append(f"{model_path}: expected relationships")
            source_pattern = model.get("nativeSourcePattern", {})
            if source_pattern.get("connector") != "Folder.Files + Csv.Document":
                errors.append(f"{model_path}: demo source connector pattern is not declared")
            production_routes = model.get("productionSourceRouting", [])
            if len(production_routes) < 3:
                errors.append(f"{model_path}: expected at least 3 production native-source routes")
            if not model.get("requiredSourceDecisions"):
                errors.append(f"{model_path}: expected required source decisions")

        dax_path = folder / "dax_measures.dax"
        if dax_path.exists():
            text = dax_path.read_text(encoding="utf-8")
            expected_min = len(process.get("kpis", [])) + 4
            measure_count = len([line for line in text.splitlines() if " = " in line and not line.strip().startswith("--")])
            if measure_count < expected_min:
                errors.append(f"{dax_path}: expected at least {expected_min} measures, found {measure_count}")

        pages_path = folder / "report_pages.json"
        if pages_path.exists():
            pages = json.loads(pages_path.read_text(encoding="utf-8")).get("pages", [])
            if len(pages) < 4:
                errors.append(f"{pages_path}: expected at least 4 report page specs")

        gate_path = folder / "quality_gate.json"
        if gate_path.exists():
            checks = json.loads(gate_path.read_text(encoding="utf-8")).get("requiredChecks", [])
            for required_check in ["model_spec_valid", "dax_measures_present", "report_pages_present"]:
                if required_check not in checks:
                    errors.append(f"{gate_path}: missing required check {required_check}")

    index_path = root / "outputs" / "industry-process-packs" / "index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: industry process-pack index is missing")
    return errors


def check_usp_capability_coverage(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_usp_capability_catalog.json"
    coverage_root = root / "outputs/usp-capability-coverage"
    process_catalog_path = root / "data/industry_process_catalog.json"

    if not catalog_path.exists():
        return [f"{catalog_path}: USP capability catalog is missing"]
    if not coverage_root.exists():
        return [f"{coverage_root}: USP coverage output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    capability_ids = {capability.get("id") for capability in capabilities}
    if len(capabilities) != 20:
        errors.append(f"{catalog_path}: expected exactly 20 USP capabilities, found {len(capabilities)}")
    for capability in capabilities:
        for field in ["id", "name", "summary", "requiredArtifacts", "evidence"]:
            if not capability.get(field):
                errors.append(f"{catalog_path}: capability {capability.get('id')} missing {field}")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        path = coverage_root / str(process_id) / "usp_coverage.json"
        if not path.exists():
            errors.append(f"{path}: USP coverage file is missing")
            continue
        coverage = json.loads(path.read_text(encoding="utf-8"))
        covered_ids = {capability.get("id") for capability in coverage.get("capabilities", [])}
        if covered_ids != capability_ids:
            missing = capability_ids - covered_ids
            extra = covered_ids - capability_ids
            errors.append(f"{path}: USP coverage mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
        if coverage.get("capabilityCount") != 20:
            errors.append(f"{path}: expected capabilityCount 20")

    index_path = coverage_root / "index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: USP coverage index is missing")
    return errors


def check_powerbi_feature_factory(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_feature_catalog.json"
    output_root = root / "outputs/powerbi-feature-factory"
    process_catalog_path = root / "data/industry_process_catalog.json"

    if not catalog_path.exists():
        return [f"{catalog_path}: executable Power BI feature catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: Power BI feature factory output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    features = catalog.get("features", [])
    if catalog.get("featureCount") != 20 or len(features) != 20:
        errors.append(f"{catalog_path}: expected exactly 20 executable features")

    required_feature_fields = [
        "id",
        "name",
        "implementationStatus",
        "implementationType",
        "inputs",
        "outputs",
        "cliCommands",
        "acceptanceChecks",
        "contractPath",
        "validationContractPath",
        "cliRecipePath",
    ]
    for feature in features:
        for field in required_feature_fields:
            if not feature.get(field):
                errors.append(f"{catalog_path}: feature {feature.get('id')} missing {field}")
        if feature.get("implementationStatus") != "implemented_as_executable_contract":
            errors.append(f"{catalog_path}: feature {feature.get('id')} has non-executable status")
        for key in ["contractPath", "validationContractPath", "cliRecipePath"]:
            target = root / feature.get(key, "")
            if not target.exists():
                errors.append(f"{target}: required feature artifact is missing")

        contract_path = root / feature.get("contractPath", "")
        validation_path = root / feature.get("validationContractPath", "")
        if contract_path.exists():
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            if contract.get("id") != feature.get("id"):
                errors.append(f"{contract_path}: contract id does not match catalog")
            for field in ["inputs", "outputs", "cliCommands"]:
                if not contract.get(field):
                    errors.append(f"{contract_path}: missing {field}")
        if validation_path.exists():
            validation = json.loads(validation_path.read_text(encoding="utf-8"))
            if not validation.get("acceptanceChecks"):
                errors.append(f"{validation_path}: missing acceptanceChecks")

    index_path = output_root / "feature_index.csv"
    matrix_path = output_root / "process_feature_matrix.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: feature index is missing")
    if not matrix_path.exists():
        errors.append(f"{matrix_path}: process feature matrix is missing")
    else:
        process_count = len(json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", []))
        row_count = max(0, len(matrix_path.read_text(encoding="utf-8").splitlines()) - 1)
        expected_rows = process_count * 20
        if row_count != expected_rows:
            errors.append(f"{matrix_path}: expected {expected_rows} rows, found {row_count}")

    return errors


def check_powerbi_execution_layer(root: Path) -> list[str]:
    errors: list[str] = []
    output_root = root / "outputs/powerbi-execution-layer"
    frown_path = root / "data/powerbi_frown_knowledge_base.json"
    process_catalog_path = root / "data/industry_process_catalog.json"
    feature_catalog_path = root / "data/powerbi_feature_catalog.json"

    if not output_root.exists():
        return [f"{output_root}: Power BI execution layer output folder is missing"]
    if not frown_path.exists():
        errors.append(f"{frown_path}: Frown-to-Fix knowledge base is missing")
    else:
        patterns = json.loads(frown_path.read_text(encoding="utf-8")).get("patterns", [])
        if len(patterns) < 5:
            errors.append(f"{frown_path}: expected at least 5 known Power BI Frown patterns")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    feature_count = json.loads(feature_catalog_path.read_text(encoding="utf-8")).get("featureCount")
    required_process_artifacts = [
        "source_profile.json",
        "m_query_templates.json",
        "schema_drift_contract.json",
        "semantic_compile_plan.json",
        "report_materialization_plan.json",
        "dax_expected_results_plan.json",
        "lineage_graph.json",
        "lineage_graph.mmd",
        "process_owner_acceptance_pack.json",
        "security_policy_plan.json",
        "performance_budget.json",
        "process_pack_version.json",
        "feature_execution_status.json",
        "build_manifest.json",
        "README.md",
    ]
    for process in processes:
        process_id = process.get("processId")
        folder = output_root / "processes" / str(process_id)
        for filename in required_process_artifacts:
            path = folder / filename
            if not path.exists():
                errors.append(f"{path}: required execution-layer artifact is missing")
        source_profile = folder / "source_profile.json"
        if source_profile.exists():
            tables = json.loads(source_profile.read_text(encoding="utf-8")).get("tables", {})
            for required_file in ["cases.csv", "events.csv", "kpi_snapshots.csv"]:
                if required_file not in tables:
                    errors.append(f"{source_profile}: missing profile for {required_file}")
        feature_status = folder / "feature_execution_status.json"
        if feature_status.exists():
            status = json.loads(feature_status.read_text(encoding="utf-8"))
            if status.get("featureCount") != feature_count:
                errors.append(f"{feature_status}: expected featureCount {feature_count}")
            if not all(item.get("status") == "generated" for item in status.get("features", [])):
                errors.append(f"{feature_status}: all features must have generated status")

    index_path = output_root / "execution_index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: execution index is missing")
    else:
        row_count = max(0, len(index_path.read_text(encoding="utf-8").splitlines()) - 1)
        if row_count != len(processes):
            errors.append(f"{index_path}: expected {len(processes)} process rows, found {row_count}")

    for global_file in ["golden_reference_suite.json", "demo_to_production_migration_wizard.json", "README.md"]:
        if not (output_root / global_file).exists():
            errors.append(f"{output_root / global_file}: required global execution artifact is missing")
    return errors


def check_powerbi_premium_usp_layer(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_premium_usp_catalog.json"
    output_root = root / "outputs/powerbi-premium-usp-layer"
    process_catalog_path = root / "data/industry_process_catalog.json"

    if not catalog_path.exists():
        return [f"{catalog_path}: premium USP catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: premium USP output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    if catalog.get("capabilityCount") != 25 or len(capabilities) != 25:
        errors.append(f"{catalog_path}: expected exactly 25 premium USP capabilities")

    required_fields = [
        "id",
        "name",
        "summary",
        "capabilityType",
        "implementationStatus",
        "inputs",
        "outputs",
        "acceptanceChecks",
        "contractPath",
        "recipePath",
        "evidencePath",
    ]
    for capability in capabilities:
        for field in required_fields:
            if not capability.get(field):
                errors.append(f"{catalog_path}: premium USP {capability.get('id')} missing {field}")
        if capability.get("implementationStatus") != "implemented_as_premium_usp_contract":
            errors.append(f"{catalog_path}: premium USP {capability.get('id')} has invalid status")
        for key in ["contractPath", "recipePath", "evidencePath"]:
            path = root / capability.get(key, "")
            if not path.exists():
                errors.append(f"{path}: premium USP artifact is missing")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        plan_path = output_root / "processes" / str(process_id) / "premium_usp_plan.json"
        if not plan_path.exists():
            errors.append(f"{plan_path}: process premium USP plan is missing")
            continue
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if plan.get("premiumUspCount") != 25 or len(plan.get("premiumUsps", [])) != 25:
            errors.append(f"{plan_path}: expected 25 premium USPs")

    matrix_path = output_root / "process_premium_usp_matrix.csv"
    if not matrix_path.exists():
        errors.append(f"{matrix_path}: process premium USP matrix is missing")
    else:
        row_count = max(0, len(matrix_path.read_text(encoding="utf-8").splitlines()) - 1)
        expected = len(processes) * 25
        if row_count != expected:
            errors.append(f"{matrix_path}: expected {expected} rows, found {row_count}")
    if not (output_root / "premium_usp_index.csv").exists():
        errors.append(f"{output_root / 'premium_usp_index.csv'}: premium USP index is missing")
    if not (output_root / "README.md").exists():
        errors.append(f"{output_root / 'README.md'}: premium USP README is missing")
    return errors


def check_powerbi_runtime_max_layer(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_runtime_max_catalog.json"
    output_root = root / "outputs/powerbi-runtime-max-layer"
    process_catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return [f"{catalog_path}: runtime max catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: runtime max output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    if catalog.get("capabilityCount") != 70 or len(capabilities) != 70:
        errors.append(f"{catalog_path}: expected exactly 70 runtime max USP capabilities")
    for capability in capabilities:
        for field in [
            "id",
            "name",
            "summary",
            "implementationStatus",
            "replacementRole",
            "replacementOutcome",
            "autonomyLevel",
            "deliverables",
            "acceptanceChecks",
        ]:
            if not capability.get(field):
                errors.append(f"{catalog_path}: runtime max capability missing {field}")
        if capability.get("implementationStatus") != "implemented_as_runtime_max_usp_artifact":
            errors.append(f"{catalog_path}: runtime max capability {capability.get('id')} has invalid status")

    required_files = [
        "runtime_manifest.json",
        "tmdl_compile_result.json",
        "pbir_materialization_result.json",
        "desktop_log_parser_contract.json",
        "semantic_auto_repair_rules.json",
        "dax_expected_result_runner.json",
        "real_connector_runner_contracts.json",
        "field_mapping_candidates.json",
        "kpi_ontology_records.json",
        "tenant_readiness_checklist.json",
        "deployment_pipeline_plan.json",
        "fabric_scaffold_plan.json",
        "documentation_publish_manifest.json",
        "README.md",
    ]
    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        folder = output_root / "processes" / str(process_id)
        for filename in required_files:
            if not (folder / filename).exists():
                errors.append(f"{folder / filename}: required runtime max artifact is missing")
        manifest_path = folder / "runtime_manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("capabilityCount") != 70:
                errors.append(f"{manifest_path}: expected capabilityCount 70")
            runtime_usps = manifest.get("runtimeMaxUsps", [])
            if len(runtime_usps) != 70:
                errors.append(f"{manifest_path}: expected 70 runtimeMaxUsps")
            for usp in runtime_usps:
                artifact_path = root / usp.get("artifactPath", "")
                if not artifact_path.exists():
                    errors.append(f"{manifest_path}: runtime max USP artifact is missing: {artifact_path}")
            pbip = Path(manifest.get("pbip", {}).get("projectPath", ""))
            if not pbip.exists():
                errors.append(f"{manifest_path}: generated PBIP path does not exist")
            if not list(pbip.glob("*.SemanticModel/definition/tables/*.tmdl")):
                errors.append(f"{manifest_path}: generated PBIP has no TMDL tables")
            if not list(pbip.glob("*.Report/definition/pages/*/visuals/*/visual.json")):
                errors.append(f"{manifest_path}: generated PBIP has no PBIR visual files")

    index_path = output_root / "runtime_index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: runtime max index is missing")
    else:
        row_count = max(0, len(index_path.read_text(encoding="utf-8").splitlines()) - 1)
        if row_count != len(processes):
            errors.append(f"{index_path}: expected {len(processes)} rows, found {row_count}")
    if not (output_root / "README.md").exists():
        errors.append(f"{output_root / 'README.md'}: runtime max README is missing")
    return errors


def check_powerbi_production_hardening(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_production_hardening_catalog.json"
    output_root = root / "outputs/powerbi-production-hardening"
    process_catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return [f"{catalog_path}: production hardening catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: production hardening output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    if catalog.get("capabilityCount") != 15 or len(capabilities) != 15:
        errors.append(f"{catalog_path}: expected exactly 15 production hardening capabilities")
    capability_ids = [str(capability.get("id")) for capability in capabilities]
    for capability in capabilities:
        for field in ["id", "name", "summary", "implementationStatus", "requiredArtifact", "acceptanceChecks"]:
            if not capability.get(field):
                errors.append(f"{catalog_path}: production hardening capability missing {field}")
        if capability.get("implementationStatus") != "implemented_as_production_hardening_artifact":
            errors.append(f"{catalog_path}: production hardening capability {capability.get('id')} has invalid status")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        folder = output_root / "processes" / str(process_id)
        for capability_id in capability_ids:
            path = folder / f"{capability_id}.json"
            if not path.exists():
                errors.append(f"{path}: required hardening artifact is missing")
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("capabilityId") != capability_id:
                errors.append(f"{path}: capabilityId mismatch")
            if payload.get("status") not in {"pass", "contract-ready", "warn", "simulated"}:
                errors.append(f"{path}: invalid status {payload.get('status')}")
        dashboard_path = folder / "production_release_dashboard.json"
        if not dashboard_path.exists():
            errors.append(f"{dashboard_path}: release dashboard is missing")
        else:
            dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))
            if dashboard.get("capabilityCount") != 15:
                errors.append(f"{dashboard_path}: expected capabilityCount 15")

    index_path = output_root / "production_hardening_index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: production hardening index is missing")
    else:
        row_count = max(0, len(index_path.read_text(encoding="utf-8").splitlines()) - 1)
        if row_count != len(processes):
            errors.append(f"{index_path}: expected {len(processes)} rows, found {row_count}")
    for global_file in ["release_quality_dashboard.json", "README.md"]:
        if not (output_root / global_file).exists():
            errors.append(f"{output_root / global_file}: required production hardening global artifact is missing")
    return errors


def check_powerbi_market_differentiator_usps(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_market_differentiator_usp_catalog.json"
    output_root = root / "outputs/powerbi-market-differentiator-usps"
    process_catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return [f"{catalog_path}: market differentiator USP catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: market differentiator USP output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    if catalog.get("capabilityCount") != 30 or len(capabilities) != 30:
        errors.append(f"{catalog_path}: expected exactly 30 market differentiator USPs")
    capability_ids = [str(capability.get("id")) for capability in capabilities]
    for capability in capabilities:
        for field in [
            "id",
            "name",
            "summary",
            "primaryPersona",
            "marketDifferentiator",
            "implementationStatus",
            "proofArtifacts",
            "acceptanceChecks",
        ]:
            if not capability.get(field):
                errors.append(f"{catalog_path}: market differentiator USP missing {field}")
        if capability.get("implementationStatus") != "implemented_as_market_differentiator_evidence":
            errors.append(f"{catalog_path}: market differentiator USP {capability.get('id')} has invalid status")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        folder = output_root / "processes" / str(process_id)
        plan_path = folder / "market_differentiator_plan.json"
        if not plan_path.exists():
            errors.append(f"{plan_path}: market differentiator process plan is missing")
            continue
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if plan.get("capabilityCount") != 30 or len(plan.get("marketDifferentiatorUsps", [])) != 30:
            errors.append(f"{plan_path}: expected 30 market differentiator USPs")
        for capability_id in capability_ids:
            artifact_path = folder / f"{capability_id}.json"
            if not artifact_path.exists():
                errors.append(f"{artifact_path}: market differentiator evidence artifact is missing")
                continue
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            if artifact.get("capabilityId") != capability_id:
                errors.append(f"{artifact_path}: capabilityId mismatch")
            if artifact.get("status") != "evidence-ready":
                errors.append(f"{artifact_path}: expected status evidence-ready")

    index_path = output_root / "market_differentiator_index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: market differentiator index is missing")
    else:
        row_count = max(0, len(index_path.read_text(encoding="utf-8").splitlines()) - 1)
        if row_count != len(processes):
            errors.append(f"{index_path}: expected {len(processes)} rows, found {row_count}")
    summary_path = output_root / "market_differentiator_summary.json"
    if not summary_path.exists():
        errors.append(f"{summary_path}: market differentiator summary is missing")
    if not (output_root / "README.md").exists():
        errors.append(f"{output_root / 'README.md'}: market differentiator README is missing")
    return errors


def check_powerbi_decision_intelligence_usps(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "data/powerbi_decision_intelligence_usp_catalog.json"
    output_root = root / "outputs/powerbi-decision-intelligence-usps"
    process_catalog_path = root / "data/industry_process_catalog.json"
    if not catalog_path.exists():
        return [f"{catalog_path}: decision intelligence USP catalog is missing"]
    if not output_root.exists():
        return [f"{output_root}: decision intelligence USP output folder is missing"]

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities", [])
    if catalog.get("capabilityCount") != 20 or len(capabilities) != 20:
        errors.append(f"{catalog_path}: expected exactly 20 decision intelligence USPs")
    capability_ids = [str(capability.get("id")) for capability in capabilities]
    for capability in capabilities:
        for field in [
            "id",
            "name",
            "summary",
            "primaryPersona",
            "decisionArtifact",
            "implementationStatus",
            "inputs",
            "outputs",
            "acceptanceChecks",
        ]:
            if not capability.get(field):
                errors.append(f"{catalog_path}: decision intelligence USP missing {field}")
        if capability.get("implementationStatus") != "implemented_as_decision_intelligence_evidence":
            errors.append(f"{catalog_path}: decision intelligence USP {capability.get('id')} has invalid status")

    processes = json.loads(process_catalog_path.read_text(encoding="utf-8")).get("processes", [])
    for process in processes:
        process_id = process.get("processId")
        folder = output_root / "processes" / str(process_id)
        plan_path = folder / "decision_intelligence_plan.json"
        if not plan_path.exists():
            errors.append(f"{plan_path}: decision intelligence process plan is missing")
            continue
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if plan.get("capabilityCount") != 20 or len(plan.get("decisionIntelligenceUsps", [])) != 20:
            errors.append(f"{plan_path}: expected 20 decision intelligence USPs")
        for capability_id in capability_ids:
            artifact_path = folder / f"{capability_id}.json"
            if not artifact_path.exists():
                errors.append(f"{artifact_path}: decision intelligence evidence artifact is missing")
                continue
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            if artifact.get("capabilityId") != capability_id:
                errors.append(f"{artifact_path}: capabilityId mismatch")
            if artifact.get("status") != "evidence-ready":
                errors.append(f"{artifact_path}: expected status evidence-ready")

    index_path = output_root / "decision_intelligence_index.csv"
    if not index_path.exists():
        errors.append(f"{index_path}: decision intelligence index is missing")
    else:
        row_count = max(0, len(index_path.read_text(encoding="utf-8").splitlines()) - 1)
        if row_count != len(processes):
            errors.append(f"{index_path}: expected {len(processes)} rows, found {row_count}")
    summary_path = output_root / "decision_intelligence_summary.json"
    if not summary_path.exists():
        errors.append(f"{summary_path}: decision intelligence summary is missing")
    if not (output_root / "README.md").exists():
        errors.append(f"{output_root / 'README.md'}: decision intelligence README is missing")
    return errors


def check_lead2order_analysis_package(root: Path) -> list[str]:
    errors: list[str] = []
    output_root = root / "outputs" / "lead2order-powerbi-analysis"
    required_files = [
        "README.md",
        "lead2order_powerbi_manifest.json",
        "measure_catalog.json",
        "kpi_problem_questions.json",
        "report_blueprint.json",
        "dax_measures.dax",
        "validation_result.json",
        "pbip/Lead2OrderAnalysis/Lead2Order.pbip",
    ]
    for filename in required_files:
        if not (output_root / filename).exists():
            errors.append(f"{output_root / filename}: required Lead2Order analysis artifact is missing")

    manifest_path = output_root / "lead2order_powerbi_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("processId") != "lead2order":
            errors.append(f"{manifest_path}: expected processId lead2order")
        if manifest.get("measureCount") != 30:
            errors.append(f"{manifest_path}: expected 30 measures")
        if manifest.get("problemQuestionCount") != 10:
            errors.append(f"{manifest_path}: expected 10 problem questions")
        if manifest.get("reportPageCount") != 6:
            errors.append(f"{manifest_path}: expected 6 report pages")

    measure_path = output_root / "measure_catalog.json"
    if measure_path.exists():
        measures = json.loads(measure_path.read_text(encoding="utf-8")).get("measures", [])
        if len(measures) != 30:
            errors.append(f"{measure_path}: expected 30 measures")
        for measure in measures:
            for field in ["name", "kpi", "expression", "question", "decision"]:
                if not measure.get(field):
                    errors.append(f"{measure_path}: measure {measure.get('name')} missing {field}")

    questions_path = output_root / "kpi_problem_questions.json"
    if questions_path.exists():
        questions = json.loads(questions_path.read_text(encoding="utf-8")).get("problemQuestions", [])
        if len(questions) != 10:
            errors.append(f"{questions_path}: expected 10 problem questions")
        for question in questions:
            for field in ["area", "question", "primaryMeasures", "drilldowns", "action"]:
                if not question.get(field):
                    errors.append(f"{questions_path}: problem question missing {field}")

    validation_path = output_root / "validation_result.json"
    if validation_path.exists():
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("status") != "pass":
            errors.append(f"{validation_path}: expected validation status pass")
        summary = validation.get("summary", {})
        if summary.get("errors") != 0 or summary.get("warnings") != 0:
            errors.append(f"{validation_path}: expected zero errors and zero warnings")

    return errors


def check_powerbi_plugin_runtime_skill_wiring(root: Path) -> list[str]:
    errors: list[str] = []
    skill_root = root / "plugins/powerbi-business-intelligence/skills"
    required_skills = [
        "powerbi-expert-mode",
        "powerbi-generalist-autopilot-mode",
        "powerbi-report-package-runtime",
        "powerbi-multi-tenant-msp-mode",
        "powerbi-reporting",
        "powerbi-pbip-tmdl-generator",
        "powerbi-live-metadata-scanner",
        "powerbi-admin-api-playbook",
        "powerbi-dax-unit-test-runner",
        "powerbi-devops-cicd",
    ]
    for skill in required_skills:
        path = skill_root / skill / "SKILL.md"
        if not path.exists():
            errors.append(f"{path}: required runtime wiring skill is missing")

    command_expectations = {
        "powerbi-expert-mode": [
            "report-package",
            "pbix-intake",
            "tenant-scan-request",
            "dax-query-request",
            "rest-deploy-request",
            "gateway-audit-request",
        ],
        "powerbi-generalist-autopilot-mode": [
            "generalist-prompt-run",
            "generalist-autopilot-run",
            "report-package",
            "runtime-max-plan",
        ],
        "powerbi-report-package-runtime": ["report-package"],
        "powerbi-reporting": ["report-package"],
        "powerbi-pbip-tmdl-generator": ["report-package"],
        "powerbi-live-metadata-scanner": ["tenant-scan-request"],
        "powerbi-admin-api-playbook": ["tenant-scan-request", "gateway-audit-request"],
        "powerbi-dax-unit-test-runner": ["dax-query-request"],
        "powerbi-devops-cicd": ["rest-deploy-request"],
        "powerbi-multi-tenant-msp-mode": ["tenant-scan-request", "gateway-audit-request"],
    }
    for skill, commands in command_expectations.items():
        path = skill_root / skill / "SKILL.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for command in commands:
            if command not in text:
                errors.append(f"{path}: expected command reference {command}")

    manifest_path = root / "plugins/powerbi-business-intelligence/.codex-plugin/plugin.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        prompts = "\n".join(manifest.get("interface", {}).get("defaultPrompt", []))
        for phrase in ["Experten Mode", "Generalisten Mode"]:
            if phrase not in prompts:
                errors.append(f"{manifest_path}: expected default prompt containing {phrase}")

    factory_path = root / "scripts/powerbi_expert_factory.py"
    if factory_path.exists():
        factory_text = factory_path.read_text(encoding="utf-8")
        for command in [
            "generalist-prompt-run",
            "generalist-autopilot-run",
            "tenant-scan-run",
            "dax-query-run",
            "rest-deploy-run",
            "gateway-audit-run",
        ]:
            if command not in factory_text:
                errors.append(f"{factory_path}: expected factory command {command}")

    matrix_path = root / "data/powerbi_runtime_usp_skill_matrix.json"
    if not matrix_path.exists():
        errors.append(f"{matrix_path}: runtime USP skill matrix is missing")
        return errors
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    entries = matrix.get("entries", [])
    runtime_catalog = json.loads((root / "data/powerbi_runtime_max_catalog.json").read_text(encoding="utf-8"))
    capabilities = runtime_catalog.get("capabilities", [])
    if matrix.get("capabilityCount") != 70 or len(entries) != 70:
        errors.append(f"{matrix_path}: expected 70 runtime USP mappings")
    entry_ids = {entry.get("capabilityId") for entry in entries}
    for capability in capabilities:
        if capability.get("id") not in entry_ids:
            errors.append(f"{matrix_path}: missing mapping for {capability.get('id')}")
    for entry in entries:
        for field in ["capabilityId", "capabilityName", "primarySkill", "cliEntrypoints", "outputArtifacts"]:
            if not entry.get(field):
                errors.append(f"{matrix_path}: mapping missing {field}")
        primary = entry.get("primarySkill")
        if primary and not (skill_root / primary / "SKILL.md").exists():
            errors.append(f"{matrix_path}: primary skill does not exist: {primary}")
    return errors


def run(root: Path) -> int:
    errors: list[str] = []
    errors.extend(check_required_files(root))
    errors.extend(
        check_json(
            [
                root / ".agents/plugins/marketplace.json",
                root / "plugins/powerbi-business-intelligence/.codex-plugin/plugin.json",
            ]
        )
    )
    errors.extend(check_github_yaml(root))
    errors.extend(check_markdown_links(root))
    errors.extend(check_root_english(root))
    errors.extend(check_industry_demo_data(root))
    errors.extend(check_powerbi_source_routing(root))
    errors.extend(check_industry_process_packs(root))
    errors.extend(check_usp_capability_coverage(root))
    errors.extend(check_powerbi_feature_factory(root))
    errors.extend(check_powerbi_execution_layer(root))
    errors.extend(check_powerbi_premium_usp_layer(root))
    errors.extend(check_powerbi_runtime_max_layer(root))
    errors.extend(check_powerbi_production_hardening(root))
    errors.extend(check_powerbi_market_differentiator_usps(root))
    errors.extend(check_powerbi_decision_intelligence_usps(root))
    errors.extend(check_lead2order_analysis_package(root))
    errors.extend(check_powerbi_plugin_runtime_skill_wiring(root))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("repository checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    return run(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
