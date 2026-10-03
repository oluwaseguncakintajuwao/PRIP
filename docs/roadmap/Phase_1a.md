# Phase 1a — Portfolio Data Foundation

*Portfolio Risk Intelligence Platform (PRIP)*

## Summary

Phase 1a built the pipeline that takes PRIP's 10-ETF universe from the Tiingo API to a validated price history, daily returns, and a buy-and-hold portfolio.

The analysis covers **2015-01-02 to 2026-10-02**, with **2,955 trading-day observations for each of the 10 ETFs** (**29,550 price records** in total).

The portfolio started with **$100,000**, split equally at **$10,000 per ETF**. By 2026-10-02, it was worth **$282,879.59**, a **cumulative return of 182.88% based on Tiingo adjusted-close data, which incorporates dividend and split adjustments.**

This is cumulative return over 11.75 years, not an annualized figure. Annualized return and risk measures are calculated in Phase 1b.

---

## Scope

Phase 1a covered:

- validation of the ETF universe and target weights;
- historical daily data extraction from the Tiingo API;
- preservation of raw source data for each extraction run, with run metadata;
- cleaning and validation of the adjusted price series;
- daily ETF returns from adjusted close; and
- construction of an initially equal-weight portfolio, with daily value and cumulative return.

Later phases cover the remaining work:

| Topic | Phase |
|---|---|
| Annualized return, volatility, drawdown, Sharpe, Sortino, correlation, risk contribution | 1b |
| ETF costs, tracking difference/error, liquidity, structure, portfolio fit | 1c |
| Weight drift and rebalancing trades | 1d |
| Holdings overlap and hidden concentration | 1e |
| Power BI reporting | 1f |
| Premium/discount monitoring | 2 |
| ETF market mechanics | 3 |

---

## Portfolio Construction

| Assumption | Phase 1a Treatment |
|---|---|
| Inception date | 2015-01-02, using Tiingo adjusted close |
| Initial portfolio value | $100,000 |
| Initial allocation | 10% ($10,000) in each of 10 ETFs |
| Methodology | Buy-and-hold; no rebalancing |
| Return input | Tiingo adjusted close (adjusted for splits and dividends) |
| Expense ratios | Reflected in ETF prices |
| Transaction costs | Not modeled |
| Taxes | Not modeled |
| Fractional shares | Permitted |
| Cash | None; fully invested |

The portfolio is **initially** equal-weighted, not continuously equal-weighted. After inception, each position grows or declines with its own price, so weights drift over time. Measuring that drift and the trades needed to correct it is the subject of Phase 1d.

---

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Start date | 2015-01-02 | Gives more than 10 years of common history for all 10 ETFs, including the 2018 Q4 selloff, the 2020 COVID crash, and the 2022 rate shock. |
| Data provider | Tiingo | Documented API that returns both raw and adjusted price fields. |
| Return price field | Adjusted close | Accounts for splits and distributions, so the return series incorporates dividend and split adjustments and is used as the project's total-return series. This matters most for the bond and REIT ETFs, where income is a large share of return. |
| Initial weighting | 10% per ETF | A transparent baseline before any strategic weighting or optimization. |
| Rebalancing | None | Keeps an untouched baseline against which rebalancing rules can later be compared. |
| Raw data | Saved per extraction run, never overwritten | Any processed file can be regenerated from a specific raw pull. |
| Processed data | Generated only by code | No manual edits to analytical datasets. |

---

## Data Pipeline

**ETF Universe → Tiingo API → Raw Data → Validation & Cleaning → Adjusted Prices → Daily ETF Returns → Buy-and-Hold Portfolio**

Each extraction is stored in its own directory under `data/raw/tiingo/` and writes a metadata record to `data/processed/run_metadata/`. The record holds the run identifier, requested period, source, tickers requested, successful and failed downloads, row count, and the location of the raw data.

---

## Validation Results

| Check | Expected | Result | Status |
|---|---|---:|---|
| ETFs in universe | 10 | 10 | Pass |
| Sum of target weights | 100% | 100% | Pass |
| Observations per ETF | Equal across ETFs | 2,955 each | Pass |
| Date range per ETF | Identical across ETFs | 2015-01-02 to 2026-10-02 for all | Pass |
| Duplicate ticker-date records | 0 | 0 | Pass |
| Missing adjusted-close values | 0 | 0 | Pass |
| Missing daily-return values | 10 (one per ETF) | 10 | Pass |
| Portfolio observations | 2,955 | 2,955 | Pass |
| Duplicate portfolio dates | 0 | 0 | Pass |
| Missing portfolio values | 0 | 0 | Pass |
| Initial portfolio value | $100,000.00 | $100,000.00 | Pass |
| Initial cumulative return | 0.00% | 0.00% | Pass |

The 10 missing daily returns are the first observation for each ETF, which has no prior price to calculate a return from.

**Cleaning:** No duplicate ticker-date records or missing adjusted-close values remained in the final processed dataset. The validation process also confirmed consistent date coverage and observation counts across all 10 ETFs.

**End-of-period data:** The final extraction was performed after the regular U.S. market close on 2026-10-02. The latest available observation across all 10 ETFs was therefore 2026-10-02.

---

## Internal Consistency Check

Cumulative return was recomputed from the stored portfolio values (value ÷ $100,000 − 1) and compared with the stored cumulative-return column. The maximum absolute difference was **1.11 × 10⁻¹⁵**, which is floating-point rounding.

This confirms that the two output columns agree. It does not independently verify the portfolio construction itself.

---

## Key Outputs

| Output | Contents |
|---|---|
| `data/raw/tiingo/` | Original Tiingo data, one directory per extraction run |
| `data/processed/run_metadata/` | One audit record per extraction run |
| `data/processed/etf_prices_long.csv` | Validated price history with raw and adjusted Tiingo fields |
| `outputs/daily_returns.csv` | Daily ETF returns from adjusted close |
| `outputs/equal_weight_portfolio_growth.csv` | Daily portfolio value, daily return, and cumulative return |

---

## Limitations

| Limitation | Where it is addressed |
|---|---|
| Returns are not yet risk-adjusted | Phase 1b |
| Transaction costs are not modeled | Phase 1c covers ETF trading costs and liquidity |
| Weights are never rebalanced | Phase 1d |
| Results reflect a single inception date and a single historical path | Not addressed; applies to all results |
| The universe was chosen in 2026, so every ETF is one that survived and remains widely held | Not addressed; applies to all results |
| Taxes are not modeled | Outside project scope |

---

## Next Phase

The portfolio nearly tripled over 11.75 years. **Phase 1b — Portfolio Performance and Risk Analytics** asks what risk it took to get there: how volatile the path was, how deep the drawdowns ran, and which ETFs contributed most of the risk.

*Status: Complete*