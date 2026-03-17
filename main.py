import streamlit as st
from frontend.visualization import Visualization
from backend.src.pipeline.run_pipeline import run_pipeline
from app.layout import render_inputs , render_layout


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

    viz = Visualization()

    render_layout(
        st.session_state["results"],
        capital,
        viz
    )