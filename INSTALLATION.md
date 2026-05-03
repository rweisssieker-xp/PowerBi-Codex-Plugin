# Installation

## Prerequisites

- Codex desktop or a Codex environment that supports local plugins.
- Local access to this repository.
- Optional for real implementation work: Power BI Desktop, Tabular Editor, Power BI/Fabric tenant access, gateways, and source-system credentials.

## Register The Local Plugin

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

## Enable The Plugin

1. Open this repository in Codex.
2. Use the local marketplace entry `powerbi-business-intelligence-marketplace`.
3. Install or enable `Power BI Business Intelligence`.
4. Verify that Codex can discover the plugin skills under `plugins/powerbi-business-intelligence/skills`.

## Validate The Repository

Run:

```powershell
python -m unittest tests\test_powerbi_expert_factory.py -v
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
```

## Security Notes

Do not commit tenant credentials, gateway credentials, source-system passwords, PBIX files with sensitive data, or exported production data. Use approved enterprise security, privacy, and data handling processes for real customer work.
