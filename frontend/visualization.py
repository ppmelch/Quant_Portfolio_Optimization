import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

class Visualization:
    """
    Visualization utilities for portfolio analysis and backtesting results.

    This class provides interactive visualizations for exploratory data
    analysis and portfolio evaluation using Plotly. It includes tools
    for correlation analysis, portfolio weight representation and
    capital evolution over time.
    """

    def __init__(self):
        """
        Initialize the Visualization class.

        This class does not require any state. All methods operate directly
        on the provided data.
        """
        pass

    # --------------------------------------------------
    # Correlation matrix
    # --------------------------------------------------
    def corr_matrix(self, corr: pd.DataFrame, show: bool = True):

        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='Greys',
            zmid=0,
            text=corr.values,
            texttemplate='%{text:.4f}',
            textfont={"size": 10},
            colorbar=dict(len=0.5, thickness=15),
            hovertemplate='%{y} vs %{x}<br>Correlación: %{z:.4f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text='Correlation Matrix of Asset Returns',
                font=dict(
                    size=16,
                    color="#444"
                ),
                x=0.5,
                xanchor='center'
            ),
            width=800,
            height=700,
            xaxis=dict(side='bottom'),
            yaxis=dict(autorange='reversed'),
            template="simple_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"

        )

        fig.update_xaxes(
            showgrid=False,
            tickfont=dict(
                color="#444",
                size=12
            )
        )

        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(
                color="#444",
                size=12
            )
        )

        if show:
            fig.show()

        return fig

    # --------------------------------------------------
    # Portfolio weights pie chart
    # --------------------------------------------------
    def plot_weights_pie(self, weights: pd.Series, strategy_name: str, show=True):

        if not isinstance(weights, pd.Series):
            raise ValueError("weights debe ser un pd.Series")

        if weights.max() > 1.5:
            weights = weights

        n_colors = len(weights)

        greys = [
            f'rgb({int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))})'
            for i in range(n_colors)
        ]

        labels_pie = [
            f"{weight * 100:.1f}%" if weight > 0.0001 else ''
            for weight in weights
        ]

        hover_text = [
            f"{name}<br>{weight * 100:.2f}%"
            for name, weight in zip(weights.index, weights)
        ]

        fig = go.Figure(data=[go.Pie(
            labels=weights.index,
            values=weights.values,
            text=labels_pie,
            textposition='outside',
            textinfo='text',
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(colors=greys, line=dict(color='white', width=1)),
            rotation=90,
            textfont=dict(
                color="#444",   # color del texto
                size=13
            ),
        )])

        fig.update_layout(
            title=dict(
                text=f"Strategy: {strategy_name}",
                font=dict(size=16, color="#444"),
                x=0.5,
                xanchor="center"
            ),
            width=1000,
            height=600,
            template="simple_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        if show:
            fig.show()

        return fig
    # --------------------------------------------------
    # Capital evolution plot
    # --------------------------------------------------
    def plot_backtesting(self, history: pd.DataFrame, show: bool = True):

        fig = go.Figure()

        colors = [
            '#001C7F', '#017517', '#8C0800', '#7600A1',
            '#B8860B', '#006374', '#573B00', '#4C004C'
        ]

        for i, col in enumerate(history.columns):
            fig.add_trace(go.Scatter(
                x=history.index,
                y=history[col],
                mode='lines',
                name=col,
                line=dict(width=2, color=colors[i % len(colors)]),
                hovertemplate='%{x}<br>%{y:,.2f} USD<extra></extra>'
            ))

        fig_backtest = px.line(
            history,
            x=history.index,
            y=history.columns,
            title="Portfolio Backtest"
        )

        fig_backtest.update_layout(

            font=dict(
                family="Poppins",
                color="#454c72"
            ),

            title=dict(
                font=dict(size=18, color="#454c72"),
                x=0.5
            ),

            xaxis=dict(
                title="Date",
                titlefont=dict(color="#454c72"),
                tickfont=dict(color="#454c72")
            ),

            yaxis=dict(
                title="Capital (USD)",
                titlefont=dict(color="#454c72"),
                tickfont=dict(color="#454c72")
            ),

            legend=dict(
                font=dict(color="#454c72")
            ),

            template="simple_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
                

        if show:
            fig.show()

        return fig



    def plot_backtesting_strategy(self, history: pd.DataFrame, strategy: str, show: bool = True):

        data = history[[strategy, "Benchmark"]]

        fig = go.Figure()

        colors = {
            strategy: "#454c72",
            "Benchmark": "#8C0800"
        }

        for col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[col],
                mode='lines',
                name=col,
                line=dict(width=2, color=colors[col]),
                hovertemplate='%{x}<br>%{y:,.2f} USD<extra></extra>'
            ))

        fig.update_layout(
            title=dict(
            text=f'Capital Evolution: {strategy} vs Benchmark',
                font=dict(
                    size=16,
                    color="#444"
                ),
                x=0.5,
                xanchor='center'
            ),
            template="simple_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        
        fig.update_xaxes(
            showgrid=False,
            tickfont=dict(
                color="#444",
                size=12
            )
        )

        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(
                color="#444",
                size=12
            )
        )

        
        if show:
            fig.show()

        return fig