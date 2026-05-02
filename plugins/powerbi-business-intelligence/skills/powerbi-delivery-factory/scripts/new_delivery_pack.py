#!/usr/bin/env python3
"""Create a complete Power BI delivery pack folder."""

from __future__ import annotations

import argparse
from pathlib import Path


FILES = {
    "POWERBI_REPORT_SPEC.md": "# Power BI Report Spec\n\n## Pages\n\n1. Executive overview\n2. Driver analysis\n3. Flow/cohort/aging\n4. Exceptions\n5. Detail and reconciliation\n",
    "SEMANTIC_MODEL_SPEC.md": "# Semantic Model Spec\n\n## Facts\n\n## Dimensions\n\n## Relationships\n\n## Security\n",
    "QUERY_EXTRACTION_PLAN.md": "# Query Extraction Plan\n\n## Sources\n\n## Connector Pattern\n\n## Incremental Refresh\n\n## Reconciliation\n",
    "DAX_MEASURE_CATALOG.csv": "measure,table,business_definition,expression,validation_source\n",
    "VALIDATION_PLAN.md": "# Validation Plan\n\n## Row Counts\n\n## KPI Totals\n\n## RLS Tests\n\n## Refresh Tests\n",
    "RLS_SECURITY_SPEC.md": "# RLS Security Spec\n\n## Roles\n\n## Rules\n\n## Test Users\n\n## Denied Access Cases\n",
    "DEPLOYMENT_CHECKLIST.md": "# Deployment Checklist\n\n- [ ] Workspace selected\n- [ ] Gateway configured\n- [ ] Credentials configured\n- [ ] RLS tested\n- [ ] Refresh scheduled\n- [ ] Owner assigned\n",
    "MAINTENANCE_RUNBOOK.md": "# Maintenance Runbook\n\n## Owners\n\n## Refresh SLA\n\n## Monitoring\n\n## Support Process\n",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--out-dir", type=Path, default=Path("powerbi-delivery-pack"))
    args = parser.parse_args()

    root = args.out_dir
    root.mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(f"# {args.name} Delivery Pack\n\nGenerated Power BI delivery pack.\n", encoding="utf-8")
    for file_name, content in FILES.items():
        (root / file_name).write_text(content, encoding="utf-8")
    print(f"Wrote delivery pack to {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

