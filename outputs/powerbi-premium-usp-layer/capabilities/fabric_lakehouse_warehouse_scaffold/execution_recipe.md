# Fabric Lakehouse/Warehouse Scaffold

Generate optional Fabric Lakehouse, Warehouse, Notebook, and Pipeline architecture scaffolds.

## Runtime Contract

- Read process context from the selected process pack.
- Use generated source profiles, semantic compile plans, lineage, and acceptance packs.
- Persist metadata, generated plans, and validation evidence only.
- Never persist credentials, tokens, or tenant secrets.

## Acceptance Checks

- contract exists
- process mapping exists
- evidence requirements are explicit
- no credentials or tenant secrets are persisted
