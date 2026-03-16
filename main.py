import streamlit as st
from frontend.visualization import Visualization
from backend.src.pipeline.run_pipeline import run_pipeline
from app.layout import render_layout

st.set_page_config(page_title="Quant Portfolio Optimization", layout="wide")

st.title("Quant Portfolio Optimization Dashboard")
st.markdown("---")

raw_tickers = st.text_input(
    "Tickers",
    value="AZO,MA,AAPL,F"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    benchmark = st.text_input(
        "Benchmark",
        value="SPY"
    )

with col2:
    interval = st.selectbox(
        "Interval",
        ["6m", "1y", "2y", "5y", "10y"]
    )

with col3:
    capital = st.number_input(
        "Capital to invest ($)",
        min_value=1000,
        value=1_000_000,
        step=100_000
    )

with col4:
    st.write("")
    st.write("")
    run_button = st.button("Run", type="primary")

st.markdown("---")

if run_button:

    tickers = [t.strip().upper() for t in raw_tickers.split(",")]

    st.session_state["results"] = run_pipeline(
        tickers=tickers,
        benchmark=benchmark,
        interval=interval
    )

if "results" in st.session_state:

    viz = Visualization()

    render_layout(
        st.session_state["results"],
        capital,
        viz
    )