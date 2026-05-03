# Governance

This repository is governed as a Power BI Expert-Replacement Factory. Changes should improve one or more of these areas:

- Power BI semantic modeling, DAX, Power Query/M, report design, validation, or governance.
- Process Owner and Process Manager self-service analytics.
- Source-system-aware process analytics packs.
- Executable trust layers, tests, schemas, templates, or evidence.
- Clear GitHub documentation and contribution workflows.

## Decision Rules

- Validation evidence beats assertions.
- KPI contracts come before generated DAX.
- Native source routing comes before generated M.
- Star-schema model quality comes before report design.
- Security and credential safety are release blockers.
- Human Process Owners still approve KPI meaning and business accountability.

## Maintainer Responsibilities

Maintainers are responsible for:

- Keeping repository structure navigable.
- Reviewing skill quality and trigger clarity.
- Blocking secrets, tenant-specific data, and customer-sensitive content.
- Requiring validation for generated PBIP/TMDL/PBIR artifacts.
- Preserving governance boundaries between AI assistance and business ownership.
