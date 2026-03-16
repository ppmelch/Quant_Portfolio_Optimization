import pandas as pd
from src.backend.optimization.optimization import OptimizePortfolioWeights

class dynamic_backtesting:
    """
    Dynamic backtesting framework combining tactical and strategic portfolios.

    This class performs a rolling-window backtest where tactical portfolio
    weights are periodically re-optimized using different optimization
    criteria, while strategic weights remain fixed. Both portfolios are
    combined and evaluated against a benchmark.

    Parameters
    ----------
    prices_tactical : pd.DataFrame
        Price series of tactical assets with datetime index.
    prices_strategic : pd.DataFrame
        Price series of strategic assets with datetime index.
    prices_benchmark : pd.DataFrame
        Price series of the benchmark asset(s).
    capital : float
        Initial investment capital.
    rf : float
        Annual risk-free rate expressed in decimal form.
    months : int
        Rebalancing frequency in months.
    """

    def __init__(self, prices_tactical, prices_strategic, prices_benchmark, capital, rf, months):
        """
        Initialize the dynamic backtesting object.

        Stores price data for tactical, strategic and benchmark assets,
        as well as capital and rebalancing configuration.
        """

        self.prices_tactical = prices_tactical
        self.prices_strategic = prices_strategic
        self.prices_benchmark = prices_benchmark
        self.capital = capital
        self.rf = rf
        self.months = months

    # --------------------------------------------------
    # Optimization step
    # --------------------------------------------------
    def optimize_weights(self, prices: pd.DataFrame, n_days: int, periods: int):
        """
        Optimize portfolio weights for a given rolling window.

        Extracts a time window of price data, computes returns, and
        applies multiple portfolio optimization techniques.

        Parameters
        ----------
        prices : pd.DataFrame
            Price series used for optimization.
        n_days : int
            Number of trading days per optimization window.
        periods : int
            Index of the rolling period.

        Returns
        -------
        tuple of pd.Series
            Optimized weights for:
            (minimum variance, maximum Sharpe, minimum semivariance, maximum Omega).
        """

        start = int(n_days * periods)
        end = int(n_days * (periods + 1))

        temp_data = prices.iloc[start:end, :]
        temp_bench = self.prices_benchmark.iloc[start:end]

        temp_rets = temp_data.pct_change().dropna()
        rets_benchmark = temp_bench.pct_change().dropna()

        optimizer = OptimizePortfolioWeights(
            returns=temp_rets,
            risk_free=self.rf
        )

        w_minvar = pd.Series(optimizer.opt_min_var(), index=prices.columns)
        w_sharpe = pd.Series(optimizer.opt_max_sharpe(), index=prices.columns)
        w_semivar = pd.Series(
            optimizer.opt_min_semivar(rets_benchmark),
            index=prices.columns
        )
        w_omega = pd.Series(
            optimizer.opt_max_omega(rets_benchmark),
            index=prices.columns
        )

        return w_minvar, w_sharpe, w_semivar, w_omega

    # --------------------------------------------------
    # Backtesting simulation
    # --------------------------------------------------
    def simulation(self):
        """
        Run the dynamic backtesting simulation.

        Performs a rolling backtest where tactical portfolio weights are
        periodically re-optimized, combined with fixed strategic weights,
        and evaluated against a benchmark.

        Returns
        -------
        pd.DataFrame
            Time series of cumulative portfolio values for each optimization
            strategy and the benchmark.
        """

        total_days = len(self.prices_tactical)
        n_periods = round(total_days / 252 * (12 / self.months))
        n_days = round(total_days / n_periods)

        capital = self.capital

        # Initial optimization window
        opt_data = self.prices_tactical.iloc[:n_days, :]
        backtesting_tactical = self.prices_tactical.iloc[n_days:, :]
        backtesting_strategic = self.prices_strategic.iloc[n_days:, :]
        backtesting_benchmark = self.prices_benchmark.iloc[n_days:]

        rets_tactical = backtesting_tactical.pct_change().dropna()
        rets_strategic = backtesting_strategic.pct_change().dropna()
        rets_benchmark = backtesting_benchmark.pct_change().dropna()

        min_len = min(len(rets_tactical), len(rets_strategic), len(rets_benchmark))
        rets_tactical = rets_tactical.iloc[:min_len, :]
        rets_strategic = rets_strategic.iloc[:min_len, :]
        rets_benchmark = rets_benchmark.iloc[:min_len]

        # Capital paths
        minvar, sharpe, semivar, omega = [capital], [capital], [capital], [capital]
        day_counter, periods_counter = 0, 0

        # Initial weights
        w_minvar, w_sharpe, w_semivar, w_omega = self.optimize_weights(
            opt_data, n_days, 0
        )

        # Fixed strategic weights (equal-weighted)
        w_strategic = pd.Series(
            [1 / self.prices_strategic.shape[1]] * self.prices_strategic.shape[1],
            index=self.prices_strategic.columns
        )

        for day in range(min_len - 1):
            if day_counter == n_days:
                w_minvar, w_sharpe, w_semivar, w_omega = self.optimize_weights(
                    backtesting_tactical, n_days, periods_counter
                )
                periods_counter += 1
                day_counter = 0

            combined_minvar = w_minvar.add(w_strategic, fill_value=0)
            combined_sharpe = w_sharpe.add(w_strategic, fill_value=0)
            combined_semivar = w_semivar.add(w_strategic, fill_value=0)
            combined_omega = w_omega.add(w_strategic, fill_value=0)

            combined_minvar /= combined_minvar.sum()
            combined_sharpe /= combined_sharpe.sum()
            combined_semivar /= combined_semivar.sum()
            combined_omega /= combined_omega.sum()

            rets_combined = pd.concat([
                rets_tactical.iloc[day, :],
                rets_strategic.iloc[day, :]
            ])

            rets_combined = rets_combined.groupby(level=0).mean()
            # alinear índices
            rets_combined = rets_combined.reindex(combined_minvar.index).fillna(0)

            minvar.append(minvar[-1] * (1 + (rets_combined @ combined_minvar)))
            sharpe.append(sharpe[-1] * (1 + (rets_combined @ combined_sharpe)))
            semivar.append(semivar[-1] * (1 + (rets_combined @ combined_semivar)))
            omega.append(omega[-1] * (1 + (rets_combined @ combined_omega)))
            
            day_counter += 1

        # Benchmark cumulative capital
        capital_benchmark = capital * (1 + rets_benchmark).cumprod()
        capital_benchmark = capital_benchmark.iloc[:len(minvar) - 1]

        df = pd.DataFrame({
            'Date': backtesting_tactical.index[:len(minvar) - 1],
            'Min_var': minvar[:-1],
            'Max_sharpe': sharpe[:-1],
            'Min_semivar': semivar[:-1],
            'Max_omega': omega[:-1],
            'Benchmark': capital_benchmark.values
        }).set_index('Date')

        return df
