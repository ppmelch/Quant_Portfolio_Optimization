import pathlib
import streamlit as st
import plotly.express as px
from backend.src.portfolio.portfolio_construction import PortfolioConstruction


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
            step=1 , 
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
        run_button = st.button("Run", type="primary" )

    return raw_tickers, benchmark, interval, rebalancing_freq, capital, run_button

def render_layout(results, capital, viz):

    prices = results["prices"]
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

    st.plotly_chart(fig_backtest, use_container_width=True)

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
    
    constructor = PortfolioConstruction(weights_strategy=selected_weights, benchmark_weight=benchmark_weight)
  
    # -------------------------
    # PORTFOLIO METRICS
    # -------------------------

    st.subheader("Portfolio Metrics")
    
    metrics = results["metrics_object"] 
    portfolio_stats = metrics.portfolio_metrics(portfolio_choice)
    
    col1, col2, col3 = st.columns(3)

    col1.metric("Expected Return", f"{portfolio_stats['return']:.2%}")
    col2.metric("Volatility", f"{portfolio_stats['vol']:.2%}")
    col3.metric("Sharpe Ratio", f"{portfolio_stats['sharpe']:.2f}")

    st.markdown("---")

    # -------------------------
    # PORTFOLIO WEIGHTS
    # -------------------------
    
    combined_weights = constructor.combine()


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
            combined_weights.to_frame("Weights"),
            "Weights",
            show=False
        )

        fig_weights.update_traces(textinfo="label+percent")

        st.plotly_chart(fig_weights, use_container_width=True)
        

    # -------------------------
    # CORRELATION + CAPITAL
    # -------------------------
    allocation = constructor.capital_allocation(capital)



    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Correlation Matrix")
        
        corr_matrix = results["correlation"]
        
        fig_corr = viz.corr_matrix(corr_matrix, show=False)

        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:

        st.subheader("Capital Allocation")

        fig_cap = viz.plot_weights_pie(
            allocation.to_frame("Allocation"),
            "Allocation",
            show=False
        )

        fig_cap.update_traces(
            textinfo="label+value",
            hovertemplate="%{label}<br>$%{value:,.0f}<extra></extra>"
        )

        st.plotly_chart(fig_cap, use_container_width=True)

    # -------------------------
    # SHARES
    # -------------------------
    
    shares = constructor.compute_shares(
        prices,
        results["benchmark_prices"],
        capital
    )
            
                
    shares_df = constructor.shares_dataframe(
        prices,
        results["benchmark_prices"],
        capital
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Shares to Buy")

        st.dataframe(shares_df)

    with col2:

        fig_qty = viz.plot_weights_pie(
            shares.to_frame("Shares"),
            "Shares",
            show=False
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

    st.subheader("Strategies Statistics")

    st.dataframe(asset_metrics)
    
    
