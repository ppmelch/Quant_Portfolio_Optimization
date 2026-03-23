import pandas as pd
import plotly.graph_objects as go


class Visualization:
    """
    Class responsible for generating all visualizations in the dashboard.
    """

    def __init__(self):
        """
        Initialize the visualization class.
        """
        pass

    def _base_layout(self, title=None):
        """
        Generate a consistent base layout for all plots.

        Parameters
        ----------
        title : str, optional
            Title of the plot.

        Returns
        -------
        dict
            Layout configuration for Plotly figures.
        """
        return dict(
            height=450,
            margin=dict(l=40, r=40, t=60, b=40),
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16, color="white")
            ) if title else None,
            font=dict(family="Poppins", color="white"),
            template="simple_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="white"))
        )

    def corr_matrix(self, corr: pd.DataFrame, show=True):
        """
        Generate a correlation matrix heatmap.

        Parameters
        ----------
        corr : pd.DataFrame
            Correlation matrix.
        show : bool, optional
            Whether to display the plot.

        Returns
        -------
        go.Figure
        """
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='Greys',
            zmid=0,
            text=corr.values,
            texttemplate='%{text:.4f}',
            textfont={"size": 10, "color": "white"},
            hovertemplate='%{y} vs %{x}<br>%{z:.4f}<extra></extra>'
        ))

        fig.update_layout(**self._base_layout("Correlation Matrix"))
        return fig

    def plot_weights_pie(self, weights: pd.Series, strategy_name: str, show=True):
        """
        Generate a pie chart for portfolio weights.

        Parameters
        ----------
        weights : pd.Series
            Asset weights.
        strategy_name : str
            Name of the strategy.
        show : bool, optional
            Whether to display the plot.

        Returns
        -------
        go.Figure
        """
        fig = go.Figure(data=[go.Pie(
            labels=weights.index,
            values=weights.values
        )])

        fig.update_layout(**self._base_layout(f"Strategy: {strategy_name}"))
        return fig

    def plot_backtesting(self, history: pd.DataFrame, show=True):
        """
        Plot full backtesting performance.

        Parameters
        ----------
        history : pd.DataFrame
            Time series of portfolio values.
        show : bool, optional

        Returns
        -------
        go.Figure
        """
        fig = go.Figure()

        for col in history.columns:
            fig.add_trace(go.Scatter(
                x=history.index,
                y=history[col],
                mode='lines',
                name=col
            ))

        return fig

    def plot_backtesting_strategy(self, history, strategy, show=True):
        """
        Plot a strategy against the benchmark.

        Parameters
        ----------
        history : pd.DataFrame
        strategy : str
        show : bool, optional

        Returns
        -------
        go.Figure
        """
        data = history[[strategy, "Benchmark"]]

        fig = go.Figure()

        for col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[col],
                mode='lines',
                name=col
            ))

        fig.update_layout(
            **self._base_layout(f'Capital Evolution: {strategy} vs Benchmark')
        )

        return fig
