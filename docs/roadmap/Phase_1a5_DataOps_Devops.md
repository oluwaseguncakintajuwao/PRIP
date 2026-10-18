# Phase 1a.5 — DataOps & DevOps Foundation

*Portfolio Risk Intelligence Platform (PRIP)*

## Objective

Phase 1a stored Tiingo price data locally. PRIP uses Tiingo's free Starter plan, whose Terms of Use prohibit storing Tiingo data in any persistent form, so the pipeline must move to in-memory processing. The reasoning is documented in `docs/decisions/ADR-001_Tiingo_Data_Retention.md`.

Phase 1a.5 makes that change and adds the controls that later phases depend on: pinned environments, reusable validation, automated tests, CI, and logging. It does not add new portfolio analytics.

## Scope

| Area | What we will do | Skill demonstrated |
|---|---|---|
| Architecture refactor | Change Tiingo ingestion from stored raw/processed files to in-memory processing | Data architecture |
| Data persistence controls | Apply the rules in [Data Persistence Rules](#data-persistence-rules) and add an automated check that enforces them | Data governance |
| Git hygiene | Confirm `.gitignore`, repository structure, and tracked files; use descriptive commit messages | Source control |
| Environment reproducibility | Pin dependency versions, record the Python version, and document setup | DevOps |
| Secrets management | Keep `.env` and the Tiingo API key local and out of Git; CI needs no Tiingo credentials | Security |
| Run provenance | Record run ID, date range, tickers, row counts, validation results, code version, and data fingerprints for each run | DataOps / auditability |
| Data validation | Convert the Phase 1a validation checks into reusable functions | Data quality |
| Automated testing | Add `pytest` tests that run on synthetic fixture data | Software engineering |
| Continuous integration | Run `ruff` and the test suite through GitHub Actions on every push | CI |
| Logging | Record each run's execution and validation results | Observability |
| Documentation | Document installation, running, testing, validation, and data-handling rules in the README | Documentation |

## Pipeline Flow

```text
ETF universe → Tiingo API → validate in memory → transform in memory
→ portfolio calculations → save permitted outputs → discard Tiingo data
```

The portfolio calculations are the ones Phase 1a already performs. No new analytics are introduced.

## Data Persistence Rules

Under the Starter-plan architecture, PRIP application code will not intentionally persist Tiingo market data to durable storage.

**Not persisted:**

- raw Tiingo API responses or HTTP caches (response caching is disabled in the API client);
- price tables, in any file format or database;
- daily return series for individual ETFs;
- daily portfolio-value, portfolio-return, drawdown, indexed-growth, and rolling-metric series calculated from Tiingo data, which are treated as temporary values within a run;
- charts, images, notebook output cells, and dashboard datasets built from any of the above; and
- logs or validation messages containing prices or return values.

**Persisted:**

- ETF-universe and configuration files;
- code and methodology documentation;
- synthetic test fixtures;
- run metadata and validation results (tickers, dates, row counts, pass/fail);
- data fingerprints that combine at least five distinct source-data fields in each hash, use a secure one-way cryptographic algorithm, and cannot reasonably be used to recover the underlying market data, where permitted by the applicable license; and
- aggregate analytical results, such as total return, CAGR, annualized volatility, Sharpe and Sortino ratios, maximum drawdown statistics, correlation matrices, and sufficiently aggregated risk-contribution results, where they satisfy the applicable derived-product requirements.

The same rules apply to SQL, Power BI, Alteryx, and Jupyter in later phases.

## Validation Rules

The validation functions will check that:

1. every ticker in the approved ETF universe is present;
2. there are no duplicate ticker-date rows;
3. all ETFs cover the same expected trading dates, with unexpected gaps flagged;
4. required price fields are present and positive;
5. daily returns beyond a configurable threshold are flagged for review, not rejected, and each flag records only the ticker and date;
6. target portfolio weights sum to 1; and
7. the portfolio starts at $100,000.

The functions do not call the Tiingo API, so they can be tested on synthetic fixtures.

## Testing and CI

GitHub Actions will not call the Tiingo API. Tests run on small synthetic datasets committed to the repository, so CI needs no credentials, gives the same result every run, and is unaffected by API outages or rate limits.

A persistence test will run the pipeline against fixture data and fail if any file is written outside the permitted output folder.

Local and CI environments use the same Python version and pinned dependencies.

## Out of Scope

The following are deferred until the core portfolio analytics are stable:

- AWS deployment
- Terraform
- Docker
- Workflow orchestration
- Production scheduling
- Cloud monitoring

## Definition of Done

Phase 1a.5 is complete when:

1. Phase 1a's permitted aggregate results (ETF count, row counts, date range, validation results, initial portfolio value, final portfolio value, and cumulative portfolio return) are recorded before restricted stored datasets are removed;
2. all existing Tiingo data has been removed from local folders, databases, caches, backups, notebooks, published outputs, and Git history, as set out in ADR-001;
3. the pipeline processes Tiingo data in memory and the persistence test passes;
4. the environment can be recreated from the documented Python version and pinned dependencies;
5. no secrets are in Git, and CI runs without the Tiingo API key;
6. the seven validation rules are implemented as reusable functions and covered by `pytest` tests on synthetic fixtures;
7. `pytest` passes locally;
8. `ruff` and `pytest` pass in GitHub Actions;
9. each run writes a log entry containing only run metadata, with no prices or return values;
10. the README covers installation, running, testing, validation, and the data persistence rules; and
11. the revised pipeline reproduces the recorded Phase 1a baseline within a documented tolerance when run against current API data.

**Next: Phase 1b — Portfolio Performance & Risk Analytics**