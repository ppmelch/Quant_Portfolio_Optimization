import numpy as np
import pandas as pd
from scipy.optimize import minimize


class OptimizePortfolioWeights():
    """
    Portfolio optimization class using different risk–return criteria.

    This class provides several portfolio optimization methods based on
    classical and downside-risk measures, assuming long-only portfolios
    with fully invested constraints.

    Parameters
    ----------
    returns : pd.DataFrame
        Asset returns with shape (T, N), where T is the number of periods
        and N is the number of assets.
    risk_free : float
        Annual risk-free rate expressed in decimal form (e.g. 0.05 for 5%).

    Attributes
    ----------
    rets : pd.DataFrame
        Asset returns.
    cov : pd.DataFrame
        Sample covariance matrix of asset returns.
    rf : float
        Daily risk-free rate.
    n_stocks : int
        Number of assets in the portfolio.
    """

    def __init__(self, returns: pd.DataFrame, risk_free: float):
        """
        Initialize the portfolio optimizer.

        Parameters
        ----------
        returns : pd.DataFrame
            Asset returns with datetime index and asset tickers as columns.
        benchmark : pd.DataFrame
            Benchmark returns aligned with asset returns.
        risk_free : float
            Annual risk-free rate (decimal format).
        """

        self.rets = returns
        self.cov = returns.cov()
        self.rf = risk_free / 252
        self.n_stocks = len(returns.columns)

    # --------------------------------------------------
    # Minimum Variance Portfolio
    # --------------------------------------------------
    def opt_min_var(self):
        """
        Compute the minimum variance portfolio.

        Solves a quadratic optimization problem that minimizes portfolio
        variance subject to full investment and long-only constraints.

        Returns
        -------
        np.ndarray
            Optimal asset weights that minimize portfolio variance.
        """

        def var(w): return w.T @ self.cov @ w
        w0 = np.ones(self.n_stocks) / self.n_stocks
        bounds = [(0, 1)] * self.n_stocks
        def constraint(w): return sum(w) - 1

        result = minimize(
            fun=var,
            x0=w0,
            bounds=bounds,
            constraints={'fun': constraint, 'type': 'eq'},
            tol=1e-16
        )

        return result.x

    # --------------------------------------------------
    # Maximum Sharpe Ratio Portfolio
    # --------------------------------------------------
    def opt_max_sharpe(self):
        """
        Compute the maximum Sharpe ratio portfolio.

        Maximizes the Sharpe ratio by minimizing its negative value,
        assuming a daily risk-free rate and long-only constraints.

        Returns
        -------
        np.ndarray
            Optimal asset weights that maximize the Sharpe ratio.
        """

        rend = self.rets.mean()
        cov = self.cov
        rf = self.rf

        def sr(w): return -((np.dot(rend, w) - rf) /
                            ((w.reshape(-1, 1).T @ cov @ w) ** 0.5))

        result = minimize(
            sr,
            np.ones(len(self.rets.T)),
            bounds=[(0, None)] * len(self.rets.T),
            constraints={'fun': lambda w: sum(w) - 1, 'type': 'eq'},
            tol=1e-16
        )

        return result.x

    # --------------------------------------------------
    # Minimum Semivariance Portfolio
    # --------------------------------------------------
    def opt_min_semivar(self, rets_benchmark):
        """
        Compute the minimum semivariance portfolio.

        Minimizes downside risk relative to a benchmark by focusing only
        on negative deviations of asset returns.

        Parameters
        ----------
        rets_benchmark : pd.Series or pd.DataFrame
            Benchmark returns aligned with asset returns.

        Returns
        -------
        np.ndarray
            Optimal asset weights that minimize portfolio semivariance.
        """

        rets = self.rets.copy()
        corr = self.rets.corr()

        diffs = rets.sub(rets_benchmark, axis=0)
        below_zero_target = diffs[diffs < 0].fillna(0)

        target_downside = np.array(below_zero_target.std())
        target_semivariance = (
            target_downside.reshape(len(target_downside), 1)
            * target_downside
            * corr
        )

        def semivar(w): return w.T @ target_semivariance @ w

        w0 = np.ones(self.n_stocks) / self.n_stocks
        bounds = [(0, 1)] * self.n_stocks
        def constraint(w): return sum(w) - 1

        result = minimize(
            fun=semivar,
            x0=w0,
            bounds=bounds,
            constraints={'fun': constraint, 'type': 'eq'},
            tol=1e-16
        )

        return result.x

    # --------------------------------------------------
    # Maximum Omega Ratio Portfolio
    # --------------------------------------------------
    def opt_max_omega(self, rets_benchmark):
        """
        Compute the maximum Omega ratio portfolio.

        Maximizes the Omega ratio by comparing upside volatility to
        downside volatility relative to a benchmark.

        Parameters
        ----------
        rets_benchmark : pd.Series or pd.DataFrame
            Benchmark returns aligned with asset returns.

        Returns
        -------
        np.ndarray
            Optimal asset weights that maximize the Omega ratio.
        """

        rets = self.rets.copy()
        diffs = rets.sub(rets_benchmark, axis=0)

        below_zero_target = diffs[diffs < 0].fillna(0)
        above_zero_target = diffs[diffs > 0].fillna(0)

        target_downside = np.array(below_zero_target.std())
        target_upside = np.array(above_zero_target.std())

        omega_ratio = target_upside / target_downside
        def omega(w): return -sum(omega_ratio * w)

        w0 = np.ones(self.n_stocks) / self.n_stocks
        bounds = [(0.05, 0.5)] * self.n_stocks
        def constraint(w): return sum(w) - 1

        result = minimize(
            fun=omega,
            x0=w0,
            bounds=bounds,
            constraints={'fun': constraint, 'type': 'eq'},
            tol=1e-16
        )

        w = result.x
        w = w / w.sum()

        return w


class TacticalOptimizeWeights(OptimizePortfolioWeights):
    """
    Tactical portfolio optimization with exposure scaling.

    Extends OptimizePortfolioWeights by grouping optimization strategies
    and applying a tactical exposure factor.
    """

    def __init__(self, returns: pd.DataFrame, risk_free: float, exposure: float = 1.0):
        """
        Parameters
        ----------
        returns : pd.DataFrame
            Asset returns.
        risk_free : float
            Annual risk-free rate.
        exposure : float
            Fraction of capital allocated to tactical portfolio (0–1).
        """
        super().__init__(returns=returns, risk_free=risk_free)
        self.exposure = exposure

    def compute_weights(self):
        """
        Compute tactical portfolio weights using multiple optimization criteria.

        Returns
        -------
        pd.DataFrame
            Weights per strategy scaled by tactical exposure.
        """

        weights = pd.DataFrame({
            "Min_var": self.opt_min_var(),
            "Max_sharpe": self.opt_max_sharpe(),
            "Min_semivar": self.opt_min_semivar(self.rets.mean()),
            "Max_omega": self.opt_max_omega(self.rets.mean())
        }, index=self.rets.columns)

        return weights * self.exposure
