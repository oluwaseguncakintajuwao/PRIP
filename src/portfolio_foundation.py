"""
PRIP - Portfolio Risk Intelligence Platform

Step 1: Load and validate the ETF universe, then download daily price history
from Tiingo for every ticker.

Pipeline layers:
    data/raw/tiingo/<RUN_ID>/        untouched Tiingo responses, one CSV per ticker
    data/processed/                  cleaned, validated long-format price table
    data/processed/run_metadata/     one JSON audit record per extraction run

Usage:
    export TIINGO_API_KEY="..."
    export PRIP_END_DATE="20260925"  # optional, pins the end date for reproducibility
    python src/portfolio_foundation.py
"""

# Standard library
import json
import logging
import os
import sys
import time
from datetime import date, datetime, timezone
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv

# Third-party
import numpy as np
import pandas as pd
import requests

# --------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

ETF_UNIVERSE_FILE = PROJECT_ROOT / "data" / "sample" / "etf_universe.csv"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


DAILY_RETURNS_FILE = (
    OUTPUT_DIR / "daily_returns.csv"
)

PORTFOLIO_GROWTH_FILE = (
    OUTPUT_DIR / "equal_weight_portfolio_growth.csv"
)

INITIAL_PORTFOLIO_VALUE = 100_000.0

# Capture the run timestamp once so all run-specific paths stay consistent.
RUN_TIMESTAMP = datetime.now(timezone.utc)
RUN_ID = RUN_TIMESTAMP.strftime("%Y%m%dT%H%M%SZ")

EXTRACTION_DATE = RUN_TIMESTAMP.date()
EXTRACTION_DATE_STR = EXTRACTION_DATE.strftime("%Y-%m-%d")

# Preserve each raw extraction as a separate run.
RAW_RUN_DIR = RAW_DATA_DIR / "tiingo" / RUN_ID

PROCESSED_PRICES_FILE = PROCESSED_DATA_DIR / "etf_prices_long.csv"

RUN_METADATA_DIR = PROCESSED_DATA_DIR / "run_metadata"
RUN_METADATA_FILE = RUN_METADATA_DIR / f"{RUN_ID}.json"

START_DATE = "20150101"

# Can be pinned for reproducibility; otherwise defaults to extraction date.
END_DATE = os.getenv(
    "PRIP_END_DATE",
    EXTRACTION_DATE.strftime("%Y%m%d"),
)

# The starting universe is designed around ten instruments, so an accidental
# addition or removal should fail the run. Relax once the universe becomes
# configurable.
EXPECTED_ETF_COUNT = 10
WEIGHT_TOLERANCE = 1e-6

TIINGO_BASE_URL = "https://api.tiingo.com/tiingo/daily"
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

REQUEST_TIMEOUT_SECONDS = 30
REQUEST_PAUSE_SECONDS = 1.0  # courtesy delay between tickers
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2.0  # doubles after each failed attempt
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

REQUIRED_UNIVERSE_COLUMNS = {
    "ticker",
    "asset_name",
    "asset_class",
    "region",
    "currency",
    "portfolio_role",
    "target_weight",
    "due_diligence_note",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("prip.foundation")


# --------------------------------------------------------------------
# EXCEPTIONS
# --------------------------------------------------------------------

class UniverseValidationError(ValueError):
    """The ETF universe file failed a configuration check."""


class DataDownloadError(RuntimeError):
    """A ticker's price data could not be downloaded or failed validation."""


# --------------------------------------------------------------------
# ETF UNIVERSE
# --------------------------------------------------------------------

def load_etf_universe(
    file_path: Path,
    expected_count: int | None = None,
) -> pd.DataFrame:
    """Load the ETF universe CSV and validate its structure and weights."""

    if not file_path.exists():
        raise UniverseValidationError(f"ETF universe file not found: {file_path}")

    df = pd.read_csv(file_path)

    missing_columns = REQUIRED_UNIVERSE_COLUMNS - set(df.columns)
    if missing_columns:
        raise UniverseValidationError(
            f"ETF universe is missing required columns: {sorted(missing_columns)}"
        )

    # Missing tickers first, so duplicate detection never sees NaN.
    if df["ticker"].isna().any():
        raise UniverseValidationError("ETF universe contains missing ticker values."
    )

    df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
    if (df["ticker"] == "").any():
        raise UniverseValidationError(
        "ETF universe contains blank ticker values."
    )

    duplicates = df.loc[df["ticker"].duplicated(), "ticker"].tolist()
    if duplicates:
        raise UniverseValidationError(
            f"ETF universe contains duplicate tickers: {duplicates}"
        )

    if expected_count is not None and len(df) != expected_count:
        raise UniverseValidationError(
            f"Expected {expected_count} ETFs, but found {len(df)}."
        )

    try:
        weights = pd.to_numeric(df["target_weight"], errors="raise")
    except (ValueError, TypeError) as exc:
        raise UniverseValidationError(
            f"target_weight contains non-numeric values: {exc}"
        ) from exc

    if weights.isna().any():
        missing = df.loc[weights.isna(), "ticker"].tolist()
        raise UniverseValidationError(f"Missing target_weight for: {missing}")

    if (weights < 0).any():
        negative = df.loc[weights < 0, "ticker"].tolist()
        raise UniverseValidationError(f"Negative target_weight for: {negative}")

    weight_total = weights.sum()
    if not np.isclose(weight_total, 1.0, atol=WEIGHT_TOLERANCE):
        raise UniverseValidationError(
            f"Target weights must sum to 1.00. Current total: {weight_total:.6f}"
        )

    df["target_weight"] = weights
    return df


# --------------------------------------------------------------------
# TIINGO DOWNLOAD
# --------------------------------------------------------------------

def format_tiingo_date(date_string: str) -> str:
    """Convert YYYYMMDD to Tiingo's YYYY-MM-DD date format."""

    try:
        return datetime.strptime(date_string, "%Y%m%d").strftime("%Y-%m-%d")
    except ValueError as exc:
        raise DataDownloadError(
            f"Invalid date {date_string!r}; expected YYYYMMDD."
        ) from exc


def fetch_tiingo_csv(
    session: requests.Session,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str,
) -> str:
    """Request raw daily EOD CSV data from Tiingo, retrying transient failures."""

    if not api_key:
        raise DataDownloadError(
            "TIINGO_API_KEY is not set."
        )

    url = f"{TIINGO_BASE_URL}/{ticker.lower()}/prices"

    params = {
        "startDate": format_tiingo_date(start_date),
        "endDate": format_tiingo_date(end_date),
        "format": "csv",
        "resampleFreq": "daily",
    }

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }

    last_error = "unknown error"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(
                url,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            last_error = f"network error ({type(exc).__name__})"
        else:
            if response.status_code == 200:
                return response.text

            last_error = f"HTTP {response.status_code}"

            if response.status_code not in RETRYABLE_STATUS_CODES:
                break

        if attempt < MAX_RETRIES:
            wait = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))

            logger.warning(
                "%s: attempt %d/%d failed (%s); retrying in %.0fs",
                ticker,
                attempt,
                MAX_RETRIES,
                last_error,
                wait,
            )

            time.sleep(wait)

    raise DataDownloadError(
        f"{ticker}: download failed after retries - {last_error}"
    )

def check_tiingo_response(response_text: str, ticker: str) -> str:
    """Reject Tiingo responses that are not valid price CSV data."""

    text = response_text.strip()

    if not text:
        raise DataDownloadError(
            f"{ticker}: Tiingo returned an empty response."
        )

    first_line = text.splitlines()[0].lower()

    if "date" in first_line and "close" in first_line:
        return text

    lowered = text.lower()

    if (
        "invalid token" in lowered
        or "authentication" in lowered
        or "unauthorized" in lowered
    ):
        raise DataDownloadError(
            f"{ticker}: Tiingo authentication failed. "
            "Check TIINGO_API_KEY."
        )

    raise DataDownloadError(
        f"{ticker}: unexpected Tiingo response: {text[:150]!r}"
    )

def save_raw_response(
    text: str,
    ticker: str,
    raw_dir: Path,
) -> Path:
    """Persist the untouched API response for the audit trail."""

    path = raw_dir / f"{ticker}.csv"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

    return path

# --------------------------------------------------------------------
# CLEANING
# --------------------------------------------------------------------

def clean_price_data(raw_text: str, ticker: str) -> pd.DataFrame:
    """Parse a raw Tiingo CSV into a validated, snake_case, date-sorted frame."""

    df = pd.read_csv(StringIO(raw_text))
    df.columns = [col.strip().lower() for col in df.columns]

    required = {"date", "open", "high", "low", "close", "volume", "adjopen", "adjhigh", "adjlow", "adjclose", "adjvolume", "divcash", "splitfactor",}
    missing = required - set(df.columns)
    if missing:
        raise DataDownloadError(f"{ticker}: price data missing columns {sorted(missing)}")

# Parse Tiingo date/timestamp.
    df["date"] = pd.to_datetime (
        df["date"],
        errors="coerce",
        utc=True,
    ).dt.tz_convert(None)

    numeric_cols = ["open", "high", "low", "close", "volume", "adjopen", "adjhigh", "adjlow", "adjclose", "adjvolume", "divcash", "splitfactor",]

    df[numeric_cols] = df[numeric_cols].apply(
        pd.to_numeric,
        errors="coerce",
    )

    ohlc_cols = ["open", "high", "low", "close"]

    adjusted_ohlc_cols = ["adjopen", "adjhigh", "adjlow", "adjclose",]

# A usable record requires a valid date, raw OHLC data,
# and adjusted OHLC data.
    bad_rows = (
    df["date"].isna() | df[ohlc_cols].isna().any(axis=1) | df[adjusted_ohlc_cols].isna().any(axis=1)
    )
    if bad_rows.any():
        logger.warning("%s: dropping %d unparseable rows", ticker, int(bad_rows.sum()),
    )
    df = df.loc[~bad_rows].copy()

    if df.empty:
        raise DataDownloadError(f"{ticker}: no valid rows after cleaning.")

    if df["date"].duplicated().any():
        raise DataDownloadError(f"{ticker}: duplicate trading dates in price data.")

    if (df[adjusted_ohlc_cols] <= 0).any().any():
        raise DataDownloadError(f"{ticker}: non-positive OHLC prices found.")

    df = df.sort_values("date").reset_index(drop=True)

    df.insert(0, "ticker", ticker)

    return df[["ticker", "date", "open", "high", "low", "close", "volume", "adjopen", "adjhigh", "adjlow", "adjclose", "adjvolume", "divcash", "splitfactor",]]


# --------------------------------------------------------------------
# CALCULATE ETF DAILY RETURNS
# --------------------------------------------------------------------

def calculate_daily_returns(
    prices: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate daily ETF returns using Tiingo adjusted close prices."""

    returns = prices[
        [
            "ticker",
            "date",
            "adjclose",
        ]
    ].copy()

    returns = returns.sort_values(
        ["ticker", "date"]
    ).reset_index(drop=True)

    returns["daily_return"] = (
        returns.groupby("ticker")["adjclose"]
        .pct_change(fill_method=None)
    )
    return returns

# -------------------------------------------------------------------
# CONSTRUCT THE $100,000 BASELINE PORTFOLIO
# -------------------------------------------------------------------

def calculate_equal_weight_portfolio(
    prices: pd.DataFrame,
    initial_portfolio_value: float = 100_000.0,
) -> pd.DataFrame:
    """
    Construct an initially equal-weight, buy-and-hold portfolio.

    Each ETF receives an equal dollar allocation on the first date.
    No rebalancing is performed during the period.
    """

    price_wide = (
        prices.pivot(
            index="date",
            columns="ticker",
            values="adjclose",
        )
        .sort_index()
    )

    if price_wide.isna().any().any():
        raise DataDownloadError(
            "Missing adjusted-close values found after pivoting prices."
        )

    ticker_count = len(price_wide.columns)

    allocation_per_etf = (
        initial_portfolio_value / ticker_count
    )

    # Normalize every ETF to 1.0 on the first date.
    normalized_prices = (
        price_wide / price_wide.iloc[0]
    )

    # Each ETF starts with the same dollar allocation.
    position_values = (
        normalized_prices * allocation_per_etf
    )

    portfolio_value = position_values.sum(axis=1)

    portfolio = pd.DataFrame(
        {
            "date": portfolio_value.index,
            "portfolio_value": portfolio_value.values,
        }
    )

    portfolio["daily_return"] = (
        portfolio["portfolio_value"]
        .pct_change(fill_method=None)
    )

    portfolio["cumulative_return"] = (
        portfolio["portfolio_value"]
        / initial_portfolio_value
        - 1
    )

    return portfolio

# --------------------------------------------------------------------
# ORCHESTRATION
# --------------------------------------------------------------------

def download_universe(
    tickers: list[str],
    start_date: str,
    end_date: str,
    api_key: str | None,
    raw_dir: Path,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """
    Download, save and clean every ticker. One bad ticker does not stop the
    run; failures are collected and returned for reporting.
    """

    frames: list[pd.DataFrame] = []
    failures: dict[str, str] = {}

    with requests.Session() as session:
        for i, ticker in enumerate(tickers):
            if i > 0:
                time.sleep(REQUEST_PAUSE_SECONDS)

            try:
                raw_text = fetch_tiingo_csv(session, ticker, start_date, end_date, api_key)
                csv_text = check_tiingo_response(raw_text, ticker)
                save_raw_response(csv_text, ticker, raw_dir)
                clean = clean_price_data(csv_text, ticker)
            except DataDownloadError as exc:
                logger.error(str(exc))
                failures[ticker] = str(exc)
                continue

            frames.append(clean)
            logger.info(
                "%-4s %5d rows  %s to %s",
                ticker,
                len(clean),
                clean["date"].min().date(),
                clean["date"].max().date(),
            )

    prices = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return prices, failures


def write_run_metadata(
    path: Path,
    tickers: list[str],
    prices: pd.DataFrame,
    failures: dict[str, str],
) -> None:
    """Record what this run pulled, so results can be reproduced and audited."""

    succeeded = sorted(prices["ticker"].unique().tolist()) if not prices.empty else []

    metadata = {
        "run_id": RUN_ID,
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Tiingo End-of-Day daily prices",
        "requested_start": START_DATE,
        "requested_end": END_DATE,
        "extraction_date": EXTRACTION_DATE_STR,
        "raw_data_dir": str(RAW_RUN_DIR.relative_to(PROJECT_ROOT)),
        "tickers_requested": tickers,
        "tickers_succeeded": succeeded,
        "tickers_failed": failures,
        "row_count": int(len(prices)),
        "price_adjustment_note": (
            "Tiingo provides both raw and adjusted price fields. "
            "The current processed dataset retains raw OHLCV only; "
            "adjusted fields will be evaluated before total-return calculations."
),
    }
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
def main() -> int:
    for directory in (RAW_RUN_DIR, PROCESSED_DATA_DIR, RUN_METADATA_DIR, OUTPUT_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    try:
        universe = load_etf_universe(ETF_UNIVERSE_FILE, EXPECTED_ETF_COUNT)
    except UniverseValidationError as exc:
        logger.error("Universe validation failed: %s", exc)
        return 1

    logger.info(
        "ETF universe loaded: %d ETFs, total weight %.2f%%",
        len(universe),
        universe["target_weight"].sum() * 100,
    )
    print(
        "\n"
        + universe[["ticker", "asset_class", "portfolio_role", "target_weight"]]
        .to_string(index=False)
        + "\n"
    )

    if not TIINGO_API_KEY:
        logger.error(
            "TIINGO_API_KEY is not set. "
            "Export the API key before running the pipeline."
        )
        return 1

    tickers = universe["ticker"].tolist()
    logger.info("Downloading %s to %s for %d tickers", START_DATE, END_DATE, len(tickers))

    prices, failures = download_universe(
        tickers, START_DATE, END_DATE, TIINGO_API_KEY, RAW_RUN_DIR
    )

    if not prices.empty:
        prices.to_csv(PROCESSED_PRICES_FILE, index=False, date_format="%Y-%m-%d")
        logger.info("Saved %d rows to %s", len(prices), PROCESSED_PRICES_FILE)

    
    write_run_metadata(RUN_METADATA_FILE, tickers, prices, failures)
    logger.info("Run metadata written to %s", RUN_METADATA_FILE)

    if failures:
        logger.error("%d of %d tickers failed: %s", len(failures), len(tickers), sorted(failures))
        return 1

    daily_returns = calculate_daily_returns(prices)
    
    daily_returns.to_csv(
        DAILY_RETURNS_FILE,
        index=False,
            date_format="%Y-%m-%d",
    )
    
    logger.info(
        "Saved %d ETF return records to %s",
        len(daily_returns),
        DAILY_RETURNS_FILE,
    )
    
    
    portfolio = calculate_equal_weight_portfolio(
        prices,
        INITIAL_PORTFOLIO_VALUE,
    )
    
    portfolio.to_csv(
        PORTFOLIO_GROWTH_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )
    
    logger.info(
        "Saved portfolio growth to %s",
        PORTFOLIO_GROWTH_FILE,
    )

    logger.info("All %d tickers downloaded successfully.", len(tickers))
    return 0


if __name__ == "__main__":
    sys.exit(main())