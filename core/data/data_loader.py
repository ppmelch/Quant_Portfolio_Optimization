import re
import time
import pandas as pd
import datetime as dt
import yfinance as yf
from matplotlib.dates import relativedelta as rd


class Financial:
    """
    Handle financial data retrieval and preprocessing.
    """

    def __init__(self, assets, benchmark=None, interval: str = "5y"):
        """
        Initialize financial data handler.

        Parameters
        ----------
        assets : list or str
        benchmark : str, optional
        interval : str
        """
        self.assets = self._format_assets(assets)
        self.benchmark = benchmark.upper() if benchmark else None
        self.interval = interval
        self.start, self.end = self._parse_interval()

    def _format_assets(self, assets):
        """
        Format and clean asset tickers.

        Returns
        -------
        list
        """
        if isinstance(assets, str):
            assets = [assets]

        return [t.strip().upper() for t in assets if isinstance(t, str) and t.strip()]

    def _parse_interval(self):
        """
        Parse interval string into start and end dates.

        Returns
        -------
        tuple
        """
        m = re.match(r"^\s*(\d+)\s*([dwmy])\s*$", self.interval.lower())
        if not m:
            raise ValueError(
                "Interval must follow '<int><unit>' with units in {d,w,m,y}")

        n, u = m.groups()
        delta = {"d": "days", "w": "weeks", "m": "months", "y": "years"}[u]

        start = dt.date.today() - rd(**{delta: int(n)})
        end = dt.date.today() + dt.timedelta(days=1)

        return start, end

    def _download_single(self, ticker, pause=1.2, retries=3):
        """
        Download a single ticker with retry logic.

        Returns
        -------
        pd.DataFrame or None
        """
        for _ in range(retries):
            try:
                df = yf.download(
                    ticker,
                    start=self.start,
                    end=self.end,
                    interval="1d",
                    progress=False,
                    auto_adjust=False,
                    threads=False
                )

                if df is None or df.empty:
                    return None

                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                if "Close" not in df.columns or df["Close"].isna().all():
                    if "Adj Close" in df.columns:
                        df["Close"] = df["Adj Close"]
                    elif all(c in df.columns for c in ["Open", "High", "Low"]):
                        df["Close"] = df[["Open", "High", "Low"]].mean(axis=1)

                df = df[["Close"]].dropna()

                if not df.empty:
                    return df.rename(columns={"Close": ticker})

            except Exception:
                time.sleep(2)

        return None

    def clean_data(self):
        """
        Download and align asset and benchmark data.

        Returns
        -------
        tuple
            (prices, benchmark_prices)
        """
        data = {}

        for ticker in self.assets:
            df = self._download_single(ticker)
            if df is not None:
                data[ticker] = df
            time.sleep(1.5)

        if not data:
            raise ValueError("No valid assets downloaded.")

        prices = pd.concat(data.values(), axis=1)
        prices.index.name = "Date"
        prices.sort_index(inplace=True)
        prices.dropna(how="any", inplace=True)

        benchmark_prices = None

        if self.benchmark:
            bench_df = self._download_single(self.benchmark)

            if bench_df is not None:
                benchmark_prices = bench_df.iloc[:, 0]
                common_idx = prices.index.intersection(benchmark_prices.index)
                prices = prices.loc[common_idx]
                benchmark_prices = benchmark_prices.loc[common_idx]

        return prices, benchmark_prices
