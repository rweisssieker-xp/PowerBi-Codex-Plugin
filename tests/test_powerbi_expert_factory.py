import json
import tempfile
import unittest
from pathlib import Path

from scripts.powerbi_expert_factory import (
    parse_model,
    run_acceptance,
    validate_model_graph,
    validate_native_sources,
    validate_visual_bindings,
)


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


if __name__ == "__main__":
    unittest.main()
