// Generic Power Query starter snippets. Replace parameters and source names before use.

// SQL Server import pattern
let
    Source = Sql.Database(ServerName, DatabaseName),
    Entity = Source{[Schema = SchemaName, Item = TableName]}[Data]
in
    Entity

// OData pattern
let
    Source = OData.Feed(ODataUrl, null, [Implementation = "2.0"]),
    Entity = Source{[Name = EntityName, Signature = "table"]}[Data]
in
    Entity

// REST JSON pattern
let
    Response = Json.Document(Web.Contents(ApiBaseUrl, [RelativePath = ApiPath])),
    Rows = if Response is list then Response else Response[data],
    Table = Table.FromRecords(Rows)
in
    Table

// Folder combine pattern
let
    Source = Folder.Files(FolderPath),
    Filtered = Table.SelectRows(Source, each [Extension] = ".csv")
in
    Filtered

