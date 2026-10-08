# International Supplier Payment & Currency Exposure Optimizer

An Excel-based financial and operations analysis project that models how foreign-exchange movements affect a fictional US electronics distributor purchasing from international suppliers.

The project combines **synthetic supplier invoice data** with **real European Central Bank (ECB) reference exchange rates** to monitor currency exposure, compare modeled USD purchasing costs against budget, and test FX scenarios for planned payments.

## Business problem

A US-based company purchases components, equipment, software, and services from suppliers in Europe, the United Kingdom, and Japan. Because invoices are denominated in EUR, GBP, and JPY, exchange-rate movements can change the USD cost of those purchases and create budget uncertainty.

**Guiding question:**  
How can a US-based company monitor foreign-exchange exposure, identify purchasing costs that exceed budget, and evaluate the potential impact of currency movements on planned supplier payments?

## Project objectives

1. **Monitor FX exposure** by currency, supplier, department, and quarter.
2. **Measure budget variance** by comparing modeled USD invoice cost with synthetic budget FX assumptions.
3. **Evaluate scenarios** showing how user-defined exchange-rate movements could affect planned purchasing costs.

## Tools

- **Microsoft Excel** — PivotTables/PivotCharts, XLOOKUP, SUMIFS, scenario modeling, conditional formatting, executive dashboard design
- **Power Query** — data cleaning, supplier-reference joins, ECB API integration, calendar/rate matching, budget-rate joins
- **ECB Data API** — real daily reference FX data for EUR, GBP, and JPY
- **Python** — used only to reproducibly generate the fictional source data; the analysis itself is built in Excel/Power Query

## Data

The business transactions are fictional and were created specifically for this portfolio project.

- **1,500 synthetic supplier invoices**
- **18 fictional international suppliers**
- **January 2025–December 2026**
- **Currencies:** EUR, GBP, JPY
- **Historical / planned cutoff:** September 30, 2026
- Synthetic quarterly budget FX assumptions
- Real ECB daily reference exchange rates

### Source files

- `data/supplier_invoices_raw.csv` — synthetic supplier invoice records
- `data/suppliers.csv` — supplier master/reference data
- `data/budget_rates_synthetic.csv` — fictional quarterly budget FX assumptions
- ECB EXR API — real daily exchange-rate reference data

ECB endpoint used:

```text
https://data-api.ecb.europa.eu/service/data/EXR/D.USD+GBP+JPY.EUR.SP00.A?startPeriod=2025-01-01&format=csvdata
```

## Data preparation

The raw invoice data intentionally includes realistic data-quality issues so the workbook demonstrates a complete cleaning workflow.

Power Query was used to:

- Trim and clean supplier-name formatting.
- Use `Supplier_ID` as the source of truth and merge official supplier names from the supplier master.
- Investigate repeated invoice IDs rather than automatically deleting them.
- Create a composite `Transaction_Key` using supplier ID and invoice ID; validation found no duplicate transaction keys.
- Recover missing department values from each supplier's default department.
- Reconstruct missing due dates using invoice date plus supplier payment terms.
- Standardize inconsistent category labels.
- Validate currency, amount, record-status, and date fields.

## FX integration and calculation logic

ECB rates are published relative to EUR, so the workbook calculates USD-per-unit cross rates:

- **EUR → USD:** ECB USD per EUR
- **GBP → USD:** USD per EUR ÷ GBP per EUR
- **JPY → USD:** USD per EUR ÷ JPY per EUR

A daily calendar is merged with ECB data and the most recent available reference rate is carried forward for weekends and holidays.

```text
Modeled Invoice Amount (USD)
= Local-Currency Invoice Amount × FX Rate to USD
```

Budget rates are joined using both **quarter and currency**:

```text
Budgeted Invoice Amount (USD)
= Local-Currency Invoice Amount × Budget USD per Unit
```

```text
FX Budget Variance
= Modeled USD Cost - Budgeted USD Cost
```

- Positive variance = **unfavorable / over budget**
- Negative variance = **favorable / under budget**

## Executive dashboard

The finished workbook includes an executive dashboard with:

- Total modeled USD spend
- Total budgeted spend
- Total FX budget variance
- FX variance percentage
- Actual vs. budgeted spend by currency
- Quarterly FX budget variance
- Top five suppliers by modeled USD spend
- Key analytical takeaways

### Portfolio results

Across the synthetic invoice portfolio:

- **Modeled USD spend:** **$31.03M**
- **Budgeted USD spend:** **$30.32M**
- **Net unfavorable FX variance:** **+$713.13K**
- **Overall variance:** approximately **+2.35%**

| Currency | Modeled USD Spend | FX Budget Variance |
|---|---:|---:|
| EUR | $17.09M | +$832.38K |
| GBP | $5.19M | +$208.25K |
| JPY | $8.75M | -$327.49K |

Additional observations:

- **EUR** represents the largest currency exposure and the largest unfavorable variance.
- Favorable **JPY** variance partially offsets unfavorable EUR and GBP variance.
- **2026-Q1** has the largest unfavorable quarterly variance at approximately **+$221.94K**.
- **2026-Q4** is favorable overall at approximately **-$87.45K**.
- **Manufacturing** accounts for approximately **87.6%** of modeled international spend.
- **Alpen Precision Systems** is the largest individual supplier exposure at approximately **$4.89M**.

## Scenario analysis

The workbook includes an interactive scenario model for **planned supplier payments only**. Users can change highlighted assumptions for EUR, GBP, and JPY and immediately see baseline planned spend, scenario planned spend, scenario cost impact, overall impact percentage, and cost impact by currency.

The default illustrative stress case applies a **+5% change** to all three foreign currencies:

| Metric | Default Scenario |
|---|---:|
| Baseline planned spend | $3.82M |
| Scenario planned spend | $4.02M |
| Scenario cost impact | +$191.24K |
| Impact | +5.00% |

Positive scenario impact represents a higher modeled USD cost; negative impact represents a lower modeled USD cost.

**The scenario model is sensitivity analysis, not an FX forecast.** It illustrates potential cost outcomes under user-defined exchange-rate assumptions.

## Workbook structure

- **Dashboard** — executive summary and charts
- **Scenario Analysis** — interactive FX sensitivity model
- **Analysis** — PivotTable-based analysis by currency, supplier, quarter, and department
- **Invoices_Clean** — cleaned invoice-level dataset
- **Calendar** — daily FX calendar used for reference-rate matching
- **ECB_FX_Rates** — transformed ECB reference-rate data
- **suppliers** — supplier reference table
- **budget_rates_synthetic** — synthetic quarterly budget assumptions

Validation and investigation sheets are retained in the workbook but hidden from the final presentation view.

## Reproducing the synthetic source data

To regenerate the same fictional CSV files using the fixed random seed:

```bash
python scripts/generate_data.py
```

Python is used only for creating the reproducible synthetic source files. The financial analysis, transformations, dashboard, and scenario model are built in Excel and Power Query.

## Validation

The model was checked through:

- Transaction-key duplicate validation
- Row-count checks after joins
- Manual EUR, GBP, and JPY conversion checks
- Budget-variance spot checks
- PivotTable total reconciliation
- Scenario-model sensitivity testing

## Limitations

- All supplier transactions and budget assumptions are synthetic.
- ECB reference rates are not guaranteed transaction execution rates.
- The model does not include bank spreads, hedging costs, transaction fees, or other settlement costs.
- Invoice date is used as the exposure measurement date for historical modeling; it may differ from actual payment date.
- Scenario outputs are conditional estimates, not exchange-rate forecasts or guaranteed savings.
- Results should not be interpreted as the performance of a real company.

## Documentation

See [`docs/methodology.md`](docs/methodology.md) for additional assumptions, synthetic-data design, and validation details.
