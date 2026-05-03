// Power Query M - import Fact_Order2CashExceptions exception table.
let
    Source = Csv.Document(File.Contents("C:/tmp/PowerBi-Codex-Plugin/outputs/powerbi-order2cash-test/data/Fact_Order2CashExceptions.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    PromotedHeaders
