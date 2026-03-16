import pandas as pd
import plotly.graph_objects as go


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
                text='Matriz de Correlación',
                font=dict(size=16),
                x=0.5,
                xanchor='center'
            ),
            width=800,
            height=700,
            xaxis=dict(side='bottom'),
            yaxis=dict(autorange='reversed')
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        if show:
            fig.show()

        return fig

    # --------------------------------------------------
    # Portfolio weights pie chart
    # --------------------------------------------------
    def plot_weights_pie(self, df_percent: pd.DataFrame, strategy_name: str, show: bool = True):

        if strategy_name not in df_percent.columns:
            raise ValueError(f"'{strategy_name}' no está en las columnas del DataFrame.")

        weights = df_percent[strategy_name]

        if weights.max() > 1.5:
            weights = weights / 100

        n_colors = len(weights)
        greys = [
            f'rgb({int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))})'
            for i in range(n_colors)
        ]

        labels_pie = [
            f"{weight * 100:.2f}%" if weight > 0.0001 else ''
            for weight in weights
        ]

        hover_text = [
            f"{name}<br>{weight * 100:.2f}%"
            for name, weight in zip(weights.index, weights)
        ]

        fig = go.Figure(data=[go.Pie(
            labels=weights.index,
            values=weights,
            text=labels_pie,
            textposition='outside',
            textinfo='text',
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(colors=greys, line=dict(color='white', width=1)),
            rotation=90
        )])

        fig.update_layout(
            title=dict(
                text=f"Estrategia: {strategy_name}",
                font=dict(size=16),
                x=0.5,
                xanchor='center'
            ),
            width=1000,
            height=600
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

        fig.update_layout(
            title='Evolución del Capital - Backtesting Dinámico',
            xaxis_title='Fecha',
            yaxis_title='Capital acumulado (USD)',
            hovermode='x unified',
            width=1400,
            height=700
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
            title=f'{strategy} vs Benchmark - Backtesting',
            xaxis_title='Fecha',
            yaxis_title='Capital acumulado (USD)',
            hovermode='x unified',
            width=700,
            height=350
        )

        if show:
            fig.show()

        return fig