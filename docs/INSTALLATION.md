# Installation

## de-DE Kurzfassung

Diese Anleitung beschreibt, wie das lokale Plugin in Codex registriert, aktiviert und validiert wird. Fuer produktive Kundenarbeit duerfen keine Tenant-, Gateway-, Quellsystem- oder Produktionsdaten-Zugangsdaten im Repository gespeichert werden.

## Prerequisites

- Codex desktop or a Codex environment that supports local plugins.
- Local access to this repository.
- Optional: Power BI Desktop, Tabular Editor, Power BI/Fabric tenant access, gateways, or source-system credentials for real implementation work.

## Local Plugin Registration

The local marketplace is defined here:

```text
.agents/plugins/marketplace.json
```

It points to:

```text
plugins/powerbi-business-intelligence
```

The plugin manifest is:

```text
plugins/powerbi-business-intelligence/.codex-plugin/plugin.json
```

## Enable the Plugin

1. Open this repository in Codex.
2. Use the local marketplace entry `powerbi-business-intelligence-marketplace`.
3. Install or enable `Power BI Business Intelligence`.
4. Verify that Codex can discover the plugin skills under `plugins/powerbi-business-intelligence/skills`.

## Validate the Repository

Run the basic checks:

```powershell
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
(Get-ChildItem plugins/powerbi-business-intelligence/skills -Recurse -Filter SKILL.md | Measure-Object).Count
```

Expected result:

- JSON validation succeeds.
- Skill count is 214 or higher when new skills are added later.

## Notes

- The plugin does not store secrets.
- Do not commit tenant credentials, gateway credentials, source-system passwords, PBIX files with sensitive data, or exported production data.
- For real customer data, use approved enterprise security, privacy, and data handling processes.
