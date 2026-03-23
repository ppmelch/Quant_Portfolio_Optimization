import streamlit as st


def render_inputs():
    """
    Render the main dashboard input controls.

    Returns
    -------
    tuple
        A tuple containing:
        (raw_tickers, benchmark, interval, rebalancing_freq, capital, run_button)
    """
    raw_tickers = st.text_input(
        "Tickers (comma separated)",
        value="AVGO , GLD , V , TSM , LLY , AMT , VOO"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        benchmark = st.text_input("Benchmark", value="SPY")

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
            step=1,
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

    return raw_tickers, benchmark, interval, rebalancing_freq, capital, run_button


def render_layout(results, capital, viz, portfolio_data, stats):
    """
    Render the main dashboard layout with portfolio results.

    Parameters
    ----------
    results : dict
        Dictionary containing backtesting results and metrics.
    capital : float
        Total investment capital.
    viz : Visualization
        Visualization object used to generate plots.
    portfolio_data : dict
        Dictionary containing portfolio weights, allocation, shares, and selections.
    stats : dict
        Dictionary containing portfolio statistics (return, volatility, sharpe).
    """
    history = results["backtest"]
    asset_metrics = results["metrics"]

    combined_weights = portfolio_data["combined_weights"]
    allocation = portfolio_data["allocation"]
    shares = portfolio_data["shares"]
    shares_df = portfolio_data["shares_df"]

    portfolio_choice = portfolio_data["portfolio_choice"]

    st.subheader("Backtesting Performance")

    fig_backtest = viz.plot_backtesting(history, show=False)
    st.plotly_chart(fig_backtest, use_container_width=True,
                    config={"displayModeBar": False})

    st.markdown("---")

    st.subheader("Portfolio Selection")

    col1, col2 = st.columns(2)

    with col1:
        portfolio_choice = st.selectbox(
            "Choose Portfolio Strategy",
            ["Min_var", "Max_sharpe", "Min_semivar", "Max_omega"],
            key="portfolio_choice"
        )

    with col2:
        benchmark_weight = st.slider(
            "Benchmark Allocation",
            0.0,
            1.0,
            key="benchmark_weight",
            step=0.05
        )

    st.markdown("---")

    st.subheader("Portfolio Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Expected Return", f"{stats['return']:.2%}")
    col2.metric("Volatility", f"{stats['vol']:.2%}")
    col3.metric("Sharpe Ratio", f"{stats['sharpe']:.2f}")

    st.markdown("---")

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

        fig_weights = viz.plot_weights_pie(
            combined_weights,
            portfolio_choice,
            show=False
        )

        fig_weights.update_traces(textinfo="label+percent")

        st.plotly_chart(fig_weights, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Correlation Matrix")

        corr_matrix = results["correlation"]
        fig_corr = viz.corr_matrix(corr_matrix, show=False)

        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        st.subheader("Capital Allocation")

        fig_cap = viz.plot_weights_pie(
            allocation,
            portfolio_choice,
            show=False
        )

        fig_cap.update_traces(
            textinfo="label+value",
            hovertemplate="%{label}<br>$%{value:,.0f}<extra></extra>"
        )

        st.plotly_chart(fig_cap, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shares to Buy")
        st.dataframe(shares_df)

    with col2:
        fig_qty = viz.plot_weights_pie(
            shares,
            portfolio_choice,
            show=False
        )

        fig_qty.update_traces(
            textinfo="label+value",
            hovertemplate="%{label}<br>%{value:.0f} shares<extra></extra>"
        )

        st.plotly_chart(fig_qty, use_container_width=True)

    st.markdown("---")

    st.subheader("Strategies Statistics")
    st.dataframe(asset_metrics)
