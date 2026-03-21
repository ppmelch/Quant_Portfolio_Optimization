import pathlib
import base64
import streamlit.components.v1 as components
import streamlit as st
from frontend.visualization import Visualization
from backend.src.pipeline.run_pipeline import run_pipeline
from app.layout import render_inputs , render_layout
 
st.set_page_config(layout="wide")
 
css_path = pathlib.Path("frontend/styles/styles.css")
 
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
 
def img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
 
github = img("frontend/images/github.png")
linkedin = img("frontend/images/LK.png")
x_icon = img("frontend/images/X.png")
email = img("frontend/images/correo.png")
telefono = img("frontend/images/Tel.png")
portafolio = img("frontend/images/portfolio.png")
 
 
 
#HTML
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
 
<nav class="menu transparent">
 
<a href="https://github.com/ppmelch" target="_blank">GitHub</a>
 
<div class="submenu">
<a class="menu-link">Projects</a>
 
<div class="submenu-items">
 
<a class="submenu-item" href="#">
<img src="data:image/png;base64,{portafolio}">
Credit Scoring Model
</a>
 
<a class="submenu-item" href="#">
<img src="data:image/png;base64,{portafolio}">
Advanced Trading Strategies
</a>
 
<a class="submenu-item" href="#">
<img src="data:image/png;base64,{portafolio}">
Mexico Crime Data Explorer
</a>
 
</div>
</div>
 
<a href="https://ppmelch.github.io/Jose_Melchor_Portfolio/" target="_self">Home</a>
 
<a href="https://ppmelch.github.io/Jose_Melchor_Portfolio/about.html" target="_self">About</a>
 
<div class="submenu contact-menu">
 
<a class="menu-link" >Contact</a>
 
<div class="submenu-items">
 
<a class="submenu-item" href="#" onclick="copyPhone(event)">
    <img src="data:image/png;base64,{telefono}">
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
Intere potfolo ozaon dsboard wting, risk metrics,
and capl alocation strategies. Visualizatis, portfolio weights, and capital evolution
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
 
 
st.markdown(f"""
<footer class="footer">
 
<div class="social-icons">
 
<a href="https://github.com/ppmelch" target="_blank">
<img src="data:image/png;base64,{github}" width="40">
</a>
 
<a href="https://linkedin.com/in/ppmelch" target="_blank">
<img src="data:image/png;base64,{linkedin}" width="40">
</a>
 
<a href="https://x.com/ppmelch_" target="_blank">
<img src="data:image/png;base64,{x_icon}" width="40">
</a>
 
<a href="mailto:jose.melchor.soto@gmail.com">
<img src="data:image/png;base64,{email}" width="40">
</a>
 
</div>
 
<h5>© 2026 José Armando Melchor Soto. All ghts reserved.</h5>
 
</footer>
""", unsafe_allow_html=True)
 
 
components.html("""
<script>

function initMenu() {

    const parentDoc = window.parent.document;
    const menu = parentDoc.querySelector(".menu");

    if (!menu) {
        setTimeout(initMenu, 150);
        return;
    }

    // Candidatos en orden de prioridad
    const selectors = [
        '[data-testid="stMainBlockContainer"]',
        '[data-testid="stAppViewBlockContainer"]',
        '[data-testid="stMain"]',
        '[data-testid="stAppViewContainer"]',
        '.main',
    ];

    let scrollContainer = null;

    for (const sel of selectors) {
        const el = parentDoc.querySelector(sel);
        if (el && el.scrollHeight > el.clientHeight) {
            scrollContainer = el;
            break;
        }
    }

    function updateMenu(scrollTop) {
        if (scrollTop > 10) {
            menu.classList.remove("transparent");
            menu.classList.add("scrolled");
        } else {
            menu.classList.remove("scrolled");
            menu.classList.add("transparent");
        }
    }

    if (scrollContainer) {
        updateMenu(scrollContainer.scrollTop);
        scrollContainer.addEventListener("scroll", () => updateMenu(scrollContainer.scrollTop));
    }

    // Fallback: window del padre
    window.parent.addEventListener("scroll", () => {
        updateMenu(window.parent.scrollY || window.parent.pageYOffset || 0);
    });

    // Si no encontró container, usar MutationObserver
    if (!scrollContainer) {
        const observer = new MutationObserver(() => {
            for (const sel of selectors) {
                const el = parentDoc.querySelector(sel);
                if (el && el.scrollHeight > el.clientHeight) {
                    scrollContainer = el;
                    updateMenu(scrollContainer.scrollTop);
                    scrollContainer.addEventListener("scroll", () => updateMenu(scrollContainer.scrollTop));
                    observer.disconnect();
                    break;
                }
            }
        });
        observer.observe(parentDoc.body, { childList: true, subtree: true });
    }
}

initMenu();


</script>
""", height=0)

components.html("""

<script>
function copyPhone(event) {
    event.preventDefault();

    const phone = "+523312990677";

    navigator.clipboard.writeText(phone).then(() => {
        const msg = document.getElementById("copied-msg");
        msg.style.display = "inline";

        setTimeout(() => {
            msg.style.display = "none";
        }, 1500);
    });
}
</script>

""", height=0)