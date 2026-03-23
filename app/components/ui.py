import streamlit as st
import streamlit.components.v1 as components


def render_navbar(icons):
    """
    Render the top navigation bar with links and dropdown menus.

    Parameters
    ----------
    icons : dict
        Dictionary containing base64-encoded images for UI elements.
    """
    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <nav class="menu transparent">
    
    <a href="https://github.com/ppmelch" target="_blank">GitHub</a>
    
    <div class="submenu">
    <a class="menu-link">Projects</a>
    
    <div class="submenu-items">
    
    <a class="submenu-item" href="#">
    <img src="data:image/png;base64,{icons['portfolio']}">
    Credit Scoring Model
    </a>
    
    <a class="submenu-item" href="#">
    <img src="data:image/png;base64,{icons['portfolio']}">
    Advanced Trading Strategies
    </a>
    
    <a class="submenu-item" href="#">
    <img src="data:image/png;base64,{icons['portfolio']}">
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
        <img src="data:image/png;base64,{icons['telefono']}">
        +52 33 1299 0677
    </a>
    
    </div>
    
    </div>
    
    </nav>
    
    
    
    """, unsafe_allow_html=True)


def render_hero():
    """
    Render the hero section including title, subtitle, and description.
    """
    st.markdown("""
    <section class="hero">
    
    <h1 class="typewriter">Quant Portfolio Optimization</h1>
    
    <h2 class="hero-subtitle">Dynamic Portfolio Optimization & Backtesting Platform</h2>
    
    <p class="hero-description">
    A quantitative finance dashboard designed to build, optimize, and analyze investment portfolios using advanced strategies such as Minimum Variance, Maximum Sharpe, Semi-Variance, and Omega optimization.
    The platform allows users to simulate portfolio performance through dynamic backtesting, compare results against benchmarks, and evaluate risk using key metrics like volatility and Sharpe ratio. With flexible inputs for asset selection, rebalancing frequency, and capital allocation, it provides a realistic environment for portfolio construction.
    Through an interactive interface, users can visualize performance, correlations, asset allocation, and translate optimal weights into real investment decisions, including capital distribution and number of shares to buy.
    </p>
    
    </section>
    """, unsafe_allow_html=True)


def render_footer(icons):
    """
    Render the footer section with social links and contact information.

    Parameters
    ----------
    icons : dict
        Dictionary containing base64-encoded icons.
    """
    st.markdown(f"""
    <footer class="footer">
    
    <div class="social-icons">
    
    <a href="https://github.com/ppmelch" target="_blank">
    <img src="data:image/png;base64,{icons['github']}" width="40">
    </a>
    
    <a href="https://linkedin.com/in/ppmelch" target="_blank">
    <img src="data:image/png;base64,{icons['linkedin']}" width="40">
    </a>
    
    <a href="https://x.com/ppmelch_" target="_blank">
    <img src="data:image/png;base64,{icons['x']}" width="40">
    </a>
    
    <a href="mailto:jose.melchor.soto@gmail.com">
    <img src="data:image/png;base64,{icons['email']}" width="40">
    </a>
    
    </div>
    
    <h5>© 2026 José Armando Melchor Soto. All rights reserved.</h5>
    
    </footer>
    """, unsafe_allow_html=True)


def render_scripts():
    """
    Inject custom JavaScript to handle dynamic navbar behavior on scroll.
    """
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
