# ETF Selection Methodology
*Last updated: 2026-09-22*
> **Scope:** This document explains why these 10 ETFs were chosen as the 
>starting universe. Detailed quantitative due diligence is deferred to
>later phases (see Section 6).


This framework is informed by CFA Institute Research Foundation ETF due diligence approach, which emphasizes efficiency, tradability, and fit when evaluating ETFs for portfolio use (Hill, Kashner, & Nadig, 2026).


## 1. Purpose of the ETF Universe

For this project, the ETF universe used is designed to support a buy-side portfolio analytics platform adapted from CFA Institute research and established portfolio-management principles. The idea of the ETF selection is not to recommend specific investments, but to create a realistic and diversified set of investable instruments that can be used to test portfolio construction, return analysis, risk measurement, asset allocation, and investment committee-style reporting.

The universe is deliberately scoped to public-market ETFs. Public listings have declined relative to private markets in recent years (Preece & Wilson, 2026), but public-market ETFs remain transparent, liquid, and have long, freely available price histories, which makes them a practical foundation for this stage of the project.

The selected ETFs provide broad exposure to major asset classes and distinct portfolio roles which include 
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

The selection follows the due diligence approach adapted from the CFA Institute Research Foundation's guide to ETFs (Hill, Kashner, & Nadig, 2026), which evaluates ETFs on three criteria:

1. Efficiency: the cost and operational reliability of the ETF. Expense ratio, tracking quality, tax considerations, and operational risks are factors in efficiency.
2. Tradability: how easily the ETF can be bought or sold, including trading volume, bid-ask spread, market depth, and suitability for portfolio implementation.
3. Fit: answers the question; "Does the ETF provide the intended exposure for the objective of the portfolio?" This project considers asset class, region, currency, benchmark, risk profile, and portfolio role.

Module 2 also recommends keeping a written record of the inputs and the rationale used to balance the three criteria. This document serves that purpose for the starting universe.

How this project adapts the framework
- Fit is applied at the level of exposure and portfolio role. Each ETF is checked for asset class, region, currency, benchmark, risk profile, and role in the portfolio. The deeper active-risk analysis, comparing each fund's holdings against its market segment, is deferred to later phases.
- Efficiency and Tradability are assessed qualitatively at this stage. The quantitative measures are listed in Section 6.


## 3. Why Were These ETFs Selected?

These ETFs were selected because they provide broad, recognizable, and historically available exposure when addressing multi-asset portfolio management.

| Ticker | Provider | Benchmark/exposure | Portfolio role |
|:---:|---|---|---|
|SPY | State Street (SPDR) | S&P 500| Core U.S. large-cap equity |
|QQQ| Invesco| Nasdaq-100| U.S. growth and technology-oriented equity|
|IWM|	iShares|	Russell 2000|	U.S. small-cap equity|
|EFA|	iShares|	MSCI EAFE|	Developed international equity outside North America|
|EEM	|iShares|	MSCI Emerging Markets|	Emerging markets equity|
|AGG|	iShares	|Bloomberg U.S. Aggregate Bond	|Core investment-grade bonds|
|TLT|	iShares	|ICE U.S. Treasury 20+ Year	|Long-duration U.S. Treasury bonds|
|LQD|	iShares	|iBoxx USD Liquid Investment Grade	|Investment-grade corporate bonds|
|VNQ|	Vanguard	|U.S. real estate (REIT) index	|Listed real estate (REITs and related companies)|
|GLD|	State Street (SPDR)	|Gold bullion	|Gold as a defensive alternative asset|

Together, these ETFs create a diversified public-market universe that can be used in the analysis of return, volatility, drawdown, correlation, asset allocation, risk contribution, and portfolio growth.

### Known trade-offs
- SPY has lower-cost alternatives with the same S&P 500 exposure. Hill, Kashner, & Nadig (2025, p. 6) report that SPY charged the highest fee of four S&P 500 ETFs (0.09%, versus 0.02% to 0.03% for SPLG, IVV, and VOO) while remaining the liquidity leader. It is retained for its liquidity and long price history.
- EFA and EEM also have lower-cost core alternatives from the same provider (IEFA and IEMG, launched in 2012; Hill, Kashner, & Nadig, 2025, Appendix B). They are retained primarily for their longer price histories and established market presence. Liquidity will be evaluated quantitatively in a later phase.
- QQQ overlaps with the large-cap technology holdings in SPY. It is kept because it gives a distinct growth and technology tilt.
- SPY, QQQ, and GLD use structures other than the standard open-end ETF. Hill, Kashner, & Nadig (2025, pp. 24-25) classify SPY and QQQ as unit investment trusts and GLD as a grantor trust. These structures carry different rules for dividend reinvestment, replication, and taxation. They are accepted here because the funds are simple, long-established, and widely traded.
- VNQ's income character differs from the bond ETFs (AGG, TLT, LQD) in the universe. Hill, Nadig, & Hougan (2015) note that return-of-capital (ROC) distributions, which are paid out in excess of a fund's earnings and reduce cost basis rather than being taxed as income, are typically seen only in REIT and master-limited-partnership ETFs. This is a reason to treat VNQ's distributions separately from bond income when analyzing total return.

These trade-offs are accepted for the starting universe and will be reviewed in later phases.


## 4. ETF List Source

The ETF list was developed from official ETF provider information and then filtered based on the project objective.

The ETF provider sources include State Street/SPDR, Invesco, iShares/BlackRock, and Vanguard. These providers were used because they offer widely recognized ETFs with clear investment objectives, available historical price data, and exposure to major asset classes.

The project also uses CFA Institute Research Foundation materials as a methodological foundation for ETF evaluation, especially based on the concepts of efficiency, tradability, and fit.

Historical price data for analysis will be downloaded from Stooq, which provides free historical market data. The project uses this data source for educational and analytical purposes.


## 5. Why Other ETFs Were Not Selected

The initial objective is to build a clean and manageable portfolio analytics foundation, not to do a comparative analysis of every ETF in the market.

This project intentionally excludes:

- Duplicate ETFs with similar exposure, such as multiple S&P 500 ETFs.
- Leveraged ETFs
- Inverse ETFs
- Highly niche thematic ETFs
- ETFs with limited historical data
- Thinly traded ETFs
- ETFs that would complicate the initial analysis without adding meaningful asset-class coverage
- Actively managed ETFs that require deeper manager due diligence
- Complex ETFs that may introduce additional structure, leverage, derivative, or liquidity risks

Hill, Kashner, & Nadig (2025, p. 10) note that ETFs built on futures, swaps, leverage, or inverse exposure involve more complex structures, counterparty risk, and unfamiliar tax treatment, which supports keeping them out of a starting universe.


## 6. Current Limitation

The ETF universe represents a starting analytical universe rather than a final investment recommendation. Subsequent phases will subject the selected ETFs to quantitative due diligence across the three dimensions of the E-T-F framework:

#### Efficiency
- Expense ratio
- Tracking difference
- Tracking error
- Tax and structural considerations

#### Tradability
- Bid-ask spread
- Trading volume
- Average daily dollar volume
- Premium/discount behaviour
- Implied liquidity of the underlying basket

#### Fit
- Historical volatility
- Correlation
- Holding overlap
- Sector and security concentration
- Benchmark exposure
- Portfolio role and risk contribution

Tracking difference and tracking error will be treated separately. Hill, Kashner, Nadig (2026, p. 4) define tracking difference using the central tendency of rolling one-year ETF NAV-versus-index return differences, whereas tracking error measures the standard deviation of daily return differences.



## References

Hill, J. M., Kashner, E., & Nadig, D. (2025). A comprehensive guide to ETFs (2nd ed.): Module 1: ETF features and evolving landscape. CFA Institute Research Foundation.

Hill, J. M., Kashner, E., & Nadig, D. (2026). A comprehensive guide to ETFs (2nd ed.): Module 2: Evaluating ETFs. CFA Institute Research Foundation.

Hill, J. M., Nadig, D., & Hougan, M. (2015). A comprehensive guide to exchange-traded funds (ETFs). CFA Institute Research Foundation. With an appendix on international ETFs by Deborah Fuhr.

Preece, R., & Wilson, C.-A. (2026). Understanding the growth of private markets: Structural shifts in the investment industry. CFA Institute Research & Policy Center.