import pathlib

import streamlit as st
from frontend.visualization import Visualization
from backend.src.pipeline.run_pipeline import run_pipeline
from app.layout import render_inputs , render_layout

st.set_page_config(layout="wide")

css_path = pathlib.Path("frontend/styles/styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


import streamlit.components.v1 as components

components.html("""
<script>

const parentDoc = window.parent.document;

const menu = parentDoc.querySelector(".menu");

if(menu){
    window.parent.addEventListener("scroll", () => {
        if(window.parent.scrollY > 10){
            menu.classList.remove("transparent");
            menu.classList.add("scrolled");
        }else{
            menu.classList.remove("scrolled");
            menu.classList.add("transparent");
        }
    });
}

const links = parentDoc.querySelectorAll(".menu a");
const currentPage = window.parent.location.pathname.split("/").pop();

links.forEach(link => {
    const linkPage = link.getAttribute("href").split("/").pop();

    if(linkPage === currentPage){
        link.classList.add("active");
    }
});

</script>
""", height=0)

#HTML
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<nav class="menu transparent">

<a href="https://github.com/ppmelch" target="_blank">GitHub</a>

<div class="submenu">
<a href="#">Projects</a>

<div class="submenu-items">

<a class="submenu-item" href="#">
<img src="images/portfolio.png">
Quant Portfolio Optimization</a>

<a class="submenu-item" href="#">
<img src="images/portfolio.png">
Credit Scoring Model
</a>

<a class="submenu-item" href="#">
<img src="images/portfolio.png">
Advanced Trading Strategies
</a>

<a class="submenu-item" href="#">
<img src="images/portfolio.png">
Mexico Crime Data Explorer
</a>

</div>
</div>

<a href="https://ppmelch.github.io/Jose_Melchor_Portfolio/">Home</a>
<a href="https://ppmelch.github.io/Jose_Melchor_Portfolio/about.html">About</a>

<div class="submenu contact-menu">
<a href="#">Contact</a>

<div class="submenu-items">
<a class="submenu-item" href="tel:+523312990677">
<img src="images/Tel.png">
+52 33 1299 0677
</a>
</div>

</div>

</nav>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">

<h1 class="typewriter">Quant Portfolio Optimization</h1>

<h2 class="hero-subtitle">Financial Engineering Course Project</h2>

<p class="hero-description">
Interactive portfio optimization dashboard with backtesting, risk metrics,
and capital allocation stragies. Visualizes asset cns, portfolio weights, and capital evolution
</p>

</section>
""", unsafe_allow_html=True)


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

    viz = Visualization()

    render_layout(
        st.session_state["results"],
        capital,
        viz
    )
    
    

st.markdown("---")

st.markdown(
"""
<footer class="footer">

<div class="social-icons">

<a href="https://github.com/ppmelch" target="_blank">
<img src="/images/github.png" alt="GitHub">
</a>

<a href="https://linkedin.com/in/ppmelch" target="_blank">
<img src="/images/LK.png" alt="LinkedIn">
</a>

<a href="https://x.com/ppmelch_" target="_blank">
<img src="/images/X.png" alt="X">
</a>

<a href="mailto:jose.melchor.soto@gmail.com">
<img src="/images/correo.png" alt="Email">
</a>

</div>

<h5>© 2026 José Armando Melchor Soto. All rights reserved.</h5>

</footer>
""",
unsafe_allow_html=True
)

