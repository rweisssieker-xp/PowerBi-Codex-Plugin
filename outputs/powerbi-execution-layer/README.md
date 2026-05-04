# Power BI Execution Layer

Concrete execution artifacts for all 20 Power BI Expert-Replacement Factory features across all 32 process packs.

- `processes/<process>/source_profile.json`: real demo-source profiling output.
- `processes/<process>/m_query_templates.json`: native Power Query/M templates.
- `processes/<process>/schema_drift_contract.json`: source compatibility contract.
- `processes/<process>/semantic_compile_plan.json`: semantic model compiler input.
- `processes/<process>/report_materialization_plan.json`: PBIR materialization plan.
- `processes/<process>/dax_expected_results_plan.json`: DAX test strategy.
- `processes/<process>/lineage_graph.json`: source-to-KPI/report lineage.
- `processes/<process>/process_owner_acceptance_pack.json`: owner signoff pack.
- `execution_index.csv`: process-level execution index.
