---
name: powerbi-process-mining
description: Use when Power BI analysis needs event logs, process variants, bottleneck detection, rework loops, conformance checks, cycle time, throughput, lead time, or process mining for Order2Cash, Procure2Pay, Production, Service, Maintenance, or Finance processes.
---

# Power BI Process Mining

Use this skill when the question is about how work flows through a process, not only final KPI totals.

## Event Log Design

Required fields:

- Case ID: order, PO, production order, service case, invoice, asset, claim.
- Activity: created, approved, released, blocked, delivered, billed, paid, closed.
- Timestamp: event date/time with timezone and late posting rules.
- Resource: user, team, plant, supplier, customer, machine.
- Attributes: amount, product, status, reason, company, plant, channel.

## Analysis Patterns

- Variant analysis.
- Bottleneck and waiting time.
- Rework and loops.
- Conformance against expected path.
- SLA and aging.
- Handover and ownership.
- Root-cause decomposition by source system and process step.

## Output Requirements

- Include event log spec, case grain, activity taxonomy, timestamp rules, source objects, and validation checks.
- Flag when source systems lack reliable timestamps or document-flow keys.

