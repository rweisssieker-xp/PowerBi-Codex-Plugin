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
