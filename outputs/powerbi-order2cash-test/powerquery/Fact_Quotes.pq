// Power Query M - import Fact_Quotes from the industrial demo workbook.
let
    Source = Excel.Workbook(File.Contents("C:/tmp/PowerBi-Codex-Plugin/outputs/powerbi-industrial-demo/powerbi_industrial_demo_data.xlsx"), null, true),
    Raw = Source{[Item="Fact_Quotes", Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(Raw, [PromoteAllScalars = true])
in
    PromotedHeaders
