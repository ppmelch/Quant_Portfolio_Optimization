# Quant Portfolio Optimization
**Author:** 
- José Armando Melchor Soto

---

## Table of Contents


---
## Overview

A quantitative finance dashboard designed to build, optimize, and analyze investment portfolios using advanced allocation strategies such as Minimum Variance, Maximum Sharpe, Semi-Variance, and Omega optimization.

The platform enables users to simulate portfolio performance through dynamic backtesting, compare strategies against benchmarks, and evaluate risk using key financial metrics including volatility, Sharpe ratio, drawdown, and downside risk.

With flexible inputs for asset selection, rebalancing frequency, and capital allocation, the system provides a realistic environment for portfolio construction and strategy testing. Users can interactively explore performance evolution, correlation structures, asset allocation, and portfolio composition, gaining deeper insights into diversification and risk exposure.

Additionally, the dashboard bridges theory and practice by translating optimal portfolio weights into actionable investment decisions, including capital distribution and the exact number of shares to buy.

- 🚧 The project is currently evolving towards an AI-powered interface, where a built-in chatbot will allow users to interact with the system using natural language — enabling actions such as selecting optimization strategies, adjusting parameters, and triggering portfolio recomputations dynamically.

---

## Architecture

### Project Structure

```mermaid
graph LR
    ROOT["Quant_Portfolio_Optimization/"]

    ROOT --> STREAMLIT[".streamlit/"]
    ROOT --> APP["app/"]
    ROOT --> SERVICES["services/"]
    ROOT --> NOTEBOOKS["notebooks/"]
    ROOT --> CORE["core/"]
    ROOT --> INFRA["infrastructure/"]
    ROOT --> REQ["requirements.txt"]
    ROOT --> README["README.md"]

    %% .streamlit
    STREAMLIT --> CONFIG["config.toml"]
    STREAMLIT --> SECRETS["secrets.toml"]

    %% app/
    APP --> ASSETS["assets/"]
    APP --> COMPONENTS["components/"]
    APP --> UTILS["utils/"]
    APP --> MAIN["main.py"]

    ASSETS --> IMAGES["images/"]
    ASSETS --> STYLES_DIR["styles/"]
    STYLES_DIR --> STYLESCSS["styles.css"]

    COMPONENTS --> LAYOUT["layout.py"]
    COMPONENTS --> UI["ui.py"]
    COMPONENTS --> VIZ["viz.py"]
    COMPONENTS --> CHATBOT_UI["chatbot_ui.py"]

    UTILS --> ASSETS_PY["assets.py"]

    %% services/
    SERVICES --> CHATBOT["chatbot.py"]
    SERVICES --> PORTFOLIO_SVC["portfolio_service.py"]

    %% notebooks/
    NOTEBOOKS --> NB["Proyecto.ipynb"]

    %% core/
    CORE --> DATA_DIR["data/"]
    CORE --> ANALYTICS["analytics/"]
    CORE --> BACKTESTING["backtesting/"]
    CORE --> OPTIMIZATION["optimization/"]
    CORE --> PIPELINE["pipeline/"]
    CORE --> PORTFOLIO["portfolio/"]

    DATA_DIR --> DATA_LOADER["data_loader.py"]
    ANALYTICS --> METRICS["metrics.py"]
    BACKTESTING --> BACKTEST["backtest.py"]
    OPTIMIZATION --> OPTIMIZATION_PY["optimization.py"]
    PIPELINE --> RUN_PIPELINE["run_pipeline.py"]
    PORTFOLIO --> PORTFOLIO_CONSTRUCTION["portfolio_construction.py"]
```

---
### Functional Architecture

---

### OOP Architecture

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/ppmelch/Credit_Scoring_Model.git
cd Credit_Scoring_Model

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```


