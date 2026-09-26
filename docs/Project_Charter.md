# Project Charter — Portfolio Risk Intelligence Platform (PRIP)

*Last updated: 2026-09-25*

> **Purpose:** This charter defines the business problem, objectives, users, scope, analytical architecture, technology stack, research foundation, project modules, delivery roadmap, assumptions, and success criteria for the Portfolio Risk Intelligence Platform.

---

## 1. Project Overview

The **Portfolio Risk Intelligence Platform (PRIP)** is an institutional-style buy-side portfolio analytics workflow designed to demonstrate how investment research, portfolio-management principles, data engineering, workflow automation, risk analytics, and business intelligence can be combined into a repeatable decision-support process.

The project begins with a deliberately manageable universe of 10 exchange-traded funds (ETFs) representing major public-market exposures across equities, fixed income, real estate, and gold.

The initial ETF universe provides a practical environment for developing and testing portfolio analytics because ETFs offer transparent, tradable, and historically observable exposures across multiple asset classes.

PRIP is not intended to be a simple buy-and-hold performance project. As the project develops, it will incorporate:

* portfolio performance and risk analysis,
* ETF due diligence,
* allocation monitoring,
* portfolio rebalancing,
* holdings overlap analysis,
* tracking difference and tracking error,
* implied liquidity,
* ETF premium/discount analysis,
* ETF creation/redemption mechanics,
* investment reporting, and
* investment-governance documentation.

The project is educational and analytical in nature. It is not intended to provide investment advice, issue trading recommendations, or execute live trades.

---

## 2. Business Problem

Institutional investment teams work with market prices, ETF holdings, benchmarks, portfolio weights, target allocations, risk measures, and reporting requirements across multiple systems and data sources.

Without a structured analytical workflow, several problems can arise:

* ETF selection decisions may not be clearly documented.
* Portfolio data may be scattered across spreadsheets, market-data files, provider reports, and analytical systems.
* Return and risk calculations may be inconsistent between analysts or reporting periods.
* Portfolios may appear diversified while containing significant hidden overlap in their underlying holdings.
* Market movements and cash flows may cause portfolios to drift from approved target allocations.
* Rebalancing calculations may become repetitive and operationally intensive.
* ETF trading volume alone may provide an incomplete picture of the liquidity available through the underlying basket.
* ETF returns may deviate from their benchmarks because of fees, cash holdings, sampling, tax effects, securities lending, and trading costs.
* Portfolio managers and investment committees may receive large volumes of raw data without concise, decision-ready insights.
* Investment decisions may lack a clear audit trail connecting source data, assumptions, methodology, calculations, and conclusions.

PRIP addresses these problems by creating a **repeatable, documented, and auditable workflow from investment data to portfolio decision support**.

---

## 3. Project Objective

The primary objective is to build an end-to-end portfolio analytics platform that demonstrates the ability to:

1. Define and document an investment universe.
2. Acquire and validate investment-market data.
3. Store investment data in a structured format.
4. Calculate portfolio returns and risk measures.
5. Evaluate ETFs using a documented due-diligence framework.
6. Monitor portfolio allocation and concentration.
7. Automate portfolio rebalancing calculations.
8. Analyze ETF holdings and hidden exposure overlap.
9. Investigate ETF liquidity, tracking risk, and market mechanics.
10. Present portfolio information through decision-focused reporting.
11. Maintain a transparent record of assumptions, methodologies, limitations, and analytical decisions.

---

## 4. Intended Users

PRIP is designed to simulate analytical support for users such as:

* Portfolio Managers
* Investment Analysts
* Buy-Side Research Analysts
* Risk Analysts
* Investment Operations Teams
* Wealth Management and Model Portfolio Teams
* Business Intelligence Analysts in investment organizations
* Investment Committees
* Chief Investment Officers and other senior decision-makers

The project is also intended to demonstrate technical, analytical, and investment-management capabilities to prospective employers.

---

## 5. Core Institutional Questions

The completed platform should help support questions in several areas.

### Portfolio Construction

* What instruments are included in the investment universe?
* Why was each ETF selected?
* What investment exposure does each ETF provide?
* What role does each ETF play within the portfolio?
* How should capital be allocated across asset classes?

### Performance

* How has the portfolio performed historically?
* What are its cumulative and annualized returns?
* How does performance compare with relevant benchmarks?
* Which holdings contribute most to portfolio return?

### Risk

* What is the portfolio's historical volatility?
* What has been its maximum drawdown?
* How correlated are the portfolio holdings?
* Which assets contribute the greatest portfolio risk?
* Where does concentration risk exist?
* How does risk change under different market conditions?

### ETF Due Diligence

* Is the ETF efficient to hold?
* Is the ETF sufficiently tradable?
* Does the ETF provide the intended exposure?
* How closely does it track its benchmark?
* What structural or cost trade-offs exist?
* How does its underlying basket affect portfolio exposure and liquidity?

### Portfolio Operations

* How far has the portfolio drifted from its approved target allocation?
* Which ETFs should be bought or sold to restore target weights?
* How should new cash inflows or withdrawals be allocated?
* How can rebalancing be performed consistently across multiple accounts?

### ETF Market Mechanics

* Is an ETF trading at a premium or discount to Net Asset Value (NAV) or estimated underlying value?
* How does the creation/redemption process help align ETF market prices with portfolio value?
* What does underlying basket liquidity imply about ETF trading capacity?
* What causes tracking difference and tracking error?

---

## 6. Initial ETF Universe

The initial analytical universe consists of 10 ETFs:

| Ticker | Primary Exposure                         |
| ------ | ---------------------------------------- |
| SPY    | U.S. large-cap equity                    |
| QQQ    | U.S. growth / technology-oriented equity |
| IWM    | U.S. small-cap equity                    |
| EFA    | Developed international equity           |
| EEM    | Emerging markets equity                  |
| AGG    | Core U.S. investment-grade fixed income  |
| TLT    | Long-duration U.S. Treasury bonds        |
| LQD    | Investment-grade corporate bonds         |
| VNQ    | Listed real estate                       |
| GLD    | Gold                                     |

The ETF universe is a **starting analytical universe**, not a final investment recommendation. It is deliberately scoped to public-market ETFs; the trade-off of staying public-market, given the broader growth of private capital, is discussed in the ETF selection methodology.

The detailed rationale, selection trade-offs, exclusions, methodological framework, and supporting references are documented separately in:

`docs/ETF_Selection_Methodology.md`

---

## 7. ETF Due-Diligence Framework

ETF analysis within PRIP is **adapted from** the CFA Institute Research Foundation framework of:

* **Efficiency**
* **Tradability**
* **Fit**

Efficiency considers issues such as:

* expense ratios,
* tracking quality,
* taxes,
* operational considerations,
* and holding costs.

Tradability considers:

* bid–ask spreads,
* trading volume,
* market depth,
* underlying basket liquidity,
* and the ability to transact efficiently.

Fit, in the source framework, measures the active risk a fund takes relative to its specific market segment. In this project, Fit is initially applied at a broader level (asset class, benchmark, geographic exposure, currency, holdings, risk profile, and the intended role of the ETF within the portfolio) as documented in the ETF selection methodology. The segment-level active-risk analysis is deferred to Module 3 (ETF Due Diligence), where it is applied quantitatively alongside tracking difference, tracking error, and liquidity measures.

The ETF selection methodology is documented separately so that the investment universe can later be challenged quantitatively rather than simply justified retrospectively.

---

## 8. Analytical Architecture

PRIP will follow the general analytical workflow:

**Investment Question**

↓

**ETF Universe and Research**

↓

**Market / Holdings Data Acquisition**

↓

**Data Cleaning and Validation**

↓

**Structured SQL Storage**

↓

**Portfolio and Risk Calculations**

↓

**ETF Due Diligence and Portfolio Analytics**

↓

**Rebalancing / Overlap / ETF Mechanics**

↓

**Power BI Reporting**

↓

**Investment Committee Decision Support**

The purpose of the architecture is to ensure that analytical outputs can be traced back to their original data, methodology, and assumptions. This workflow is the operational expansion of the same progression described in Section 17.

---

## 9. Technology Stack

### Visual Studio Code and WSL Ubuntu

Visual Studio Code with WSL Ubuntu serves as the primary development environment.

It is used for:

* Python development,
* SQL development,
* Markdown documentation,
* Git operations,
* terminal execution,
* and project structure management.

### Python

Python serves as the main analytical and data-processing engine.

Planned uses include:

* market-data extraction,
* data cleaning,
* return calculations,
* portfolio construction,
* risk analytics,
* tracking-risk calculations,
* holdings analysis,
* rebalancing logic,
* and reusable analytical functions.

Initial libraries include:

* pandas
* NumPy
* matplotlib
* requests
* SQLAlchemy

### SQL

SQL provides the structured analytical storage layer.

Planned datasets include:

* ETF metadata,
* historical market prices,
* returns,
* portfolio weights,
* portfolio performance,
* benchmark data,
* ETF holdings,
* risk metrics,
* and rebalance history.

### Alteryx Designer 2025.2

Alteryx Designer will support repeatable workflow automation, including:

* data cleansing,
* data validation,
* reconciliation,
* joins,
* ETF holdings preparation,
* analytical apps,
* macros,
* and reporting outputs.

### Alteryx Intelligence Suite 2025.2

Full daily ETF holdings are typically published by providers as structured files (e.g., CSV) rather than PDFs, and these are expected to be ingested directly through Python/SQL rather than through Intelligence Suite. Intelligence Suite is instead planned for document types that are genuinely unstructured or semi-structured, such as:

* ETF fact sheets and prospectuses,
* provider commentary and disclosure documents,
* and other PDF or text-based ETF-provider documents that support due diligence but are not the primary holdings data source.

This scoping will be confirmed once actual provider data formats are reviewed in Module 1.

### Alteryx Predictive Tools 2025.2

Predictive Tools may be used in later phases for:

* regression analysis,
* benchmark relationships,
* factor exposure,
* tracking-risk analysis,
* scenario analysis,
* and portfolio-risk modelling.

Predictive tools will be used primarily to understand relationships and risk rather than to claim reliable market-price prediction.

### Power BI

Power BI provides the business-intelligence and investment-reporting layer.

Potential reporting areas include:

* portfolio performance,
* risk,
* asset allocation,
* drawdown,
* concentration,
* ETF overlap,
* rebalancing,
* tracking risk,
* liquidity,
* and investment committee summaries.

### Git and GitHub

Git and GitHub will support:

* version control,
* change history,
* project documentation,
* code review,
* repository publishing,
* and future workflow automation.

---

## 10. Major Project Modules

### Module 1 — Portfolio Data Foundation

Establish the ETF universe, obtain historical market data, validate the datasets, calculate returns, and create the core project data structure.

### Module 2 — Portfolio Performance and Risk Analytics

Develop metrics including:

* cumulative return,
* annualized return,
* volatility,
* Sharpe ratio,
* Sortino ratio,
* maximum drawdown,
* correlation,
* and risk contribution.

### Module 3 — ETF Due Diligence

Quantitatively extend the Efficiency–Tradability–Fit methodology through measures such as:

* expense ratios,
* tracking difference,
* tracking error,
* bid–ask spreads,
* trading volume,
* implied liquidity,
* structural considerations,
* and portfolio fit, including segment-level active risk (see Section 7).

### Module 4 — ETF Rebalancing Engine

Develop a repeatable workflow that compares current allocations with target model weights.

The engine will calculate:

* current market value,
* current portfolio weight,
* target portfolio weight,
* target dollar allocation,
* trade amount,
* and shares to buy or sell.

A later Alteryx implementation may use a Batch Macro to apply the process across multiple accounts.

### Module 5 — ETF Holding Overlap Analyzer

Develop an interactive workflow that can:

* accept multiple ETF tickers,
* retrieve or import holdings,
* standardize securities,
* join holdings across ETFs,
* calculate shared exposure,
* identify repeated securities,
* measure hidden concentration,
* and present overlap results visually.

An Alteryx Analytic App is planned as one implementation.

### Module 6 — Investment Reporting

Develop Power BI dashboards that convert analytical results into decision-ready investment reporting.

### Advanced Module — ETF Premium/Discount Monitoring Prototype

Develop an analytical prototype comparing ETF market prices with NAV or estimated underlying portfolio value.

Potential components include:

* ETF market prices,
* holdings data,
* constituent prices,
* estimated basket valuation,
* premium/discount calculations,
* and pricing-anomaly flags.

This module will be presented as a research prototype because institutional intraday NAV and arbitrage analysis may require specialized market data.

### Advanced Module — ETF Market Mechanics

Analyze or simulate concepts including:

* Authorized Participant creation/redemption,
* AP arbitrage,
* premium/discount convergence,
* implied liquidity,
* underlying basket liquidity,
* tracking difference,
* tracking error,
* cash drag,
* sampling and optimization,
* securities lending,
* trading costs,
* and ETF legal structures.

---

## 11. Data Governance and Validation

A key objective of PRIP is to demonstrate that portfolio analytics should be controlled and reproducible.

Data-management practices will include:

* identifying the source of every external dataset,
* retaining raw data separately from processed data,
* documenting transformation logic,
* checking for missing observations,
* identifying duplicate records,
* validating data types,
* validating portfolio weights,
* reconciling analytical outputs where practical,
* documenting extraction dates,
* and recording known data limitations.

Raw data should not be manually overwritten after ingestion.

---

## 12. Project Scope

### In Scope

PRIP may include:

* public-market ETF analytics,
* ETF due diligence,
* historical portfolio analysis,
* portfolio risk measurement,
* rebalancing analytics,
* ETF holdings analysis,
* tracking-risk analysis,
* liquidity analysis,
* ETF mechanics,
* SQL data modelling,
* Alteryx workflow automation,
* Power BI reporting,
* business analysis documentation,
* and Git-based project management.

### Out of Scope for the Overall Project

The following are not primary project objectives:

* live securities trading,
* actual client trade execution,
* personalized investment recommendations,
* guaranteed return forecasting,
* high-frequency trading infrastructure,
* production-grade institutional order management,
* proprietary market-making systems,
* and use of non-public or improperly licensed data.

---

## 13. Delivery Roadmap

Detailed objectives, tasks, assumptions, validation checks, exclusions, and definitions of done are maintained in separate weekly roadmap documents.

The high-level roadmap is:

| Phase   | Focus                                                          | Module(s) |
| ------- | --------------------------------------------------------------- | --------- |
| Phase 1a  | Portfolio data foundation, ETF universe, SQL schema setup       | Module 1  |
| Phase 1b  | Portfolio performance and risk analytics                        | Module 2  |
| Phase 1c  | ETF due diligence (quantitative Efficiency–Tradability–Fit)      | Module 3  |
| Phase 1d  | ETF portfolio rebalancing engine                                 | Module 4  |
| Phase 1e  | ETF holdings overlap analyzer                                    | Module 5  |
| Phase 1f  | Power BI investment reporting                                    | Module 6  |
| Phase 2 | ETF premium/discount monitoring prototype                        | Advanced  |
| Phase 3 | ETF market mechanics                                              | Advanced  |

Alteryx validation work (data cleansing, reconciliation) is not a standalone phase; it runs alongside the module it supports, starting with Phase 1a.

The initial six-module delivery sequence is ambitious relative to the scope, particularly for Module 3 and Module 5. Phase durations may therefore vary without changing the module sequence or definitions of done.

The roadmap may evolve if empirical findings or data limitations justify a change.

Detailed weekly documentation will be maintained in:

`docs/roadmap/`

---

## 14. Research Foundation

The project is informed by CFA Institute Research Foundation and CFA Institute Research & Policy Center publications. Each source supports a distinct part of the project rather than all of it equally:

Hill, J. M., Kashner, E., & Nadig, D. (2025). *A comprehensive guide to ETFs (2nd ed.): Module 1: ETF features and evolving landscape.* CFA Institute Research Foundation.
— Supports ETF structure, mechanics, fee trends, and the ETF ecosystem (Modules 1–3, Section 9's data-format assumptions).

Hill, J. M., Kashner, E., & Nadig, D. (2026). *A comprehensive guide to ETFs (2nd ed.): Module 2: Evaluating ETFs.* CFA Institute Research Foundation.
— Supports the Efficiency–Tradability–Fit due-diligence framework (Section 7, Module 3).

Hill, J. M., Nadig, D., & Hougan, M. (2015). *A comprehensive guide to exchange-traded funds (ETFs).* CFA Institute Research Foundation. With an appendix on international ETFs by Deborah Fuhr.
— Supports additional structural and tax detail (e.g., legal structures, distribution treatment) referenced in the ETF selection methodology.

Preece, R., & Wilson, C.-A. (2026). *Understanding the growth of private markets: Structural shifts in the investment industry.* CFA Institute Research & Policy Center.
— Supports the framing decision to scope this project to public markets (Section 1, Section 6), given the broader shift of capital formation toward private markets. It is not a source for ETF mechanics, due diligence, or liquidity.

Additional external sources will be documented as they are introduced.

---

## 15. Assumptions and Limitations

The project currently assumes:

* sufficiently complete historical ETF data can be obtained for the selected universe;
* daily market data are adequate for the initial portfolio analytics;
* the initial analytical portfolio is denominated in USD;
* public ETF data can support an educational simulation of institutional portfolio workflows;
* free and public data may not replicate the quality, latency, licensing, or completeness of institutional market-data platforms;
* historical relationships do not imply future investment performance;
* public-market ETFs represent only part of the institutional investment opportunity set;
* ETF holdings data is available in structured form (e.g., CSV) from providers, and Alteryx Intelligence Suite is not required for core holdings ingestion (see Section 9);
* and the six-week core-module timeline in Section 13 is compressed relative to the scope defined in Section 10, and is a schedule risk rather than a firm commitment.

Major assumptions and limitations will be documented and revisited as the project evolves.

---

## 16. Project-Level Success Criteria

PRIP will be considered successful when it demonstrates a coherent progression from investment question to decision-support output.

At minimum, the completed project should demonstrate:

* a documented investment universe,
* research-supported ETF selection,
* reproducible market-data acquisition,
* controlled data transformation,
* structured data storage,
* valid portfolio-return calculations,
* portfolio-risk analytics,
* at least one automated portfolio workflow,
* portfolio reporting suitable for decision-makers,
* documented assumptions and limitations,
* clear research citations,
* and sufficient documentation for another analyst to understand and reproduce the analytical process.

---

## 17. Project Success Vision

The completed project should demonstrate the integration of investment knowledge with modern analytical tools.

Rather than presenting only charts or historical returns, PRIP should demonstrate the ability to move systematically from:

**Investment Question → Research → Data → Validation → Analysis → Portfolio Decision Support → Reporting**

This is the same progression set out in the analytical architecture in Section 8.

The final outcome should provide evidence of practical capability in:

* portfolio management,
* buy-side analytics,
* business analysis,
* Python,
* SQL,
* Alteryx,
* Power BI,
* workflow automation,
* data governance,
* documentation,
* and investment decision support.