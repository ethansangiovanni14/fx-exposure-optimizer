# Data dictionary

## supplier_invoices_raw.csv
| Field | Description |
|---|---|
| Invoice_ID | Source transaction identifier; possible deliberate collisions |
| Supplier_ID | Foreign supplier key, joins to `suppliers.csv` |
| Supplier_Name | Raw supplier display name; some casing and whitespace variants |
| Department | Purchasing department; some blanks |
| Category | Type of purchase; some alternate labels |
| Invoice_Date | Issue date; mostly ISO YYYY-MM-DD, some M/D/YYYY |
| Due_Date | Contractual due date; some blanks |
| Currency | Invoice currency: EUR, GBP or JPY |
| Invoice_Amount_Local | Nominal local-currency amount; some thousands separators |
| Record_Status | `Historical` through 2026-09-30, `Planned` thereafter |

## suppliers.csv
Supplier_ID (key); Supplier_Name (canonical); Country; Currency; Category; Default_Department; Payment_Terms_Days; Typical_Invoice_Min; Typical_Invoice_Max; Relative_Frequency. Range and frequency fields are generation assumptions, not analytical findings.

## budget_rates_synthetic.csv
`Budget_Quarter` (YYYY-Q#); `Currency`; `Budget_USD_Per_Unit` — synthetic planning exchange rate. Join to invoice quarter and currency. These are **not actual ECB rates**.

## ECB rate series (to be imported, not yet included)
ECB daily `EXR` reference series for USD, GBP, JPY quoted per 1 EUR; the key fields for the analysis are observation date, currency, and observation value.
