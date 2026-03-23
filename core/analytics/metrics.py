import numpy as np
import pandas as pd

class Metrics():
    """Class to compute portfolio performance metrics"""

    def __init__(self, returns: pd.DataFrame, benchmark: pd.Series, rf: float):

        if returns.empty:
            raise ValueError("Returns can't be empty")

        self.returns = returns
        self.benchmark = benchmark
        self.rf = rf

    # -----------------------------
    # RETURNS
    # -----------------------------

    def anual_rets(self) -> pd.Series:
        return self.returns.mean() * 252 

    # -----------------------------
    # VOLATILITY
    # -----------------------------

    def anual_vol(self) -> pd.Series:
        return self.returns.std() * np.sqrt(252) 

    # -----------------------------
    # SHARPE
    # -----------------------------

    def sharpe_ratio(self) -> pd.Series:

        r_p = self.anual_rets()
        vol = self.anual_vol()

        return (r_p - self.rf) / vol

    # -----------------------------
    # DOWNSIDE / UPSIDE
    # -----------------------------

    def downside_risk(self) -> pd.Series:

        downside = self.returns[self.returns < 0].std() * np.sqrt(252)

        return downside

    def upside_risk(self) -> pd.Series:

        upside = self.returns[self.returns > 0].std() * np.sqrt(252)

        return upside

    # -----------------------------
    # OMEGA
    # -----------------------------

    def omega_ratio(self) -> pd.Series:

        return self.upside_risk() / self.downside_risk()

    # -----------------------------
    # MAX DRAWDOWN
    # -----------------------------

    def max_drawdown(self) -> pd.Series:

        cumulative = (1 + self.returns).cumprod()

        rolling_max = cumulative.cummax()

        drawdown = (cumulative - rolling_max) / rolling_max

        return drawdown.min()

    # -----------------------------
    # BETA
    # -----------------------------

    def beta(self) -> pd.Series:

        cov = self.returns.apply(lambda x: x.cov(self.benchmark))

        var_market = self.benchmark.var()

        return cov / var_market

    # -----------------------------
    # JENSEN ALPHA
    # -----------------------------

    def alpha_jensen(self) -> pd.Series:

        r_p = self.anual_rets()

        r_m = self.benchmark.mean() * 252 

        beta = self.beta()

        return r_p - (self.rf + beta * (r_m - self.rf))

    # -----------------------------
    # TREYNOR
    # -----------------------------

    def ratio_treynor(self) -> pd.Series:

        r_p = self.anual_rets()

        beta = self.beta()

        return (r_p - self.rf) / beta

    # -----------------------------
    # SORTINO
    # -----------------------------

    def ratio_sortino(self) -> pd.Series:

        r_p = self.anual_rets()

        downside = self.downside_risk()

        return (r_p - self.rf) / downside

    # -----------------------------
    # SUMMARY
    # -----------------------------

    def summary(self) -> pd.DataFrame:

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

        return {
            "return": self.anual_rets()[portfolio_name],
            "vol": self.anual_vol()[portfolio_name],
            "sharpe": self.sharpe_ratio()[portfolio_name]
        }
    
        
    
        
    
        
    