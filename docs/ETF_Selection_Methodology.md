# ETF Selection Methodology
*Last updated: 2026-10-03*

> **Scope:** This document explains why these 10 ETFs were chosen as the starting universe. Quantitative due diligence is deferred to later phases (see Section 6).


## 1. Purpose of the ETF Universe

The ETF universe gives the platform a set of real, investable instruments for testing portfolio construction, return analysis, risk measurement, asset allocation, and reporting. It is not an investment recommendation.

The universe is limited to U.S.-listed, public-market ETFs. They publish holdings, trade daily, and long historical price series are available for all ten funds, which makes them a workable base for the first phases of the project. All returns are measured in U.S. dollars.

The ten funds cover the following asset classes and portfolio roles:

- U.S. large-cap equity
- U.S. growth equity
- U.S. small-cap equity
- Developed international equity
- Emerging markets equity
- Core fixed income
- Long-duration government bonds
- Investment-grade corporate bonds
- Listed real estate
- Gold


## 2. Selection Framework

The selection follows the due diligence approach in the CFA Institute Research Foundation's guide to ETFs (Hill, Kashner, & Nadig, 2026), which evaluates ETFs on three criteria:

1. **Efficiency:** the cost and operational reliability of the ETF, including expense ratio, tracking quality, tax considerations, and operational risks.
2. **Tradability:** how easily the ETF can be bought or sold, including trading volume, bid-ask spread, and market depth.
3. **Fit:** whether the ETF provides the intended exposure for the portfolio's objective, judged by asset class, region, currency, benchmark, risk profile, and portfolio role.

Module 2 of the guide recommends keeping a written record of the inputs and rationale used to balance the three criteria. This document is that record for the starting universe.

**How this project applies the framework at this stage**

- **Fit** is applied at the level of exposure and portfolio role. Comparing each fund's holdings against its market segment is deferred to Phase 1c.
- **Efficiency** is assessed qualitatively using structure, fees, fund age, and the availability of lower-cost or newer alternatives, while **Tradability** considers trading volume, bid-ask spreads and market depth. The quantitative measures are listed in Section 6.


## 3. Selected ETFs

| Ticker | Provider | Benchmark / exposure | Portfolio role | Launched | Selection rationale |
|:---:|---|---|---|:---:|---|
| SPY | State Street (SPDR) | S&P 500 | Core U.S. large-cap equity | 1993 | Oldest U.S. ETF; liquidity leader among S&P 500 funds |
| QQQ | Invesco | Nasdaq-100 | U.S. growth and technology tilt | 1999 | Long-established Nasdaq-100 fund; adds a more concentrated growth and technology tilt relative to SPY. |
| IWM | iShares | Russell 2000 | U.S. small-cap equity | 2000 | Long-running fund on the standard U.S. small-cap benchmark |
| EFA | iShares | MSCI EAFE | Developed markets outside North America | 2001 | History predates the lower-cost IEFA (2012) by over a decade |
| EEM | iShares | MSCI Emerging Markets | Emerging markets equity | 2003 | History predates the lower-cost IEMG (2012) by nearly a decade |
| AGG | iShares | Bloomberg U.S. Aggregate Bond | Core investment-grade bonds | 2003 | Tracks the standard U.S. bond-market benchmark |
| TLT | iShares | ICE U.S. Treasury 20+ Year | Long-duration U.S. Treasuries | 2002 | Isolates long-duration interest-rate exposure |
| LQD | iShares | iBoxx USD Liquid Investment Grade | Investment-grade corporate bonds | 2002 | Isolates investment-grade credit exposure |
| VNQ | Vanguard | MSCI US IMI Real Estate 25/50 | Listed real estate (REITs) | 2004 | Broad U.S. REIT exposure with history back to 2004 |
| GLD | State Street (SPDR) | Gold bullion | Gold as a defensive alternative | 2004 | Physically backed gold with history back to 2004 |

The ten ETFs have common fund history from November 2004, when GLD launched. PRIP currently uses 2015-01-02 as the analytical start date, providing more than a decade of common data while covering several materially different market environments. This analytical window includes the 2018 Q4 selloff, the 2020 COVID-19 drawdown, and the 2022 inflation and interest-rate shock.

### Known trade-offs

- **SPY has cheaper alternatives.** Hill, Kashner, & Nadig (2025, p. 6) report that SPY charged the highest fee of four S&P 500 ETFs (0.09%, versus 0.02% to 0.03% for SPLG, IVV, and VOO) while remaining the liquidity leader. It is kept for its liquidity and history.
- **EFA and EEM have cheaper alternatives** from the same provider: IEFA and IEMG, both launched in 2012 (Hill, Kashner, & Nadig, 2025, Appendix B). EFA and EEM are kept for their longer histories. Their liquidity will be measured in Phase 1c.
- **QQQ overlaps with SPY** through their shared large-cap technology holdings. It is kept for its distinct growth tilt.
- **AGG overlaps with TLT and LQD.** The Bloomberg U.S. Aggregate includes both Treasuries and investment-grade corporates. AGG serves as the broad core bond holding, while TLT and LQD isolate duration and credit risk. The overlap will be quantified in Phase 1e.
- **SPY and GLD use non-standard structures.** Hill, Kashner, & Nadig (2025, pp. 24-25) classify SPY as a unit investment trust and GLD as a grantor trust, which carry different rules for dividend reinvestment, replication, and taxation. They are accepted because both funds are simple and widely traded.
- **QQQ changed structure during the price history.** The source above also lists QQQ as a unit investment trust, but shareholders approved its conversion to an open-end ETF in December 2025, effective December 22, 2025, with the expense ratio cut from 0.20% to 0.18% (Invesco, 2025). Its history before that date reflects unit investment trust rules.
- **VNQ's income differs from bond income.** Hill, Nadig, & Hougan (2015) note that return-of-capital (ROC) distributions, which exceed a fund's earnings and reduce cost basis rather than being taxed as income, typically appear only in REIT and master-limited-partnership ETFs. VNQ's distribution and tax characteristics will therefore be considered separately from bond ETFs during quantitative due diligence.

These trade-offs are accepted for the starting universe and will be reviewed in later phases.


## 4. Why Other ETFs Were Not Selected

The goal is a small, clean universe that covers the major asset classes, not a comparison of every ETF on the market. The following were excluded:

- Duplicate funds with near-identical exposure, such as additional S&P 500 ETFs
- Leveraged and inverse ETFs
- Niche thematic ETFs
- ETFs with short price histories
- Thinly traded ETFs
- Actively managed ETFs, which require manager due diligence
- ETFs built on futures, swaps, or other derivatives

Hill, Kashner, & Nadig (2025, p. 10) note that ETFs built on futures, swaps, leverage, or inverse exposure carry more complex structures, counterparty risk, and unfamiliar tax treatment, which supports keeping them out of a starting universe.


## 5. Data Sources

The ETF list was built from provider information published by State Street (SPDR), Invesco, iShares (BlackRock), and Vanguard.

Historical prices are downloaded from Tiingo, which provides free end-of-day market data. Returns are calculated from Tiingo's adjusted-close series, whose adjustment methodology incorporates dividends and splits, so that bond and  Real Estate Investment Trust (REIT) returns are not understated.

Tiingo provides market prices, not fund NAVs or index levels. Metrics that require NAV or index data, such as tracking difference and premium/discount behavior, will need an additional source, which will be documented in the phase that uses it.


## 6. Current Limitations

The universe is a starting point for analysis, not a final investment recommendation. Later phases will apply quantitative due diligence across the three E-T-F dimensions:

### Efficiency

- Expense ratio — **Phase 1c**
- Tracking difference — **Phase 1c**
- Tracking error — **Phase 1c**
- Tax and structural considerations — **Phase 1c**


### Tradability

- Bid-ask spread — **Phase 1c**
- Trading volume — **Phase 1c**
- Average daily dollar volume — **Phase 1c**
- Premium/discount behavior — **Phase 2**
- Implied liquidity of the underlying basket — **Phase 3**


### Fit

- Historical volatility — **Phase 1b**
- Correlation — **Phase 1b**
- Portfolio role and risk contribution — **Phase 1b**
- Benchmark exposure — **Phase 1c**
- Holding overlap — **Phase 1e**
- Sector and security concentration — **Phase 1e**

Tracking difference and tracking error will be treated separately. Hill, Kashner, & Nadig (2026, p. 4) define tracking difference as the central tendency of rolling one-year differences between ETF NAV and index returns, and tracking error as the standard deviation of daily return differences.

The universe also contains no cash or Treasury bill proxy. Risk-adjusted measures such as the Sharpe ratio need a risk-free rate series, and its source will be documented in Phase 1b.


## References

Hill, J. M., Kashner, E., & Nadig, D. (2025). *A comprehensive guide to ETFs* (2nd ed.): Module 1: ETF features and evolving landscape. CFA Institute Research Foundation.

Hill, J. M., Kashner, E., & Nadig, D. (2026). *A comprehensive guide to ETFs* (2nd ed.): Module 2: Evaluating ETFs. CFA Institute Research Foundation.

Hill, J. M., Nadig, D., & Hougan, M. (2015). *A comprehensive guide to exchange-traded funds (ETFs)*. CFA Institute Research Foundation. With an appendix on international ETFs by Deborah Fuhr.

Invesco Ltd. (2025, December 19). *Invesco QQQ shareholders vote to approve modernization* [Press release].