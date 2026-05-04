---
name: powerbi-generalist-autopilot-mode
description: Use when the user asks for Generalisten Mode, Prozess Manager mode, Process Owner mode, autonomous BI delivery, or wants the plugin to handle Power BI work end-to-end without requiring expert knowledge.
---

# Power BI Generalist Autopilot Mode

Use Generalist Autopilot Mode for Prozess Manager, Process Owner, business owners, and non-technical stakeholders who want the plugin to autonomously turn a business/process question into usable Power BI delivery artifacts.

## Operating Contract

- Minimize questions. Make reasonable assumptions and document them.
- Translate business language into process scope, KPI tree, source profile, semantic model plan, DAX plan, report pages, action cockpit, validation plan, and owner acceptance pack.
- Prefer `report-package` as the primary autonomous delivery path.
- Produce business-readable outputs first, with technical artifacts attached.
- Escalate only for credentials, destructive actions, external writes, unclear legal/security constraints, or missing source access.

## Runtime Commands

Default autonomous package:

```powershell
python scripts\powerbi_expert_factory.py generalist-prompt-run --prompt "<free-text process owner request>" --out outputs\autopilot-runs\<case-name>
python scripts\powerbi_expert_factory.py report-package --process <process-id> --sources "<source description>" --goal "<business goal>" --out outputs\report-packages\<process-id>
python scripts\powerbi_expert_factory.py generalist-autopilot-run --process <process-id> --sources "<source description>" --goal "<business goal>" --out outputs\autopilot-runs\<process-id>
```

Optional full capability plan:

```powershell
python scripts\powerbi_expert_factory.py runtime-max-plan --process <process-id> --out outputs\powerbi-runtime-max-layer\<process-id>-runtime-max-plan.json
```

## Autonomous Delivery Flow

1. Interpret the business/process question.
2. Pick or normalize the process chain.
3. Draft KPI contracts and decision questions.
4. Generate the report/model package.
5. Add validation, acceptance, and improvement artifacts.
6. Return the next business actions and owner signoff checklist.

## Output Requirements

- Explain what was generated in Process Owner language.
- Include the output folder and next validation command.
- Include assumptions, owner questions, action backlog, and release readiness.
- Avoid expert jargon unless needed for evidence.

## Checks

- Do not ask the user to design tables, DAX, Power Query, or visuals unless the request explicitly asks for expert control.
- Keep credentials external.
- Never perform tenant changes, deployments, permissions, or ticket creation without explicit approval.
