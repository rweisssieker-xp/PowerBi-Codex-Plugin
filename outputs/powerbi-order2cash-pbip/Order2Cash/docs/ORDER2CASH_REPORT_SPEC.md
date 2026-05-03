# Order2Cash Power BI Report Spec

## Source

`C:\tmp\PowerBi-Codex-Plugin\outputs\powerbi-industrial-demo\powerbi_industrial_demo_data.xlsx`

## Business Goal

Show all major Order2Cash problems in one Power BI cockpit: customer churn risk, ATP shortages, backlog, late/short delivery, billing blocks, open receivables, disputes, discount leakage, and service/SLA risks.

## Pages

1. **O2C Executive Overview**: KPI cards, process health score, top 10 exceptions, financial exposure.
2. **Customer Churn and Retention Risk**: churn-risk score, no-order aging, disputes, delivery failures, service issues.
3. **Order Intake and Backlog**: order value, open backlog, ATP status, requested vs confirmed dates.
4. **Delivery and OTIF**: late/short delivery rate, carrier performance, warehouse and plant root causes.
5. **Billing and Cash**: billing blocks, invoice amount, open AR, dunning level, disputes.
6. **Quote and Margin Leakage**: discount leakage, approval cycle days, legal loops, quote conversion.
7. **Exception Action Backlog**: customer, owner, problem type, estimated exposure, recommended action.

## Demo KPIs From Current Workbook

| KPI | Value |
| --- | --- |
| Sales order count | 260 |
| Order value | 37.705.914 EUR |
| Open backlog value | 23.188.023 EUR |
| ATP issue rate | 75.0% |
| Late or short delivery rate | 96.8% |
| Billing block rate | 7.3% |
| Open AR amount | 3.951.156 EUR |
| Dispute rate | 7.3% |
| Estimated discount leakage | 2.878.713 EUR |
| High churn-risk customers | 9 |
| O2C exception count | 526 |
| O2C exception exposure | 102.532.226 EUR |

## Top Churn-Risk Customers

| Customer | Segment | Revenue | Days Since Last Order | Late/Short Events | Disputes | Risk Score | Risk Band |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Apex Systems 27 | Distributor | 1.138.263 EUR | 280 | 5 | 0 | 74 | High |
| Vector Industries 31 | Strategic Account | 591.575 EUR | 140 | 7 | 1 | 70 | High |
| Orion Components 32 | Public Sector | 1.377.554 EUR | 82 | 10 | 3 | 65 | High |
| Vector Systems 2 | Public Sector | 505.943 EUR | 135 | 9 | 0 | 60 | High |
| Helio Mobility 29 | Aftermarket | 580.850 EUR | 184 | 4 | 0 | 55 | High |
| Vector Technologies 7 | Aftermarket | 0 EUR | 999 | 0 | 0 | 55 | High |
| Vector Mobility 30 | Strategic Account | 0 EUR | 999 | 0 | 0 | 55 | High |
| Helio Technologies 44 | OEM | 0 EUR | 999 | 0 | 0 | 55 | High |
| Atlas Mobility 47 | Strategic Account | 84.484 EUR | 221 | 1 | 0 | 54 | High |
| Prime Components 5 | Public Sector | 1.153.876 EUR | 32 | 15 | 1 | 49 | Medium |
| Global Technologies 57 | Distributor | 1.035.028 EUR | 108 | 13 | 1 | 49 | Medium |
| Apex Mobility 53 | Strategic Account | 714.678 EUR | 71 | 8 | 1 | 49 | Medium |
| Vector Technologies 11 | Public Sector | 463.450 EUR | 100 | 11 | 1 | 49 | Medium |
| Prime Systems 3 | Strategic Account | 0 EUR | 999 | 0 | 0 | 49 | Medium |
| Orion Mobility 16 | Strategic Account | 0 EUR | 999 | 0 | 0 | 49 | Medium |

## Top Products By Order Value

| Product | Product Family | Order Value |
| --- | --- | ---: |
| Hydraulic Pump Eco 103 | Hydraulic Pump | 3.187.045 EUR |
| Sensor Module Pro 101 | Sensor Module | 2.674.486 EUR |
| Control Cabinet Eco 104 | Control Cabinet | 2.239.059 EUR |
| Control Cabinet Eco 123 | Control Cabinet | 2.145.989 EUR |
| Hydraulic Pump Pro 127 | Hydraulic Pump | 1.994.936 EUR |
| Sensor Module Heavy Duty 111 | Sensor Module | 1.965.699 EUR |
| Valve Block Heavy Duty 135 | Valve Block | 1.773.413 EUR |
| Drive Unit Standard 102 | Drive Unit | 1.671.643 EUR |
| Drive Unit Heavy Duty 130 | Drive Unit | 1.660.007 EUR |
| Hydraulic Pump Eco 106 | Hydraulic Pump | 1.525.642 EUR |

## Top O2C Exceptions By Exposure

| Problem | Severity | Customer | Related Document | Exposure | Recommended Action |
| --- | --- | --- | --- | ---: | --- |
| Customer Churn Risk | Medium | Vector Mobility 17 | C0017 | 1.966.673 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Helio Systems 45 | C0045 | 1.854.257 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Apex Technologies 18 | C0018 | 1.676.872 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Global Mobility 56 | C0056 | 1.590.170 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Orion Mobility 58 | C0058 | 1.589.642 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | High | Orion Components 32 | C0032 | 1.377.554 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Global Systems 49 | C0049 | 1.352.493 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Orion Systems 12 | C0012 | 1.207.855 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Apex Systems 19 | C0019 | 1.185.579 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Prime Components 5 | C0005 | 1.153.876 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Apex Mobility 36 | C0036 | 1.143.988 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Atlas Technologies 46 | C0046 | 1.139.116 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | High | Apex Systems 27 | C0027 | 1.138.263 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Nova Technologies 10 | C0010 | 1.073.927 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
| Customer Churn Risk | Medium | Orion Components 59 | C0059 | 1.054.375 EUR | Account owner retention call, service recovery, delivery review, commercial offer validation |
