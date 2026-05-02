# Power BI Expert Review Checklist

## Business and KPI

- KPI has owner, definition, numerator, denominator, date basis, exclusions, and validation source.
- Report pages answer specific decisions.
- Source totals reconcile to model totals.

## Semantic Model

- Fact grain is documented.
- Dimensions are conformed where needed.
- Relationships are single-direction unless justified.
- Many-to-many and bidirectional filters are tested.
- Hidden technical columns are not exposed.

## DAX

- Measures are explicit and named consistently.
- Time intelligence uses a marked date table.
- DIVIDE is used for ratios.
- Expensive iterators are justified.
- Measures are organized into display folders.

## Power Query and Refresh

- Query folding is preserved where needed.
- Incremental refresh boundaries are documented.
- Gateway and refresh identity are known.
- Schema drift and API pagination are handled.

## Security and Delivery

- RLS/OLS is tested.
- Sensitivity labels are applied where required.
- Deployment pipeline and workspace ownership are clear.
- Monitoring and support process exist.

