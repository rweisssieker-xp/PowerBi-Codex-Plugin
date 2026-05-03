# Order2Cash Semantic Model Relationships

## Dimensions

- `Dim_Calendar[Date]` to role-playing dates in orders, quotes, deliveries, billings, AR, service tickets, and shipments.
- `Dim_Customer[CustomerID]` -> facts with `CustomerID`.
- `Dim_Product[ProductID]` -> sales orders, deliveries, service tickets.
- `Dim_Plant[PlantID]` -> sales orders.
- `Dim_Warehouse[WarehouseID]` -> deliveries.

## Fact Flow

- `Fact_Leads[LeadID]` -> `Fact_Opportunities[LeadID]`
- `Fact_Opportunities[OpportunityID]` -> `Fact_Quotes[OpportunityID]`
- `Fact_Quotes[QuoteID]` -> `Fact_SalesOrders[QuoteID]`
- `Fact_SalesOrders[SalesOrderID]` -> `Fact_Deliveries[SalesOrderID]`
- `Fact_Deliveries[DeliveryID]` -> `Fact_Billing[DeliveryID]`
- `Fact_Billing[InvoiceID]` -> `Fact_AR[InvoiceID]`
- `Fact_Deliveries[DeliveryID]` -> `Fact_Shipments[DeliveryID]`
- `Fact_Order2CashExceptions[CustomerID]` -> `Dim_Customer[CustomerID]`
- `Fact_Order2CashExceptions[ProductID]` -> `Dim_Product[ProductID]` where populated

## Notes

- Keep the main customer/product/date dimensions as one-to-many relationships.
- Keep fact-to-fact relationships inactive or use bridge/detail pages if Power BI creates ambiguity.
- Prefer a process-event table later if true process mining is needed.
