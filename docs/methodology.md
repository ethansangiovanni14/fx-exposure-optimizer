# Methodology and assumptions

## Fictional case
The subject is a fictional US electronics distributor. Supplier names, transactions, invoice dates, amounts, payment terms and quarterly budget rates are **synthetically generated**. No observed private business transactions are implied.

## Modeling cutoff
2026-09-30. Jan 2025–Sep 2026 invoices are labeled historical; Oct–Dec 2026 are planned. The label describes the illustrative planning period, not whether an invoice was actually settled. `Due_Date` may extend beyond December 2026.

## Generation and validation
- 1,500 records, 18 suppliers, EUR/GBP/JPY, source invoices between Jan 2025 and Dec 2026.
- Supplier-specific transaction ranges and relative sampling frequencies; generated from a fixed pseudorandom seed (`scripts/generate_data.py`).
- Purchase dates drawn within each selected month; terms based on supplier reference data.
- `budget_rates_synthetic.csv` contains planning assumptions in **USD per local-currency unit** and must not be described as actual historical exchange rates.
- Some raw records have inconsistent formatting or incomplete fields. These are deliberate test cases for repeatable cleaning.

## Intentionally introduced issues (known to data generator)
- 15 records with supplier-name case/whitespace variants
- 15 with missing department (may be recoverable from supplier master)
- 15 with invoice dates in M/D/YYYY rather than ISO format
- 15 with thousands separators in local-currency invoice amounts
- 15 with colliding invoice IDs (must be investigated, **not** blindly deleted)
- 15 with alternate category naming
- 15 with missing payment due dates (may be reconstructed from supplier terms, but document assumptions)

There are 105 distinct affected source records (7%). The analyst should independently profile the data, document decisions, and preserve raw records. Do not assume all ID collisions identify true duplicate transactions.

## Intended Excel methodology (not yet implemented)
1. Import raw invoices and supplier master to Power Query.
2. Audit duplicate identifiers, missing essential fields, date formats, and amount types.
3. Standardize fields and record any reconstruction or exclusions without overwriting raw source files.
4. Query ECB daily EUR-based reference FX data from the documented endpoint.
5. For each historical invoice, match the relevant published rate on invoice date or the most recent preceding business day. This **models reference-rate exposure**, not bank settlement amounts.
6. For planning invoices, use a clearly labeled last available reference-rate baseline plus scenario assumptions. Do not use future ECB observations when reproducing the Sep-30 planning-cutoff scenario; users refreshing later must explicitly freeze a cutoff or relabel their analysis as of refresh date.
7. Convert rates into USD per local-currency unit (USD/EUR = ECB USD; USD/GBP = ECB USD / ECB GBP; USD/JPY = ECB USD / ECB JPY).
8. Compare modeled USD amount with synthetic quarterly budget USD rate, and summarize by supplier, currency, and department.
9. Independently validate a sample of FX conversions and budget variances.

## Constraints and limitations
- Synthetic invoice behavior reflects design assumptions, not an external sample of purchasing behavior.
- ECB reference FX quotations are not guaranteed executable settlement rates.
- Invoice issue date is not necessarily payment date; the project must distinguish exposure measurement dates from realized payment costs.
- Scenario outcomes are conditional estimates, **not forecasts** or promised savings.
- No claims of actual corporate savings should be made.
