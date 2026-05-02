# Power BI Model Patterns

## Preferred Shape

- Use star schemas with single-direction relationships by default.
- Keep fact tables at a stable grain and avoid mixing transaction, snapshot, and balance rows in one table.
- Use surrogate keys or durable business keys; document late-arriving dimensions.
- Hide technical keys and staging columns from report users.
- Avoid many-to-many unless a bridge table is intentional and tested.
- Use calculation groups and field parameters only when they simplify report UX.

## Fact Types

- Transaction: orders, invoices, movements, events, tickets, journal lines.
- Periodic snapshot: inventory by day, customer status by month, balances by period.
- Accumulating snapshot: opportunity lifecycle, order-to-cash, procure-to-pay, case lifecycle.
- Factless fact: attendance, eligibility, coverage, entitlement, subscription activity.

## Performance

- Reduce cardinality, split date/time, disable auto date/time, remove unused columns, and prefer integer keys.
- Keep DAX measures explicit and reusable.
- Validate query folding for Power Query sources that need incremental refresh.

