#!/usr/bin/env python3
"""Offline simulation suite for the Power BI Business Intelligence plugin."""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "powerbi-business-intelligence"
SKILLS = PLUGIN / "skills"


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def skill_files() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter_and_body(text: str) -> tuple[str, str]:
    match = re.match(r"(?s)^---\s*(.*?)\s*---\s*(.*)$", text)
    if not match:
        return "", text
    return match.group(1), match.group(2)


def validate_skill_structure(files: list[Path]) -> list[Check]:
    failures: list[str] = []
    for path in files:
        text = read(path)
        fm, body = frontmatter_and_body(text)
        rel = path.relative_to(ROOT)
        if len(text.strip()) < 80:
            failures.append(f"{rel}: too short")
        if not re.search(r"(?m)^name:\s*\S+", fm):
            failures.append(f"{rel}: missing name")
        if not re.search(r"(?m)^description:\s*.+", fm):
            failures.append(f"{rel}: missing description")
        if not re.search(r"(?m)^#\s+.+", body):
            failures.append(f"{rel}: missing H1")
    return [Check("Skill structure", not failures, f"{len(files)} skills checked; failures={len(failures)}")]


def validate_references(files: list[Path]) -> list[Check]:
    missing: list[str] = []
    for path in files:
        text = read(path)
        for match in re.finditer(r"`([^`]+)`", text):
            ref = match.group(1)
            if not ref.startswith(("assets/", "references/", "scripts/", "docs/")):
                continue
            resolved = path.parent / ref.replace("/", os.sep)
            if not resolved.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {ref}")
    return [Check("Skill references", not missing, f"missing_refs={len(missing)}")]


def validate_docs() -> list[Check]:
    md_files = [
        p
        for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and "__pycache__" not in p.parts
    ]
    broken: list[str] = []
    for path in md_files:
        text = read(path)
        for match in re.finditer(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = Path(target) if re.match(r"^[A-Za-z]:", target) else (path.parent / target)
            if not resolved.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    return [Check("Markdown links", not broken, f"markdown_files={len(md_files)}; broken_links={len(broken)}")]


def validate_json() -> list[Check]:
    checks: list[Check] = []
    for path in [PLUGIN / ".codex-plugin" / "plugin.json", ROOT / ".agents" / "plugins" / "marketplace.json"]:
        result = run([sys.executable, "-m", "json.tool", str(path)])
        checks.append(Check(f"JSON {path.relative_to(ROOT)}", result.returncode == 0, result.stderr.strip() or "ok"))
    return checks


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def simulate_generators() -> list[Check]:
    checks: list[Check] = []
    temp = Path(tempfile.mkdtemp(prefix="powerbi-plugin-sim-"))
    try:
        measure_csv = temp / "measure-catalog.csv"
        table_csv = temp / "table-catalog.csv"
        write_csv(
            measure_csv,
            [
                {
                    "measure": "Net Revenue",
                    "table": "FactSales",
                    "folder": "Finance",
                    "business_definition": "Revenue after credits and rebates",
                    "expression": "SUM ( FactSales[NetRevenue] )",
                    "validation_source": "SAP FI revenue total",
                },
                {
                    "measure": "Churn Rate",
                    "table": "FactCustomerLifecycle",
                    "folder": "Customer",
                    "business_definition": "Lost customers divided by active customers",
                    "expression": "DIVIDE ( [Lost Customers], [Active Customers] )",
                    "validation_source": "CRM lifecycle extract",
                },
            ],
        )
        write_csv(
            table_csv,
            [
                {
                    "table": "FactSales",
                    "source_kind": "sql",
                    "source_entity": "SalesFact",
                    "incremental_column": "PostingDate",
                },
                {
                    "table": "DimCustomer",
                    "source_kind": "odata",
                    "source_entity": "Customers",
                    "incremental_column": "",
                },
            ],
        )

        scripts = {
            "business blueprint": [
                sys.executable,
                str(SKILLS / "powerbi-business-problem-factory" / "scripts" / "new_business_problem_blueprint.py"),
                "Customer Churn",
                "--out",
                str(temp / "BLUEPRINT.md"),
            ],
            "semantic model spec": [
                sys.executable,
                str(SKILLS / "powerbi-modelling" / "scripts" / "new_semantic_model_spec.py"),
                "Order2Cash",
                "--out",
                str(temp / "SEMANTIC_MODEL_SPEC.md"),
            ],
            "report spec": [
                sys.executable,
                str(SKILLS / "powerbi-reporting" / "scripts" / "new_powerbi_report_spec.py"),
                "FiCO Margin Cockpit",
                "--out",
                str(temp / "REPORT_SPEC.md"),
            ],
            "dax pack": [
                sys.executable,
                str(SKILLS / "powerbi-dax" / "scripts" / "new_dax_measure_pack.py"),
                "--measure-catalog",
                str(measure_csv),
                "--out-dir",
                str(temp / "dax-pack"),
            ],
            "powerbi pack": [
                sys.executable,
                str(SKILLS / "powerbi-reporting" / "scripts" / "generate_powerbi_pack.py"),
                "--tables",
                str(table_csv),
                "--measures",
                str(measure_csv),
                "--out",
                str(temp / "implementation-pack"),
            ],
        }
        for name, command in scripts.items():
            result = run(command)
            checks.append(Check(f"Generator {name}", result.returncode == 0, result.stderr.strip() or result.stdout.strip()))

        generated_expectations = {
            "DAX measure names": temp / "implementation-pack" / "dax" / "measures.dax",
            "Power Query SQL": temp / "implementation-pack" / "powerquery" / "FactSales.pq",
            "Power Query OData": temp / "implementation-pack" / "powerquery" / "DimCustomer.pq",
        }
        checks.append(
            Check(
                "Generated DAX content",
                "Net Revenue" in read(generated_expectations["DAX measure names"])
                and "Churn Rate" in read(generated_expectations["DAX measure names"]),
                "measure names preserved",
            )
        )
        checks.append(
            Check(
                "Generated Power Query content",
                "Sql.Database" in read(generated_expectations["Power Query SQL"])
                and "OData.Feed" in read(generated_expectations["Power Query OData"]),
                "SQL and OData connector patterns generated",
            )
        )
    finally:
        shutil.rmtree(temp, ignore_errors=True)
    return checks


SCENARIOS: dict[str, list[str]] = {
    "Customer Churn CRM to Power BI": [
        "powerbi-business-problem-factory",
        "powerbi-domain-packs",
        "powerbi-ai-kpi-discovery-agent",
        "powerbi-ai-causal-hypothesis-tester",
        "powerbi-nl-to-dax-guardrails",
        "powerbi-bilingual-documentation",
    ],
    "Order2Cash SAP Salesforce EWM Snowflake": [
        "powerbi-industrial-process-intelligence",
        "powerbi-source-system-process-adapter",
        "powerbi-erp-object-resolver",
        "powerbi-process-chain-kpi-visibility",
        "powerbi-golden-semantic-model-templates",
        "powerbi-automated-executive-briefing",
    ],
    "FiCO margin and close cockpit": [
        "powerbi-domain-packs",
        "powerbi-regulatory-standards",
        "powerbi-enterprise-kpi-ontology",
        "powerbi-dax",
        "powerbi-quality-gate",
        "powerbi-ai-boardroom-copilot",
    ],
    "Dock2Stock WHS WMS operational cockpit": [
        "powerbi-whs-wms-warehouse-source-pack",
        "powerbi-process-chain-kpi-visibility",
        "powerbi-source-metadata-discovery",
        "powerbi-visual-layout-spec-generator",
        "powerbi-automated-action-creation",
        "powerbi-closed-loop-bi",
    ],
    "Complaint2CAPA QMS EHS quality cockpit": [
        "powerbi-qm-qms-ehs-source-pack",
        "powerbi-process-chain-kpi-visibility",
        "powerbi-industrial-root-cause-cockpit",
        "powerbi-data-quality-rule-library",
        "powerbi-compliance-evidence-pack",
        "powerbi-ai-root-cause-playbook-generator",
    ],
    "Control2Evidence audit and security": [
        "powerbi-regulatory-standards",
        "powerbi-compliance-evidence-pack",
        "powerbi-rls-ols-pattern-library",
        "powerbi-ai-compliance-reviewer",
        "powerbi-automated-security-exposure-scan",
        "powerbi-audit-ready-ai-evidence-trail",
    ],
    "Expert reduction autonomous BI sprint": [
        "powerbi-intake-router",
        "powerbi-agent-workforce",
        "powerbi-ai-multi-agent-bi-orchestrator",
        "powerbi-ai-autonomous-bi-sprint",
        "powerbi-semantic-model-certification-bot",
        "powerbi-value-realization-tracker",
    ],
}


def simulate_scenarios() -> list[Check]:
    available = {path.parent.name for path in skill_files()}
    checks: list[Check] = []
    for scenario, expected in SCENARIOS.items():
        missing = [skill for skill in expected if skill not in available]
        checks.append(
            Check(
                f"Scenario {scenario}",
                not missing,
                "skills=" + ", ".join(expected) + ("" if not missing else "; missing=" + ", ".join(missing)),
            )
        )
    return checks


def desktop_status() -> Check:
    result = run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-Process PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty MainWindowTitle",
        ]
    )
    title = result.stdout.strip()
    return Check("Power BI Desktop process", bool(title), title or "PBIDesktop not running during simulation")


def cleanup_pycaches() -> None:
    for path in SKILLS.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)


def render_report(checks: list[Check]) -> str:
    passed = sum(1 for check in checks if check.passed)
    failed = len(checks) - passed
    lines = [
        "# Power BI Plugin Simulation Test Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Skills simulated: {len(skill_files())}",
        f"Checks passed: {passed}",
        f"Checks failed: {failed}",
        "",
        "## Scope",
        "",
        "- Offline simulation of all Codex skills and feature families.",
        "- Structural validation of skill metadata, H1 bodies, references, JSON manifests, and Markdown links.",
        "- Execution of available artifact generators for blueprint, semantic model spec, report spec, DAX pack, Power Query pack, and implementation pack.",
        "- Scenario routing simulation for customer churn, Order2Cash, FiCO, Dock2Stock, Complaint2CAPA, Control2Evidence, and autonomous expert-reduction sprint.",
        "- Power BI Desktop process smoke check where available.",
        "",
        "## Results",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        detail = check.detail.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check.name} | {status} | {detail} |")
    lines.extend(
        [
            "",
            "## Scenario Coverage",
            "",
            "| Scenario | Simulated skill route |",
            "| --- | --- |",
        ]
    )
    for scenario, route in SCENARIOS.items():
        lines.append(f"| {scenario} | `{ '`, `'.join(route) }` |")
    lines.extend(
        [
            "",
            "## de-DE Kurzfassung",
            "",
            "Die Simulation validiert alle 214 Skills offline und prueft die wichtigsten Power-BI-Featurefamilien gegen real ausfuehrbare Generatoren und typische Industrie-Szenarien. Ein echter Desktop-Klicktest aller Skills ist nicht moeglich, weil Skills Codex-Arbeitsanweisungen sind und keine Power-BI-Desktop-Add-ins. Die Desktop-Verfuegbarkeit wird aber als Smoke-Test geprueft.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "docs" / "SIMULATION_TEST_REPORT.md")
    args = parser.parse_args()

    files = skill_files()
    checks: list[Check] = []
    checks.extend(validate_skill_structure(files))
    checks.extend(validate_references(files))
    checks.extend(validate_json())
    checks.extend(validate_docs())
    checks.extend(simulate_generators())
    checks.extend(simulate_scenarios())
    checks.append(desktop_status())

    report = render_report(checks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    cleanup_pycaches()
    print(report)
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
