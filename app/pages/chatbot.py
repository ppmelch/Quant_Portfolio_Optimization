import streamlit as st
from openai import OpenAI


class PortfolioChatbot:

    def __init__(self, tickers , benchmark , interval , rebalancing_frequency , capital , strategy , weights , metrics):
        
        self.tickers = tickers
        self.benchmark = benchmark
        self.interval = interval
        self.rebalancing_frequency = rebalancing_frequency
        self.capital = capital
        self.strategy = strategy
        self.weights = weights
        self.metrics = metrics


        self.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )

    def build_context(self):

        return f"""
        You are a financial portfolio assistant helping users understand a portfolio optimization dashboard.

        You must explain financial concepts clearly and interpret the portfolio results shown in the dashboard.
        
        ----- PORTFOLIO INPUTS -----
        {self.tickers} (Selected Assets)
        
        
        {self.benchmark} (Benchmark)
        
        Data Interval:
        {self.interval} (Data Interval)
        
        Rebalancing Frequency:
        {self.rebalancing_frequency} (Rebalancing Frequency)
        
        Initial Capital:
        {self.capital} (Initial Capital)
        
        Strategy:
        {self.strategy} (Optimization Strategy)
        
        weights:
        {self.weights} (Asset Weights)
        
        ----- DASHBOARD CONTEXT -----

        Portfolio Strategies Metrics:

        Expected Return: {self.metrics['return']}
        Volatility: {self.metrics['volatility']}
        Sharpe Ratio: {self.metrics['sharpe']}
        Beta: {self.metrics['beta']}
        Downside Risk: {self.metrics['downside_risk']}
        Upside Risk: {self.metrics['upside_risk']}
        Max Drawdown: {self.metrics['max_drawdown']}
        Omega Ratio: {self.metrics['omega']}
        Sortino Ratio: {self.metrics['sortino']}
        Treynor Ratio: {self.metrics['treynor']}
        Alpha Jensen: {self.metrics['alpha_jensen']}
        Calmar Ratio: {self.metrics['calmar']}

        ----- WHAT YOU SHOULD EXPLAIN -----

        Ticker Information:
        Explain what the selected assets are and their role in the portfolio.

        Interval Information:
        Explain how the data interval affects the backtesting results.

        Capital Information:
        Explain how the initial capital affects portfolio allocation and backtesting.

        Backtesting Behavior:
        Explain how the backtesting simulation works.

        Portfolio Selection:
        Explain the strategies available:
        - Minimum Variance
        - Maximum Sharpe
        - Minimum Semivariance
        - Maximum Omega

        Strategy vs Benchmark:
        Explain how to interpret the strategy vs benchmark performance graph.

        Results Interpretation:

        Correlation Matrix:
        Explain how asset correlations influence diversification.

        Portfolio Weights:
        Explain how weights are determined by each optimization strategy.

        Capital Allocation:
        Explain how capital is distributed across assets.

        Shares to Buy:
        Explain how the number of shares is calculated.

        When answering:
        - Use the provided metrics
        - Explain concepts clearly
        - Relate explanations to the portfolio when possible
        """


    def run(self):

        context = self.build_context()

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        for msg in st.session_state.chat_messages:
            st.chat_message(msg["role"]).write(msg["content"])

        prompt = st.chat_input("Ask about the portfolio")

        if prompt:

            st.session_state.chat_messages.append({
                "role": "user",
                "content": prompt
            })

            messages = [
                {"role": "system", "content": context}
            ] + st.session_state.chat_messages

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            reply = response.choices[0].message.content

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": reply
            })

            st.chat_message("assistant").write(reply)
            
    def get_response(self, messages):

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        return response.choices[0].message.content