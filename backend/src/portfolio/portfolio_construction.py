import pandas as pd

class PortfolioConstruction:

    def __init__(self, weights_strategy, benchmark_weight):

        self.weights_strategy = weights_strategy
        self.benchmark_weight = benchmark_weight
        self.strategy_weight = 1 - benchmark_weight

    def combine(self):

        w = self.weights_strategy * self.strategy_weight

        weights = dict(w)

        weights["Benchmark"] = self.benchmark_weight

        return pd.Series(weights)
    
    def portfolio_returns(self, asset_returns, benchmark_returns):

        strategy_returns = asset_returns @ self.weights_strategy

        combined_returns = (
            self.strategy_weight * strategy_returns
            + self.benchmark_weight * benchmark_returns
        )

        return combined_returns