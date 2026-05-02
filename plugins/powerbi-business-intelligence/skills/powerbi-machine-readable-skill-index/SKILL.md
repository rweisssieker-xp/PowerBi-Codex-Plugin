---
name: powerbi-machine-readable-skill-index
description: Use when the plugin needs a JSON or YAML index of Power BI skills with tags, triggers, inputs, outputs, dependencies, examples, routing hints, and capability coverage.
---

# Power BI Machine Readable Skill Index

Create a structured index so agents, docs, and governance tooling can route to the right skill.

## Output Contract

- Skill name, category, description, triggers, tags, inputs, outputs, dependencies, related skills, and example prompts.
- Coverage map by process, source system, artifact, governance area, AI/KI feature, and expert-reduction USP.
- JSON/YAML schema and validation checklist.
- Missing coverage and duplicate capability findings.

## Checks

- Keep generated index aligned with actual `SKILL.md` files.
- Avoid inventing capabilities not present in the repository.
