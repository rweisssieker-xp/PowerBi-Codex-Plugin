import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.powerbi_expert_factory import (
    build_dax_query_run_request,
    build_feature_delivery_plan,
    build_gateway_audit_request,
    build_generalist_autopilot_run,
    build_generalist_prompt_run,
    build_market_differentiator_usp_plan,
    build_premium_usp_plan,
    build_production_hardening_plan,
    build_powerbi_rest_deployment_request,
    build_powerbi_report_package,
    build_runtime_max_plan,
    build_process_delivery,
    build_tenant_scan_request,
    load_feature_catalog,
    load_market_differentiator_usp_catalog,
    load_premium_usp_catalog,
    load_production_hardening_catalog,
    load_runtime_max_catalog,
    parse_model,
    run_dax_query_executor,
    run_gateway_audit_executor,
    run_powerbi_rest_executor,
    run_tenant_scan_executor,
    run_pbix_binary_intake,
    run_acceptance,
    validate_model_graph,
    validate_native_sources,
    validate_visual_bindings,
)
from zipfile import ZipFile


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class PowerBiExpertFactoryTests(unittest.TestCase):
    def make_project(self) -> Path:
        root = Path(tempfile.mkdtemp())
        definition = root / "Order2Cash.SemanticModel" / "definition"
        report = root / "Order2Cash.Report" / "definition"
        write(
            definition / "tables" / "Dim_Customer.tmdl",
            """table Dim_Customer
\tcolumn CustomerID
\t\tdataType: string
\t\tsourceColumn: [CustomerID]

\tpartition Dim_Customer = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Excel.Workbook(File.Contents("customers.xlsx"), null, true)
\t\t\tin
\t\t\t    Source
""",
        )
        write(
            definition / "tables" / "Fact_Sales.tmdl",
            """table Fact_Sales
\tcolumn CustomerID
\t\tdataType: string
\t\tsourceColumn: [CustomerID]

\tcolumn Amount
\t\tdataType: double
\t\tsourceColumn: [Amount]

\tmeasure 'Sales Amount' =
\t\tSUM(Fact_Sales[Amount])
\t\tformatString: #,0.00

\tpartition Fact_Sales = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("sales.csv"), [Delimiter = ","])
\t\t\tin
\t\t\t    Source
""",
        )
        write(
            definition / "relationships.tmdl",
            """relationship rel_sales_customer
\tfromColumn: Fact_Sales.CustomerID
\ttoColumn: Dim_Customer.CustomerID
""",
        )
        write(
            report / "pages" / "ReportSection01" / "visuals" / "Visual0101" / "visual.json",
            json.dumps(
                {
                    "name": "Visual0101",
                    "visual": {
                        "visualType": "tableEx",
                        "query": {
                            "queryState": {
                                "Values": {
                                    "projections": [
                                        {
                                            "field": {
                                                "Column": {
                                                    "Expression": {"SourceRef": {"Entity": "Fact_Sales"}},
                                                    "Property": "Amount",
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                    },
                }
            ),
        )
        return root

    def test_parse_model_collects_tables_measures_and_relationships(self):
        project = self.make_project()
        model = parse_model(project)

        self.assertIn("Fact_Sales", model.tables)
        self.assertIn("Dim_Customer", model.tables)
        self.assertIn("Sales Amount", model.tables["Fact_Sales"].measures)
        self.assertEqual(len(model.relationships), 1)

    def test_model_graph_validator_accepts_star_schema(self):
        result = validate_model_graph(parse_model(self.make_project()))

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["errors"], [])

    def test_model_graph_validator_rejects_fact_to_fact(self):
        project = self.make_project()
        write(
            project / "Order2Cash.SemanticModel" / "definition" / "relationships.tmdl",
            """relationship rel_bad
\tfromColumn: Fact_Sales.CustomerID
\ttoColumn: Fact_Returns.CustomerID
""",
        )
        result = validate_model_graph(parse_model(project))

        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("Fact_* -> Dim_*" in error for error in result["errors"]))

    def test_model_graph_validator_allows_shared_dimensions_across_facts(self):
        project = self.make_project()
        write(
            project / "Order2Cash.SemanticModel" / "definition" / "tables" / "Fact_Returns.tmdl",
            """table Fact_Returns
\tcolumn CustomerID
\t\tdataType: string
\t\tsourceColumn: [CustomerID]

\tcolumn Amount
\t\tdataType: double
\t\tsourceColumn: [Amount]

\tpartition Fact_Returns = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("returns.csv"), [Delimiter = ","])
\t\t\tin
\t\t\t    Source
""",
        )
        write(
            project / "Order2Cash.SemanticModel" / "definition" / "relationships.tmdl",
            """relationship rel_sales_customer
\tfromColumn: Fact_Sales.CustomerID
\ttoColumn: Dim_Customer.CustomerID

relationship rel_returns_customer
\tfromColumn: Fact_Returns.CustomerID
\ttoColumn: Dim_Customer.CustomerID
""",
        )
        result = validate_model_graph(parse_model(project))

        self.assertEqual(result["status"], "pass")

    def test_visual_binding_validator_finds_missing_column(self):
        project = self.make_project()
        visual = project / "Order2Cash.Report" / "definition" / "pages" / "ReportSection01" / "visuals" / "Visual0101" / "visual.json"
        payload = json.loads(visual.read_text(encoding="utf-8"))
        payload["visual"]["query"]["queryState"]["Values"]["projections"][0]["field"]["Column"]["Property"] = "MissingAmount"
        visual.write_text(json.dumps(payload), encoding="utf-8")

        result = validate_visual_bindings(project, parse_model(project))

        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("missing column" in error.lower() for error in result["errors"]))

    def test_native_source_validator_reports_connector_counts(self):
        result = validate_native_sources(parse_model(self.make_project()))

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["connectors"]["Excel.Workbook"], 1)
        self.assertEqual(result["connectors"]["Csv.Document"], 1)

    def test_acceptance_runner_combines_checks(self):
        result = run_acceptance(self.make_project())

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["summary"]["tables"], 2)
        self.assertEqual(result["summary"]["relationships"], 1)

    def test_feature_catalog_exposes_all_twenty_executable_features(self):
        catalog = load_feature_catalog()

        self.assertEqual(catalog["featureCount"], 20)
        self.assertEqual(len(catalog["features"]), 20)
        for feature in catalog["features"]:
            self.assertEqual(feature["implementationStatus"], "implemented_as_executable_contract")
            self.assertTrue(feature["inputs"])
            self.assertTrue(feature["outputs"])
            self.assertTrue(feature["cliCommands"])
            self.assertTrue(feature["acceptanceChecks"])

    def test_feature_delivery_plan_maps_all_features_to_process(self):
        result = build_feature_delivery_plan("lead-to-order")

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertEqual(result["featureCount"], 20)
        self.assertEqual(len(result["features"]), 20)
        self.assertTrue(all(feature["contractExists"] for feature in result["features"]))
        self.assertTrue(all(feature["validationContractExists"] for feature in result["features"]))

    def test_build_process_delivery_creates_local_bundle(self):
        out = Path(tempfile.mkdtemp()) / "lead-to-order"
        result = build_process_delivery("lead-to-order", "demo", out)

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertTrue((out / "source_profile.json").exists())
        self.assertTrue((out / "m_query_templates.json").exists())
        self.assertTrue((out / "demo-data" / "cases.csv").exists())
        self.assertTrue((out / "process-pack" / "model_spec.json").exists())

    def test_build_powerbi_report_package_creates_model_report_and_improvement_artifacts(self):
        out = Path(tempfile.mkdtemp()) / "lead-to-order-report"
        result = build_powerbi_report_package(
            "lead-to-order",
            "Excel export and SAP CRM opportunity extract",
            out,
            "Process owner cockpit for conversion, aging, SLA breaches, and next actions",
        )

        self.assertEqual(result["eventType"], "powerbi_expert_factory_report_package")
        self.assertEqual(result["processId"], "lead2order")
        self.assertTrue(Path(result["pbip"]["projectPath"]).exists())
        self.assertTrue((out / "model_build_plan.json").exists())
        self.assertTrue((out / "dax_measure_plan.json").exists())
        self.assertTrue((out / "power_query_m_plan.json").exists())
        self.assertTrue((out / "report_pages_plan.json").exists())
        self.assertTrue((out / "model_improvement_plan.json").exists())
        self.assertTrue((out / "validation_plan.json").exists())
        self.assertIn("validate", " ".join(result["nextCommands"]))

    def test_premium_usp_catalog_exposes_all_twenty_five_contracts(self):
        catalog = load_premium_usp_catalog()

        self.assertEqual(catalog["capabilityCount"], 25)
        self.assertEqual(len(catalog["capabilities"]), 25)
        for capability in catalog["capabilities"]:
            self.assertEqual(capability["implementationStatus"], "implemented_as_premium_usp_contract")
            self.assertTrue(capability["inputs"])
            self.assertTrue(capability["outputs"])
            self.assertTrue(capability["acceptanceChecks"])

    def test_premium_usp_plan_maps_all_contracts_to_process(self):
        result = build_premium_usp_plan("lead-to-order")

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertEqual(result["premiumUspCount"], 25)
        self.assertEqual(len(result["premiumUsps"]), 25)

    def test_market_differentiator_usps_cover_all_thirty_capabilities(self):
        catalog = load_market_differentiator_usp_catalog()

        self.assertEqual(catalog["capabilityCount"], 30)
        self.assertEqual(len(catalog["capabilities"]), 30)
        for capability in catalog["capabilities"]:
            self.assertEqual(capability["implementationStatus"], "implemented_as_market_differentiator_evidence")
            self.assertTrue(capability["primaryPersona"])
            self.assertTrue(capability["marketDifferentiator"])
            self.assertTrue(capability["proofArtifacts"])
            self.assertTrue(capability["acceptanceChecks"])

    def test_market_differentiator_usp_plan_maps_to_process(self):
        result = build_market_differentiator_usp_plan("lead-to-order")

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertEqual(result["capabilityCount"], 30)
        self.assertEqual(len(result["marketDifferentiatorUsps"]), 30)
        self.assertTrue(all(usp["artifactExists"] for usp in result["marketDifferentiatorUsps"]))

    def test_runtime_max_catalog_exposes_max_usp_replacement_capabilities(self):
        catalog = load_runtime_max_catalog()

        self.assertEqual(catalog["capabilityCount"], 70)
        self.assertEqual(len(catalog["capabilities"]), 70)
        for item in catalog["capabilities"]:
            self.assertEqual(item["implementationStatus"], "implemented_as_runtime_max_usp_artifact")
            self.assertIn(item["replacementRole"], {"Data Analyst", "Power BI Expert", "Power BI Developer"})
            self.assertTrue(item["replacementOutcome"])
            self.assertTrue(item["autonomyLevel"])
            self.assertTrue(item["deliverables"])
            self.assertTrue(item["acceptanceChecks"])

    def test_runtime_max_plan_points_to_generated_pbip_and_all_max_usps(self):
        result = build_runtime_max_plan("lead-to-order")

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertEqual(result["capabilityCount"], 70)
        self.assertEqual(len(result["runtimeMaxUsps"]), 70)
        self.assertTrue(all(usp["artifactExists"] for usp in result["runtimeMaxUsps"]))
        self.assertTrue(any(usp["replacementRole"] == "Data Analyst" for usp in result["runtimeMaxUsps"]))
        self.assertTrue(any(usp["replacementRole"] == "Power BI Expert" for usp in result["runtimeMaxUsps"]))
        self.assertTrue(any(usp["replacementRole"] == "Power BI Developer" for usp in result["runtimeMaxUsps"]))
        capability_ids = {usp["capabilityId"] for usp in result["runtimeMaxUsps"]}
        self.assertIn("legacy_report_reverse_engineer", capability_ids)
        self.assertIn("dashboard_consolidation_autopilot", capability_ids)
        self.assertIn("autonomous_bi_sprint_manager", capability_ids)
        self.assertIn("pbix_binary_intake", capability_ids)
        self.assertIn("live_tenant_scanner", capability_ids)
        self.assertIn("dax_query_runner", capability_ids)
        self.assertIn("powerbi_rest_deployer", capability_ids)
        self.assertIn("multi_tenant_msp_mode", capability_ids)
        self.assertTrue(Path(result["pbip"]["projectPath"]).exists())

    def test_pbix_binary_intake_extracts_safe_metadata_without_payload_secrets(self):
        pbix = Path(tempfile.mkdtemp()) / "sample.pbix"
        with ZipFile(pbix, "w") as archive:
            archive.writestr("Report/Layout", "{}")
            archive.writestr("DataModelSchema", '{"model": {"tables": []}}')
            archive.writestr("SecurityBindings", "secret-token")

        result = run_pbix_binary_intake(pbix)

        self.assertEqual(result["status"], "parsed")
        self.assertEqual(result["file"]["extension"], ".pbix")
        self.assertEqual(result["package"]["entryCount"], 3)
        self.assertIn("Report/Layout", result["package"]["entries"])
        self.assertTrue(result["classification"]["hasReportLayout"])
        self.assertTrue(result["classification"]["hasDataModelSchema"])
        self.assertNotIn("secret-token", json.dumps(result))

    def test_runtime_executor_requests_are_credential_safe(self):
        tenant = build_tenant_scan_request("tenant-01", ["workspace-01"])
        dax = build_dax_query_run_request("workspace-01", "dataset-01", "EVALUATE ROW(\"Cases\", [Case Count])")
        deploy = build_powerbi_rest_deployment_request(
            "workspace-01",
            "outputs/powerbi-runtime-max-layer/processes/lead2order/pbip/Lead2Order",
            ["import", "refresh"],
        )
        gateway = build_gateway_audit_request("gateway-cluster-01", ["datasource-01"])

        for payload in [tenant, dax, deploy, gateway]:
            self.assertEqual(payload["credentialPolicy"], "external_runtime_only")
            self.assertTrue(payload["operations"])
            self.assertTrue(payload["evidence"])
            self.assertNotIn("password", json.dumps(payload).lower())
            self.assertNotIn("token", json.dumps(payload).lower())

        self.assertEqual(tenant["executor"], "live_tenant_scanner")
        self.assertEqual(dax["executor"], "dax_query_runner")
        self.assertEqual(deploy["executor"], "powerbi_rest_deployer")
        self.assertEqual(gateway["executor"], "gateway_configuration_auditor")

    def test_runtime_executors_dry_run_without_access_token(self):
        with patch.dict(os.environ, {}, clear=True):
            tenant = run_tenant_scan_executor("tenant-01", ["workspace-01"])
            dax = run_dax_query_executor("workspace-01", "dataset-01", "EVALUATE ROW(\"Cases\", [Case Count])")
            gateway = run_gateway_audit_executor("gateway-01", ["datasource-01"])
            rest = run_powerbi_rest_executor(
                "workspace-01",
                "outputs/powerbi-runtime-max-layer/processes/lead2order/pbip/Lead2Order",
                ["import", "refresh"],
            )

        for payload in [tenant, dax, gateway, rest]:
            self.assertEqual(payload["status"], "dry_run")
            self.assertEqual(payload["credentialPolicy"], "external_runtime_only")
            self.assertTrue(payload["plannedRequests"])
            self.assertNotIn("secret-access-token", json.dumps(payload).lower())

    def test_runtime_executor_uses_injected_transport_with_access_token(self):
        calls = []

        def transport(method, url, headers=None, payload=None):
            calls.append({"method": method, "url": url, "headers": headers, "payload": payload})
            return {"ok": True, "value": [{"id": "workspace-01"}]}

        with patch.dict(os.environ, {"POWERBI_ACCESS_TOKEN": "secret-access-token"}, clear=True):
            result = run_tenant_scan_executor("tenant-01", ["workspace-01"], transport=transport)

        self.assertEqual(result["status"], "executed")
        self.assertTrue(calls)
        self.assertIn("Authorization", calls[0]["headers"])
        self.assertNotIn("secret-access-token", json.dumps(result))

    def test_generalist_autopilot_run_creates_business_manifest_and_report_package(self):
        out = Path(tempfile.mkdtemp()) / "autopilot"
        result = build_generalist_autopilot_run(
            "lead-to-order",
            "Excel export and SAP CRM opportunity extract",
            "Process owner wants conversion, aging, SLA breach, and action visibility",
            out,
        )

        self.assertEqual(result["eventType"], "powerbi_generalist_autopilot_run")
        self.assertEqual(result["processId"], "lead2order")
        self.assertTrue((out / "generalist_autopilot_manifest.json").exists())
        self.assertTrue((out / "report-package" / "report_package_manifest.json").exists())
        self.assertTrue((out / "runtime_max_plan.json").exists())
        self.assertTrue(result["businessSummary"])

    def test_generalist_prompt_run_interprets_human_o2c_request(self):
        out = Path(tempfile.mkdtemp()) / "human-prompt"
        prompt = (
            "Wir haben im O2C dauernd Stress. Aufträge hängen, Lieferungen kommen zu spät, "
            "Finance sagt Cash kommt nicht rein, Vertrieb beschwert sich über blockierte Rechnungen, "
            "und keiner weiß, ob das an Kunden, Material, Lager, Preisen oder Datenqualität liegt. "
            "Bau mir bitte ein Power BI Cockpit, mit dem ein Prozessverantwortlicher jeden Montag sieht, "
            "wo es brennt, wer handeln muss und welche Fälle zuerst dran sind. Quellen sind SAP Export, "
            "ein Excel mit Reklamationen/Disputes und irgendein CSV aus dem Lager."
        )

        result = build_generalist_prompt_run(prompt, out)

        self.assertEqual(result["eventType"], "powerbi_generalist_prompt_run")
        self.assertEqual(result["interpretedRequest"]["processId"], "order2cash")
        self.assertIn("SAP", result["interpretedRequest"]["sourceDescription"])
        self.assertIn("Monday", result["interpretedRequest"]["businessGoal"])
        self.assertTrue((out / "interpreted_request.json").exists())
        self.assertTrue((out / "autopilot" / "generalist_autopilot_manifest.json").exists())

    def test_production_hardening_catalog_exposes_all_fifteen_capabilities(self):
        catalog = load_production_hardening_catalog()

        self.assertEqual(catalog["capabilityCount"], 15)
        self.assertEqual(len(catalog["capabilities"]), 15)
        self.assertTrue(
            all(
                item["implementationStatus"] == "implemented_as_production_hardening_artifact"
                for item in catalog["capabilities"]
            )
        )

    def test_production_hardening_plan_returns_release_dashboard(self):
        result = build_production_hardening_plan("lead-to-order")

        self.assertEqual(result["requestedProcessId"], "lead-to-order")
        self.assertEqual(result["processId"], "lead2order")
        self.assertEqual(result["capabilityCount"], 15)
        self.assertEqual(result["releaseDecision"], "ready_for_desktop_smoke")

    def test_lead2order_powerbi_analysis_package_validates_cleanly(self):
        package_root = Path("outputs/lead2order-powerbi-analysis")
        manifest = json.loads((package_root / "lead2order_powerbi_manifest.json").read_text(encoding="utf-8"))
        measures = json.loads((package_root / "measure_catalog.json").read_text(encoding="utf-8"))
        questions = json.loads((package_root / "kpi_problem_questions.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["processId"], "lead2order")
        self.assertEqual(manifest["measureCount"], 30)
        self.assertEqual(manifest["problemQuestionCount"], 10)
        self.assertEqual(len(measures["measures"]), 30)
        self.assertEqual(len(questions["problemQuestions"]), 10)

        result = run_acceptance(package_root / "pbip" / "Lead2OrderAnalysis")
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["summary"]["errors"], 0)
        self.assertEqual(result["summary"]["warnings"], 0)


if __name__ == "__main__":
    unittest.main()
