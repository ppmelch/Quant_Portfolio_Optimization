import pandas as pd
from backend.src.data.financial_statements import Financial
from backend.src.optimization.optimization import OptimizePortfolioWeights
from backend.src.backtesting.backtest import dynamic_backtesting
from backend.src.analytics.metrics import Metrics
from backend.src.portfolio.portfolio_construction import PortfolioConstruction

def run_pipeline(
    tickers: list,
    benchmark: str,
    interval: str = "5y",
    capital: float = 1000000,
    risk_free_rate: float = 0.0375,
    rebalancing_freq: int = 3,
    strategy: str = "Min_var",
    benchmark_weight: float = 0.0
):

    financial = Financial(
        assets=tickers,
        benchmark=benchmark,
        interval=interval
    )

    prices, benchmark_prices = financial.clean_data()


    returns = prices.pct_change().dropna()
    benchmark_returns = benchmark_prices.pct_change().dropna()


    corr_matrix = returns.corr()


    optimizer = OptimizePortfolioWeights(
        returns=returns,
        risk_free=risk_free_rate
    )

    weights = {
        "Min_var": pd.Series(optimizer.opt_min_var(), index=returns.columns),
        "Max_sharpe": pd.Series(optimizer.opt_max_sharpe(), index=returns.columns),
        "Min_semivar": pd.Series(optimizer.opt_min_semivar(benchmark_returns), index=returns.columns),
        "Max_omega": pd.Series(optimizer.opt_max_omega(benchmark_returns), index=returns.columns)
    }

    strategy_weights = pd.Series(
        weights[strategy],
        index=returns.columns
    )


    constructor = PortfolioConstruction(
        weights_strategy=strategy_weights,
        benchmark_weight=benchmark_weight
    )

    final_weights = constructor.combine()

    backtest = dynamic_backtesting(
        prices_tactical=prices,
        prices_strategic=prices,
        prices_benchmark=benchmark_prices,
        capital=capital,
        rf=risk_free_rate,
        months=rebalancing_freq
    )

    history = backtest.simulation()

    history_returns = history.pct_change().dropna()

    metrics = Metrics(
        returns=history_returns,
        benchmark=history_returns["Benchmark"],
        rf=risk_free_rate
    )

    metrics_table = metrics.summary()

    results = {
        "prices": prices,
        "benchmark_prices": benchmark_prices,
        "returns": returns,
        "backtest": history,
        "weights": weights,
        "correlation": corr_matrix,
        "metrics": metrics_table,
        "final_weights": final_weights
    }
    return results