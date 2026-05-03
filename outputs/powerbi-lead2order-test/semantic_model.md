# Lead2Order Semantic Model

## en-US

## Grain

- `Fact_Leads`: one row per lead.
- `Fact_LeadStageHistory`: one row per lead stage event.
- `Fact_Opportunities`: one row per opportunity.
- `Fact_Quotes`: one row per quote version or quote header, depending on source availability.
- `Fact_Orders`: one row per booked order header or line, depending on order-value grain.
- `Fact_Lead2OrderExceptions`: one row per actionable process exception.

## Dimensions

- `Dim_Account`: account/customer/prospect.
- `Dim_Contact`: contact and buying center attributes.
- `Dim_Product`: product, product group, solution family.
- `Dim_Channel`: inbound/outbound, partner, web, event, referral, paid campaign.
- `Dim_Campaign`: campaign and spend attributes.
- `Dim_SalesOwner`: SDR, account executive, sales team, manager.
- `Dim_Region`: country, region, territory.
- `Dim_Calendar`: created, qualified, quote, order, and close dates.
- `Dim_LostReason`: normalized lost/disqualified reason.

## Relationship Rules

- Use a star schema: facts connect to dimensions, not to other facts.
- Use bridge keys only when CRM and ERP identifiers differ.
- Keep role-playing date relationships explicit and activate secondary dates through dedicated measures.
- Avoid bidirectional filtering unless a bridge table is deliberately designed and tested.

## de-DE

## Granularitaet

- `Fact_Leads`: eine Zeile je Lead.
- `Fact_LeadStageHistory`: eine Zeile je Lead-Stage-Event.
- `Fact_Opportunities`: eine Zeile je Opportunity.
- `Fact_Quotes`: eine Zeile je Angebotsversion oder Angebotskopf, abhaengig von der Quelle.
- `Fact_Orders`: eine Zeile je gebuchtem Auftragskopf oder Auftragsposition, abhaengig vom Wert-Grain.
- `Fact_Lead2OrderExceptions`: eine Zeile je steuerbarer Prozess-Exception.

## Dimensionen

- `Dim_Account`: Account/Kunde/Prospect.
- `Dim_Contact`: Kontakt und Buying-Center-Attribute.
- `Dim_Product`: Produkt, Produktgruppe, Solution Family.
- `Dim_Channel`: inbound/outbound, Partner, Web, Event, Referral, Paid Campaign.
- `Dim_Campaign`: Kampagne und Spend-Attribute.
- `Dim_SalesOwner`: SDR, Account Executive, Sales Team, Manager.
- `Dim_Region`: Land, Region, Territory.
- `Dim_Calendar`: Created, Qualified, Quote, Order und Close Dates.
- `Dim_LostReason`: normalisierte Lost-/Disqualified-Gruende.

## Beziehungsregeln

- Sternschema verwenden: Facts verbinden sich mit Dimensionen, nicht mit anderen Facts.
- Bridge Keys nur verwenden, wenn CRM- und ERP-Identifier abweichen.
- Role-playing Date Relationships explizit halten und Sekundaerdaten ueber dedizierte Measures aktivieren.
- Bidirektionale Filter vermeiden, ausser eine Bridge Table ist bewusst modelliert und getestet.

