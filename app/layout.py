import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def render_inputs():

    raw_tickers = st.text_input(
        "Tickers (comma separated)",
        value="AVGO , GLD , V , TSM , LLY , AMT , VOO"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        benchmark = st.text_input(
            "Benchmark",
            value="SPY"
        )

    with col2:
        interval = st.selectbox(
            "Data Interval",
            ["6m", "1y", "2y", "5y", "10y"]
        )
        
    with col3: 
        rebalancing_freq = st.number_input(
            "Rebalancing Frequency (months)",
            min_value=1,
            value=3,
            step=1
        )

    with col4:
        capital = st.number_input(
            "Capital to invest ($)",
            min_value=1000,
            value=1_000_000,
            step=100_000
        )

    with col5:
        st.write("")
        st.write("")
        run_button = st.button("Run", type="primary")

    return raw_tickers, benchmark, interval, capital, run_button , rebalancing_freq

def render_layout(results, capital, viz):

    prices = results["prices"]
    returns = results["returns"]
    history = results["backtest"]
    weights = results["weights"]
    asset_metrics = results["metrics"]

    # -------------------------
    # BACKTEST
    # -------------------------

    st.subheader("Backtesting Performance")

    fig_backtest = px.line(
        history,
        x=history.index,
        y=history.columns,
        title="Portfolio Backtest"
    )

    st.plotly_chart(fig_backtest, use_container_width=True, key="backtest_all")

    st.markdown("---")

    # -------------------------
    # PORTFOLIO SELECTOR
    # -------------------------

    st.subheader("Portfolio Selection")

    col1, col2 = st.columns(2)

    with col1:
        portfolio_choice = st.selectbox(
            "Choose Portfolio Strategy",
            ["Min_var", "Max_sharpe", "Min_semivar", "Max_omega"]
        )

    with col2:
        benchmark_weight = st.slider(
            "Benchmark Allocation",
            0.0,
            1.0,
            0.50,
            step=0.05
        )

    strategy_map = {
        "Min_var": "Min_var",
        "Max_sharpe": "Max_sharpe",
        "Min_semivar": "Min_semivar",
        "Max_omega": "Max_omega"
    }

    selected_weights = weights[strategy_map[portfolio_choice]]

    # -------------------------
    # PORTFOLIO METRICS
    # -------------------------

    st.subheader("Portfolio Metrics")

    combined_history = (
        (1 - benchmark_weight) * history[portfolio_choice] +
        benchmark_weight * history["Benchmark"]
    )

    combined_returns = combined_history.pct_change().dropna()

    expected_return = combined_returns.mean() * 252
    volatility = combined_returns.std() * np.sqrt(252)

    rf = 0.0375
    sharpe = (expected_return - rf) / volatility

    col1, col2, col3 = st.columns(3)

    col1.metric("Expected Return", f"{expected_return:.2%}")
    col2.metric("Volatility", f"{volatility:.2%}")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

    st.markdown("---")

    # -------------------------
    # PORTFOLIO WEIGHTS
    # -------------------------

    portfolio_weight = 1 - benchmark_weight

    combined_weights = selected_weights * portfolio_weight
    combined_weights["Benchmark"] = benchmark_weight

    allocation = combined_weights * capital

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Selected Strategy Backtest")

        fig_strategy = viz.plot_backtesting_strategy(
            history,
            portfolio_choice,
            show=False
        )

        st.plotly_chart(fig_strategy, use_container_width=True)

    with col2:

        st.subheader("Portfolio Weights")

        fig_weights = px.pie(
            values=combined_weights.values,
            names=combined_weights.index
        )

        fig_weights.update_traces(textinfo="label+percent")

        st.plotly_chart(fig_weights, use_container_width=True)

    # -------------------------
    # CORRELATION + CAPITAL
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Correlation Matrix")

        returns_with_benchmark = returns.copy()
        returns_with_benchmark["Benchmark"] = history["Benchmark"].pct_change()

        corr_matrix = returns_with_benchmark.corr()

        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale="RdBu_r"
        )

        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:

        st.subheader("Capital Allocation")

        fig_cap = px.pie(
            names=allocation.index,
            values=allocation.values
        )

        fig_cap.update_traces(
            textinfo="label+value",
            hovertemplate="%{label}<br>$%{value:,.0f}<extra></extra>"
        )

        st.plotly_chart(fig_cap, use_container_width=True)

    # -------------------------
    # SHARES
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Shares to Buy")

        latest_prices = prices.iloc[-1].copy()

        benchmark_price = results["benchmark_prices"].iloc[-1]

        latest_prices["Benchmark"] = benchmark_price

        shares = (allocation / latest_prices).round().astype(int)

        shares_df = pd.DataFrame({
            "Price": latest_prices,
            "Weight": combined_weights,
            "Capital": allocation,
            "Shares": shares
        })

        st.dataframe(shares_df)

    with col2:

        fig_qty = px.pie(
            names=shares.index,
            values=shares.values,
            title="Number of Shares"
        )

        fig_qty.update_traces(
            textinfo="label+value",
            hovertemplate="%{label}<br>%{value:.0f} shares<extra></extra>"
        )

        st.plotly_chart(fig_qty, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # ASSET STATS
    # -------------------------

    st.subheader("Asset Statistics")

    st.dataframe(asset_metrics)