# Multi-Agent BI Sprint Orchestrator

Coordinate consultant, modeler, DAX, designer, QA, and CoE agents with evidence handoffs.

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
