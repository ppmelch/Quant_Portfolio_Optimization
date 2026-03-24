import streamlit as st
from app.components.viz import Visualization
from app.utils.assets import load_css, load_icons
from core.pipeline.run_pipeline import run_pipeline
from app.components.layout import render_inputs, render_layout
from services.portfolio_service import build_portfolio, compute_metrics
from app.components.ui import render_footer, render_hero, render_navbar, render_scripts


def main():
    """
    Execute the Streamlit-based portfolio optimization dashboard.

    This function serves as the main entry point of the application and orchestrates
    the full workflow, including UI initialization, user input handling, portfolio
    computation, and visualization rendering.

    Workflow
    --------
    1. Initialize the Streamlit app configuration and load UI assets such as CSS and icons.
    2. Render static interface components including the navigation bar and hero section.
    3. Collect user inputs:
        - Asset tickers
        - Benchmark
        - Historical data interval
        - Rebalancing frequency
        - Investment capital
    4. When the user triggers execution:
        - Parse and clean ticker inputs
        - Run the full portfolio pipeline:
            * Data retrieval
            * Return computation
            * Portfolio optimization
            * Backtesting simulation
            * Metrics generation
        - Store results in Streamlit session state
    5. If results exist in session state:
        - Retrieve selected portfolio strategy and benchmark allocation
        - Build portfolio allocation (weights, capital distribution, shares)
        - Compute portfolio performance metrics
        - Render all dashboard visualizations and tables
    6. Render footer and inject custom scripts for enhanced UI behavior.

    Notes
    -----
    - Relies on `st.session_state` to persist results across user interactions.
    - The dashboard is reactive: changes in portfolio selection or benchmark weight
      dynamically update the displayed results without recomputing the entire pipeline.
    - External dependencies include financial data retrieval (yfinance) and optimization modules.

    Raises
    ------
    ValueError
        If invalid inputs are provided or no financial data can be retrieved.

    Side Effects
    ------------
    - Updates Streamlit session state.
    - Triggers external API calls (financial data and optional LLM services).
    - Renders interactive charts and tables in the web interface.
    """
    st.set_page_config(layout="wide")

    load_css()
    icons = load_icons()

    render_navbar(icons)
    render_hero()

    st.markdown("---")

    raw_tickers, benchmark, interval, rebalancing_freq, capital, run_button = render_inputs()

    if run_button:
        tickers = [t.strip().upper() for t in raw_tickers.split(",")]

        st.session_state["results"] = run_pipeline(
            tickers=tickers,
            benchmark=benchmark,
            interval=interval,
            capital=capital,
            rebalancing_freq=rebalancing_freq
        )

    if "results" in st.session_state:
        results = st.session_state["results"]
        viz = Visualization()

        portfolio_choice = st.session_state.get("portfolio_choice", "Min_var")
        benchmark_weight = st.session_state.get("benchmark_weight", 0.5)

        portfolio_data = build_portfolio(
            results=results,
            capital=capital,
            portfolio_choice=portfolio_choice,
            benchmark_weight=benchmark_weight
        )

        stats = compute_metrics(
            results=results,
            portfolio_choice=portfolio_choice,
            benchmark_weight=benchmark_weight
        )

        render_layout(
            results=results,
            capital=capital,
            viz=viz,
            portfolio_data={
                **portfolio_data,
                "portfolio_choice": portfolio_choice,
                "benchmark_weight": benchmark_weight
            },
            stats=stats
        )

    st.markdown("---")

    render_footer(icons)
    render_scripts()


if __name__ == "__main__":
    main()
