# International Supplier Payment & Currency Exposure Optimizer

**Status:** In development — Phase 1 (data design). This is a fictional business case using synthetic invoices and actual ECB reference exchange rates (to be connected in Excel).

## Business problem
A fictional US electronics distributor purchases components, equipment, software, and services from European, UK, and Japanese suppliers. Foreign-currency payment obligations create uncertainty in USD-equivalent purchasing costs.

**Guiding question:** How can a US-based company monitor foreign exchange exposure, identify international purchasing costs that exceed budget, and evaluate scenarios for managing currency-related expenses?

## Decisions supported
1. **Exposure:** Which currencies and suppliers account for the largest outstanding foreign-currency payment obligations?
2. **Budget variance:** Which modeled payments exceed their budgeted USD cost, and by how much?
3. **Scenario planning:** How would adverse or favorable exchange-rate movements change estimated USD payment costs?

## Deliverable
A refreshable Excel workbook with Power Query transformations, an ECB exchange-rate API connection, invoice-level calculations, an interactive scenario model, and an executive dashboard.

## Data
- `data/supplier_invoices_raw.csv`: 1,500 synthetic invoice records, spanning January 2025–December 2026.
- `data/suppliers.csv`: 18 fictional suppliers and default attributes.
- `data/budget_rates_synthetic.csv`: fictional quarterly budget assumptions in USD per currency unit. **Not observed exchange rates.**
- Actual daily currency reference rates: ECB EXR API; will be retrieved into Excel using Power Query (not bundled as fabricated observations).

### Time framing
The analysis uses a **2026-09-30 planning cutoff**. Invoices dated through that day are labeled `Historical`; invoices dated October–December 2026 are labeled `Planned`. Historical invoice amounts are synthetic and do **not** establish actual paid USD amounts. Reference-rate calculations are approximations and do not include bank spreads or settlement fees.

### ECB API
Official series for USD, GBP, and JPY quoted per EUR:

`https://data-api.ecb.europa.eu/service/data/EXR/D.USD+GBP+JPY.EUR.SP00.A?startPeriod=2025-01-01&format=csvdata`

Because the fictional company reports in USD, cross rates must be calculated from the ECB series correctly (e.g. USD per GBP = USD per EUR / GBP per EUR). Reference rates are not guaranteed transaction execution rates.

## Reproduction (dataset only, so far)
Run `python scripts/generate_data.py` to regenerate identical synthetic CSV files using a fixed random seed. **Python is used only to construct the fictional source data, not for the Excel analysis.**

## Methodology
See [`docs/methodology.md`](docs/methodology.md) for business assumptions, synthetic data quality issues, future rate handling, and validation rules.

## Work in progress
- [x] Define business objectives and synthetic invoice schema
- [x] Generate initial invoice and supplier source data
- [ ] Inspect and clean data in Excel Power Query
- [ ] Integrate ECB exchange-rate API
- [ ] Validate invoice-level USD conversions and budget variances
- [ ] Build scenario model and executive dashboard
- [ ] Document findings and publish screenshots
