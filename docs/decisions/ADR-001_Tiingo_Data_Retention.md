# ADR-001 — Tiingo Data Retention and Transient Processing

**Date:** 2026-10-03  
**Status:** Accepted

## Context

Phase 1a of PRIP used a conventional raw-to-processed architecture. Historical Tiingo responses were saved locally, cleaned into a processed price dataset, and used to calculate ETF returns and portfolio performance.

While drafting Phase 1a.5, a requirement to keep dated raw-data snapshots for reproducibility prompted a review of Tiingo's Terms of Use. The terms were updated on August 5, 2026. Section 1.6(a) states that Starter and trial plan users may not save, archive, back up, or otherwise retain Tiingo Data in any persistent storage, including local files, databases, logs, archives, and backups. Data may only be processed in memory and must be deleted when the calculation finishes.

PRIP uses the free Starter plan, so the Phase 1a architecture is not compliant, and the proposed snapshot requirement could not be adopted.

## Options Considered

1. **Upgrade to the Tiingo Power plan ($30/month).** Tiingo's Terms allow an eligible paid plan to persist data only to the extent permitted by that specific plan. This is not chosen because the additional cost is not currently justified, and persistence rights would still need to be confirmed for the applicable Power subscription. Data retained under a qualifying paid plan must generally be deleted if the subscription ends or is downgraded unless Tiingo agrees otherwise in writing.
2. **Request written permission from Tiingo for educational use.** Not pursued. A transient architecture meets the project's objectives without it.
3. **Switch to another data provider.** Not chosen at this time. It remains an option if transient processing proves unworkable.
4. **Process Tiingo data transiently.** Chosen.

## Decision

PRIP will stop storing Tiingo market data. Each run will fetch the data it needs, process it in memory, and keep only results that cannot be used to reconstruct the source data.

Each run will:

1. retrieve Tiingo data from the API when the analysis requires it;
2. validate and transform the data in memory;
3. calculate portfolio analytics within the same run; and
4. discard the Tiingo data when the run ends.

PRIP will retain:

- its own configuration and ETF-universe files;
- code and methodology documentation;
- synthetic test fixtures;
- run metadata and validation results that contain no Tiingo prices (tickers, date range, row counts, pass/fail);
- cryptographic data fingerprints that combine at least five distinct Tiingo data fields in each hash, use a secure one-way algorithm, and cannot reasonably be used to recover, match, confirm, or reproduce the underlying data, consistent with  Section 1.6(c); and
- aggregate analytical outputs, such as volatility, Sharpe ratio, maximum drawdown, and correlations, where the output satisfies Tiingo's Derived Product requirements and cannot reasonably be used to reconstruct the underlying Tiingo Data.

PRIP will not retain or publish:

- raw Tiingo responses or processed price datasets;
- daily return series supplied with a starting value, or any series complete enough to rebuild prices;
- growth-of-$100,000 or similar indexed charts where the sequence could expose or permit reconstruction of underlying Tiingo-derived data; or
- any file, table, or chart from which Tiingo prices could be recovered.

## Consequences

### Positive

- Once existing retained Tiingo data is removed and the transient-processing controls are implemented (see Implementation), PRIP's architecture will be aligned with the Starter-plan retention restrictions identified in Section 1.6.
- The pipeline treats the data source as an input that is fetched, not owned, which makes a later change of provider simpler.
- Every new output now needs a licensing check before it is kept or published.

### Trade-offs

- Exact input data cannot be stored, so a later run may produce slightly different results if Tiingo corrects data or applies new corporate-action adjustments.
- Reproducibility therefore covers the code, configuration, validation rules, and recorded run metadata and fingerprints, not the input data itself.
- Every run depends on the Tiingo API being available. Starter limits (50 requests per hour, 1,000 per day) are sufficient for the 10-ETF universe but leave limited room for repeated reruns.
- Tools used in later phases cannot hold Tiingo prices. This rules out SQL price tables, Power BI datasets with imported prices, Alteryx files containing prices, Jupyter notebooks saved with data in their output cells, and logs that record prices. Later phases must work from aggregate outputs or fetch data within the run.

## Implementation

The change will be implemented in Phase 1a.5 — DataOps & DevOps Foundation, including:

1. deleting all existing Tiingo data from local folders, databases, caches, backups, and any cloud-synced storage;
2. checking the Git history and, if Tiingo data was ever committed, removing it from the history as well as the current files;
3. reviewing published Phase 1a outputs (README, documentation, charts) and removing any that could reveal Tiingo prices;
4. clearing output cells from saved notebooks; and
5. refactoring the pipeline so that no Tiingo data is written to disk.

Phase 1a's code and documentation remain the record of the original implementation. Its stored data does not.

## Source Reviewed

This decision is based on Tiingo's Terms of Use, Section 1.6
(Data Storage, Retention, and Derived Products), last updated
August 5, 2026, and Tiingo's pricing information reviewed on
2026-10-03.

Terms:
https://app.tiingo.com/tos/

Pricing:
https://www.tiingo.com/account/billing/pricing

## Revisit When

- PRIP moves to a paid Tiingo plan;
- Tiingo grants written permission for a different retention arrangement;
- the project switches to another data provider; or
- Tiingo changes its terms.