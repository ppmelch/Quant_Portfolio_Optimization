import pandas as pd


class PortfolioConstruction:
    """
    Construct and manage portfolio allocation combining strategy weights and benchmark exposure.
    """

    def __init__(self, weights_strategy, benchmark_weight):
        """
        Initialize portfolio construction.

        Parameters
        ----------
        weights_strategy : pd.Series
            Weights of the selected portfolio strategy.
        benchmark_weight : float
            Proportion of capital allocated to the benchmark.
        """
        self.weights_strategy = weights_strategy
        self.benchmark_weight = benchmark_weight
        self.strategy_weight = 1 - benchmark_weight

    def combine(self):
        """
        Combine strategy weights with benchmark allocation.

        Returns
        -------
        pd.Series
            Final portfolio weights including benchmark.
        """
        w = self.weights_strategy * self.strategy_weight
        weights = dict(w)
        weights["Benchmark"] = self.benchmark_weight
        return pd.Series(weights)

    def portfolio_returns(self, asset_returns, benchmark_returns):
        """
        Compute combined portfolio returns.

        Parameters
        ----------
        asset_returns : pd.DataFrame
            Returns of portfolio assets.
        benchmark_returns : pd.Series
            Benchmark returns.

        Returns
        -------
        pd.Series
        """
        strategy_returns = asset_returns @ self.weights_strategy

        combined_returns = (
            self.strategy_weight * strategy_returns
            + self.benchmark_weight * benchmark_returns
        )

        return combined_returns

    def capital_allocation(self, capital):
        """
        Compute capital allocation across assets.

        Parameters
        ----------
        capital : float
            Total investment capital.

        Returns
        -------
        pd.Series
        """
        combined_weights = self.combine()
        allocation = combined_weights * capital
        return allocation

    def compute_shares(self, prices, benchmark_prices, capital):
        """
        Compute number of shares to purchase for each asset.

        Parameters
        ----------
        prices : pd.DataFrame
            Historical asset prices.
        benchmark_prices : pd.Series
            Benchmark price series.
        capital : float
            Total investment capital.

        Returns
        -------
        pd.Series
        """
        latest_prices = prices.iloc[-1].copy()
        benchmark_price = benchmark_prices.iloc[-1]

        latest_prices["Benchmark"] = benchmark_price

        allocation = self.capital_allocation(capital)
        shares = (allocation / latest_prices).round().astype(int)

        return shares

    def shares_dataframe(self, prices, benchmark_prices, capital):
        """
        Generate a detailed DataFrame with prices, weights, capital allocation, and shares.

        Parameters
        ----------
        prices : pd.DataFrame
        benchmark_prices : pd.Series
        capital : float

        Returns
        -------
        pd.DataFrame
        """
        latest_prices = prices.iloc[-1].copy()
        latest_prices["Benchmark"] = benchmark_prices.iloc[-1]

        weights = self.combine()
        allocation = self.capital_allocation(capital)
        shares = self.compute_shares(prices, benchmark_prices, capital)

        shares_df = pd.DataFrame({
            "Price": latest_prices,
            "Weight": weights,
            "Capital": allocation,
            "Shares": shares
        })

        return shares_df
