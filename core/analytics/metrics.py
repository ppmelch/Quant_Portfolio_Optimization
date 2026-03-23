import numpy as np
import pandas as pd


class Metrics:
    """
    Compute portfolio performance metrics based on asset returns and a benchmark.
    """

    def __init__(self, returns: pd.DataFrame, benchmark: pd.Series, rf: float):
        """
        Initialize the Metrics class.

        Parameters
        ----------
        returns : pd.DataFrame
            DataFrame of asset or portfolio returns.
        benchmark : pd.Series
            Benchmark return series.
        rf : float
            Risk-free rate.
        """
        if returns.empty:
            raise ValueError("Returns can't be empty")

        self.returns = returns
        self.benchmark = benchmark
        self.rf = rf

    def anual_rets(self) -> pd.Series:
        """
        Compute annualized returns.

        Returns
        -------
        pd.Series
        """
        return self.returns.mean() * 252

    def anual_vol(self) -> pd.Series:
        """
        Compute annualized volatility.

        Returns
        -------
        pd.Series
        """
        return self.returns.std() * np.sqrt(252)

    def sharpe_ratio(self) -> pd.Series:
        """
        Compute Sharpe ratio.

        Returns
        -------
        pd.Series
        """
        r_p = self.anual_rets()
        vol = self.anual_vol()
        return (r_p - self.rf) / vol

    def downside_risk(self) -> pd.Series:
        """
        Compute downside risk.

        Returns
        -------
        pd.Series
        """
        return self.returns[self.returns < 0].std() * np.sqrt(252)

    def upside_risk(self) -> pd.Series:
        """
        Compute upside risk.

        Returns
        -------
        pd.Series
        """
        return self.returns[self.returns > 0].std() * np.sqrt(252)

    def omega_ratio(self) -> pd.Series:
        """
        Compute Omega ratio.

        Returns
        -------
        pd.Series
        """
        return self.upside_risk() / self.downside_risk()

    def max_drawdown(self) -> pd.Series:
        """
        Compute maximum drawdown.

        Returns
        -------
        pd.Series
        """
        cumulative = (1 + self.returns).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        return drawdown.min()

    def beta(self) -> pd.Series:
        """
        Compute portfolio beta relative to the benchmark.

        Returns
        -------
        pd.Series
        """
        cov = self.returns.apply(lambda x: x.cov(self.benchmark))
        var_market = self.benchmark.var()
        return cov / var_market

    def alpha_jensen(self) -> pd.Series:
        """
        Compute Jensen's alpha.

        Returns
        -------
        pd.Series
        """
        r_p = self.anual_rets()
        r_m = self.benchmark.mean() * 252
        beta = self.beta()
        return r_p - (self.rf + beta * (r_m - self.rf))

    def ratio_treynor(self) -> pd.Series:
        """
        Compute Treynor ratio.

        Returns
        -------
        pd.Series
        """
        r_p = self.anual_rets()
        beta = self.beta()
        return (r_p - self.rf) / beta

    def ratio_sortino(self) -> pd.Series:
        """
        Compute Sortino ratio.

        Returns
        -------
        pd.Series
        """
        r_p = self.anual_rets()
        downside = self.downside_risk()
        return (r_p - self.rf) / downside

    def summary(self) -> pd.DataFrame:
        """
        Generate a summary table of portfolio metrics.

        Returns
        -------
        pd.DataFrame
        """
        summary_df = pd.DataFrame({
            'Annual Rend': self.anual_rets(),
            'Annual Vol': self.anual_vol(),
            'Sharpe R': self.sharpe_ratio(),
            'Beta': self.beta(),
            'Downside Risk': self.downside_risk(),
            'Upside Risk': self.upside_risk(),
            'Max Drawdown': self.max_drawdown(),
            'Omega R': self.omega_ratio(),
            'Sortino R': self.ratio_sortino(),
            'Treynor R': self.ratio_treynor(),
            'Alpha Jensen': self.alpha_jensen(),
            'Calmar R': self.anual_rets() / abs(self.max_drawdown())
        })

        return summary_df.T.round(4)

    def portfolio_metrics(self, portfolio_name):
        """
        Extract key metrics for a specific portfolio.

        Parameters
        ----------
        portfolio_name : str

        Returns
        -------
        dict
        """
        return {
            "return": self.anual_rets()[portfolio_name],
            "vol": self.anual_vol()[portfolio_name],
            "sharpe": self.sharpe_ratio()[portfolio_name]
        }
