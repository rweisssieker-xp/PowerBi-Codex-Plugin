# Performance and Refresh Checklist

- Disable auto date/time where enterprise date tables exist.
- Remove unused columns and reduce cardinality.
- Validate query folding before incremental refresh.
- Prefer source-side filtering and aggregation where appropriate.
- Replace implicit measures with explicit measures.
- Use aggregation tables for high-volume DirectQuery/import scenarios.
- Test RLS performance separately from unrestricted queries.
- Monitor gateway CPU, memory, credentials, and refresh concurrency.
- Document API pagination, throttling, retries, and schema drift.

