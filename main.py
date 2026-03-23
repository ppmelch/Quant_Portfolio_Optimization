import streamlit as st
from app.components.visualization import Visualization
from app.utils.assets import load_css, load_icons
from core.pipeline.run_pipeline import run_pipeline
from app.components.layout import render_inputs , render_layout
from services.portfolio_service import build_portfolio, compute_metrics
from app.components.ui import render_footer, render_hero, render_navbar, render_scripts


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