"""Generate executable feature contracts for the 20 Power BI expert-replacement USPs."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USP_CATALOG_PATH = ROOT / "data" / "powerbi_usp_capability_catalog.json"
PROCESS_CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
FEATURE_CATALOG_PATH = ROOT / "data" / "powerbi_feature_catalog.json"
OUTPUT_ROOT = ROOT / "outputs" / "powerbi-feature-factory"


FEATURE_IMPLEMENTATIONS = {
    "one_click_process_to_pbip": {
        "implementationType": "generator",
        "inputs": ["processId", "sourceMode", "sourceProfile", "outputFolder"],
        "outputs": ["PBIP folder", "TMDL semantic model", "PBIR report spec", "validation evidence"],
        "cliCommands": [
            "python scripts\\build_industry_process_packs.py",
            "python scripts\\powerbi_expert_factory.py feature-plan --process <processId> --out <file>",
        ],
        "acceptanceChecks": ["process pack exists", "model spec exists", "report page specs exist"],
    },
    "connector_aware_source_interview": {
        "implementationType": "source-intake",
        "inputs": ["source system", "connector category", "authentication mode", "gateway decision"],
        "outputs": ["native connector recommendation", "required source decisions", "refresh constraints"],
        "cliCommands": [
            "python scripts\\build_powerbi_source_routing.py",
            "python scripts\\powerbi_expert_factory.py feature-plan --process <processId>",
        ],
        "acceptanceChecks": ["native connector declared", "gateway owner declared", "schema drift decision declared"],
    },
    "kpi_contract_negotiator": {
        "implementationType": "kpi-contract",
        "inputs": ["business question", "grain", "date basis", "numerator", "denominator", "tolerance"],
        "outputs": ["KPI contract", "DAX measure intent", "test tolerance"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["KPI owner exists", "measure strategy exists", "acceptance criteria exists"],
    },
    "ambiguous_path_prevention_engine": {
        "implementationType": "validator",
        "inputs": ["relationships.tmdl", "model_spec.json"],
        "outputs": ["model graph validation result", "ambiguous path errors"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py validate --project <pbip-folder>"],
        "acceptanceChecks": ["no fact-to-fact relationship", "no alternate active relationship path"],
    },
    "frown_to_fix_knowledge_loop": {
        "implementationType": "triage",
        "inputs": ["Power BI frown message", "stack trace", "artifact path"],
        "outputs": ["root-cause class", "repair checklist", "validation rerun command"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["error class mapped", "repair action mapped", "post-fix validation declared"],
    },
    "visual_binding_compiler": {
        "implementationType": "validator",
        "inputs": ["report_pages.json", "visual.json", "model tables", "measures"],
        "outputs": ["visual binding validation result", "missing field errors"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py validate --project <pbip-folder>"],
        "acceptanceChecks": ["all columns exist", "all measures exist", "visual count reported"],
    },
    "measure_test_harness": {
        "implementationType": "test-harness",
        "inputs": ["DAX catalog", "demo data", "expected KPI tolerances"],
        "outputs": ["measure test plan", "reconciliation strategy", "risk score"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["each KPI has DAX", "each KPI has expected-result strategy"],
    },
    "process_digital_twin_layer": {
        "implementationType": "process-mining",
        "inputs": ["cases.csv", "events.csv", "kpi_snapshots.csv"],
        "outputs": ["case flow", "bottleneck candidates", "simulation baseline"],
        "cliCommands": ["python scripts\\build_industry_process_demo_data.py"],
        "acceptanceChecks": ["case grain exists", "event log exists", "KPI snapshots exist"],
    },
    "action_cockpit_generator": {
        "implementationType": "report-generator",
        "inputs": ["exceptions", "owners", "root causes", "value impact"],
        "outputs": ["owner action cockpit page", "action backlog fields", "value priority"],
        "cliCommands": ["python scripts\\build_industry_process_packs.py"],
        "acceptanceChecks": ["ActionRequired available", "owner field available", "action page declared"],
    },
    "rls_ols_policy_generator": {
        "implementationType": "security-design",
        "inputs": ["process owner", "organization scope", "sensitive fields"],
        "outputs": ["RLS role draft", "OLS sensitivity notes", "identity mapping requirements"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["role declared", "scope rule declared", "enterprise identity mapping noted"],
    },
    "source_to_kpi_lineage": {
        "implementationType": "lineage",
        "inputs": ["source routes", "model tables", "DAX measures", "visual specs"],
        "outputs": ["source-to-KPI lineage graph", "governance evidence"],
        "cliCommands": ["python scripts\\build_powerbi_feature_factory.py"],
        "acceptanceChecks": ["source linked", "model table linked", "measure linked", "visual linked"],
    },
    "process_pack_marketplace": {
        "implementationType": "catalog",
        "inputs": ["industry process catalog", "process pack outputs"],
        "outputs": ["pack index", "reuse metadata", "selection criteria"],
        "cliCommands": ["python scripts\\build_industry_process_packs.py"],
        "acceptanceChecks": ["pack indexed", "domain assigned", "KPI library linked"],
    },
    "industry_variant_packs": {
        "implementationType": "variant-engine",
        "inputs": ["industry", "plant/site", "source systems", "compliance context"],
        "outputs": ["industry variant metadata", "source variants", "KPI variants"],
        "cliCommands": ["python scripts\\build_industry_process_demo_data.py"],
        "acceptanceChecks": ["domain exists", "source systems exist", "industry context exists"],
    },
    "coe_certification_bot": {
        "implementationType": "governance",
        "inputs": ["quality gate", "validation evidence", "owner signoff"],
        "outputs": ["certification decision", "release evidence", "open risks"],
        "cliCommands": ["python scripts\\ci_repository_checks.py"],
        "acceptanceChecks": ["required checks pass", "evidence exists", "release blockers listed"],
    },
    "report_consolidation_ai": {
        "implementationType": "portfolio-optimizer",
        "inputs": ["report inventory", "KPI names", "measure definitions"],
        "outputs": ["duplicate report candidates", "reuse target", "retirement proposal"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["KPI names comparable", "measure names comparable", "process pack reuse target exists"],
    },
    "semantic_model_refactoring": {
        "implementationType": "model-refactoring",
        "inputs": ["flat tables", "candidate keys", "measures", "relationships"],
        "outputs": ["fact/dimension split", "relationship plan", "renamed semantic objects"],
        "cliCommands": ["python scripts\\build_industry_process_packs.py"],
        "acceptanceChecks": ["facts declared", "dimensions declared", "many-to-one relationships declared"],
    },
    "query_folding_verifier": {
        "implementationType": "source-validator",
        "inputs": ["connector mode", "Power Query/M", "source capability matrix"],
        "outputs": ["folding expectation", "DirectQuery risk", "fallback import recommendation"],
        "cliCommands": ["python scripts\\build_powerbi_source_routing.py"],
        "acceptanceChecks": ["query folding property declared", "source mode declared", "fallback declared"],
    },
    "refresh_failure_triage": {
        "implementationType": "operations",
        "inputs": ["refresh error", "gateway settings", "privacy level", "schema drift evidence"],
        "outputs": ["failure class", "repair owner", "retry/rollback decision"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["gateway decision exists", "schema drift handling exists", "refresh check exists"],
    },
    "business_value_realization_tracker": {
        "implementationType": "value-management",
        "inputs": ["actions", "financial impact", "status", "owner"],
        "outputs": ["value realization dashboard spec", "action ROI", "benefit tracking"],
        "cliCommands": ["python scripts\\build_industry_process_packs.py"],
        "acceptanceChecks": ["value field exists", "action field exists", "owner action cockpit exists"],
    },
    "boardroom_narrative_generator": {
        "implementationType": "narrative",
        "inputs": ["KPI status", "root causes", "financial impact", "decisions needed"],
        "outputs": ["executive narrative", "decision brief", "boardroom page spec"],
        "cliCommands": ["python scripts\\powerbi_expert_factory.py feature-plan --process <processId>"],
        "acceptanceChecks": ["executive page exists", "KPI status exists", "decision path exists"],
    },
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_feature_catalog() -> list[dict]:
    usp_catalog = load_json(USP_CATALOG_PATH)
    features: list[dict] = []
    for capability in usp_catalog["capabilities"]:
        implementation = FEATURE_IMPLEMENTATIONS[capability["id"]]
        feature = {
            **capability,
            "implementationStatus": "implemented_as_executable_contract",
            "implementationType": implementation["implementationType"],
            "inputs": implementation["inputs"],
            "outputs": implementation["outputs"],
            "cliCommands": implementation["cliCommands"],
            "acceptanceChecks": implementation["acceptanceChecks"],
            "contractPath": f"outputs/powerbi-feature-factory/{capability['id']}/feature_contract.json",
            "validationContractPath": f"outputs/powerbi-feature-factory/{capability['id']}/validation_contract.json",
            "cliRecipePath": f"outputs/powerbi-feature-factory/{capability['id']}/cli_recipe.md",
        }
        features.append(feature)

    payload = {
        "version": "2026-05-04",
        "description": "Executable feature catalog for all 20 Power BI Expert-Replacement Factory USPs.",
        "featureCount": len(features),
        "features": features,
    }
    write_json(FEATURE_CATALOG_PATH, payload)
    return features


def write_feature_outputs(features: list[dict]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for feature in features:
        folder = OUTPUT_ROOT / feature["id"]
        folder.mkdir(parents=True, exist_ok=True)
        contract = {
            "id": feature["id"],
            "name": feature["name"],
            "summary": feature["summary"],
            "implementationStatus": feature["implementationStatus"],
            "implementationType": feature["implementationType"],
            "inputs": feature["inputs"],
            "outputs": feature["outputs"],
            "requiredArtifacts": feature["requiredArtifacts"],
            "evidence": feature["evidence"],
            "cliCommands": feature["cliCommands"],
        }
        validation = {
            "id": feature["id"],
            "name": feature["name"],
            "acceptanceChecks": feature["acceptanceChecks"],
            "minimumEvidence": feature["evidence"],
            "blockingRule": "The feature is not release-ready for a process if any acceptance check lacks generated evidence.",
        }
        write_json(folder / "feature_contract.json", contract)
        write_json(folder / "validation_contract.json", validation)
        (folder / "cli_recipe.md").write_text(
            f"# {feature['name']} CLI Recipe\n\n"
            f"{feature['summary']}\n\n"
            "## Commands\n\n"
            + "\n".join(f"```powershell\n{command}\n```" for command in feature["cliCommands"])
            + "\n\n## Acceptance Checks\n\n"
            + "\n".join(f"- {check}" for check in feature["acceptanceChecks"])
            + "\n",
            encoding="utf-8",
        )
        rows.append(
            {
                "FeatureID": feature["id"],
                "FeatureName": feature["name"],
                "ImplementationType": feature["implementationType"],
                "Contract": feature["contractPath"],
                "ValidationContract": feature["validationContractPath"],
            }
        )

    with (OUTPUT_ROOT / "feature_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_process_matrix(features: list[dict]) -> None:
    processes = load_json(PROCESS_CATALOG_PATH)["processes"]
    rows = []
    for process in processes:
        for feature in features:
            rows.append(
                {
                    "ProcessID": process["processId"],
                    "ProcessName": process["name"],
                    "Domain": process["domain"],
                    "FeatureID": feature["id"],
                    "FeatureName": feature["name"],
                    "ImplementationStatus": feature["implementationStatus"],
                    "Contract": feature["contractPath"],
                }
            )
    with (OUTPUT_ROOT / "process_feature_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_readme(features: list[dict]) -> None:
    lines = [
        "# Power BI Feature Factory",
        "",
        "Executable feature contracts for the 20 Power BI Expert-Replacement Factory USPs.",
        "",
        "Generated artifacts:",
        "",
        "- `feature_index.csv`: all executable USP feature contracts.",
        "- `process_feature_matrix.csv`: all 20 features mapped to every industrial process pack.",
        "- `<feature>/feature_contract.json`: machine-readable input/output and command contract.",
        "- `<feature>/validation_contract.json`: release-readiness checks for the feature.",
        "- `<feature>/cli_recipe.md`: local commands and acceptance checks.",
        "",
        "## Features",
        "",
    ]
    lines.extend(f"- `{feature['id']}`: {feature['name']}" for feature in features)
    (OUTPUT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    features = build_feature_catalog()
    write_feature_outputs(features)
    write_process_matrix(features)
    write_readme(features)
    print(f"generated executable contracts for {len(features)} USP features")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
