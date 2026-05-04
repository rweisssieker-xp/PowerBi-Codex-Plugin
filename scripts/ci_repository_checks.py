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
