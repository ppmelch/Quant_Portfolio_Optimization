from core.analytics.metrics import Metrics
from core.portfolio.portfolio_construction import PortfolioConstruction


def build_portfolio(results, capital, portfolio_choice, benchmark_weight):
    
    weights = results["weights"][portfolio_choice]

    constructor = PortfolioConstruction(
        weights_strategy=weights,
        benchmark_weight=benchmark_weight
    )

    return {
        "combined_weights": constructor.combine(),
        "allocation": constructor.capital_allocation(capital),
        "shares": constructor.compute_shares(
            results["prices"],
            results["benchmark_prices"],
            capital
        ),
        "shares_df": constructor.shares_dataframe(
            results["prices"],
            results["benchmark_prices"],
            capital
        )
}

def compute_metrics(results, portfolio_choice, benchmark_weight):

    history_returns = results["backtest"].pct_change().dropna()

    portfolio_returns = history_returns[portfolio_choice]
    benchmark_returns = history_returns["Benchmark"]

    combined_returns = (
        (1 - benchmark_weight) * portfolio_returns +
        benchmark_weight * benchmark_returns
    )

    metrics = Metrics(
        returns=combined_returns.to_frame("Portfolio"),
        benchmark=benchmark_returns,
        rf=0.0375
    )

    return metrics.portfolio_metrics("Portfolio")