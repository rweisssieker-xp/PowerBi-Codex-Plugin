# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Reporting Security Issues

Do not open public issues for vulnerabilities, exposed secrets, tenant identifiers, gateway details, customer data, or confidential Power BI artifacts. Contact the repository maintainers privately.

## Data Handling

Do not commit:

- Power BI tenant secrets.
- Gateway credentials.
- OAuth tokens.
- API keys.
- Customer data extracts.
- PBIX/PBIP artifacts with confidential production data.
- Screenshots containing sensitive business data.

## AI Output Safety

AI-generated Power BI guidance must be validated before operational use. Validate source metadata, KPI definitions, access rules, reconciliation totals, data privacy constraints, DAX behavior, Power Query refresh behavior, and model relationships before release.
