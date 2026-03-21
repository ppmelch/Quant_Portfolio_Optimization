import pandas as pd
import plotly.graph_objects as go


class Visualization:

    def __init__(self):
        pass

    # --------------------------------------------------
    # 🎨 THEME CENTRAL (CLAVE)
    # --------------------------------------------------
    def _base_layout(self, title=None):

        return dict(
            height=450,  # 🔥 tamaño estándar
            margin=dict(l=40, r=40, t=60, b=40),

            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16, color="white")
            ) if title else None,

            font=dict(
                family="Poppins",
                color="white"   # 🔥 SIEMPRE BLANCO
            ),

            template="simple_white",

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            legend=dict(
                font=dict(color="white")
            )
        )

    # --------------------------------------------------
    # 📊 Correlation matrix
    # --------------------------------------------------
    def corr_matrix(self, corr: pd.DataFrame, show=True):

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

        fig.update_xaxes(
            showgrid=False,
            tickfont=dict(color="white")
        )

        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(color="white"),
            autorange='reversed'
        )

        return fig

    # --------------------------------------------------
    # 🥧 Pie chart
    # --------------------------------------------------
    def plot_weights_pie(self, weights: pd.Series, strategy_name: str, show=True):

        n_colors = len(weights)

        greys = [
            f'rgb({int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))}, '
            f'{int(255 - i * 200 / (n_colors - 1))})'
            for i in range(n_colors)
        ]

        fig = go.Figure(data=[go.Pie(
            labels=weights.index,
            values=weights.values,
            text=[f"{w*100:.1f}%" if w > 0.0001 else '' for w in weights],
            textposition='outside',
            hovertext=[f"{n}<br>{w*100:.2f}%" for n, w in zip(weights.index, weights)],
            hoverinfo='text',
            marker=dict(colors=greys, line=dict(color='white', width=1)),
            textfont=dict(color="white", size=13),
        )])

        fig.update_layout(**self._base_layout(f"Strategy: {strategy_name}"))

        return fig

    # --------------------------------------------------
    # 📈 Backtesting general
    # --------------------------------------------------
    def plot_backtesting(self, history: pd.DataFrame, show=True):

        fig = go.Figure()

        colors = [
            "#444E79", "#44724E", "#990A00", "#5A356C",
            "#606060", "#818181", "#5C5547", "#9F979F"
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

        fig.update_xaxes(
            title="Date",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            tickfont=dict(color="Grey"),
            title_font=dict(color="Grey")
        )

        fig.update_yaxes(
            title="Capital (USD)",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            tickfont=dict(color="Grey"),
            title_font=dict(color="Grey")
        )

        return fig

    # --------------------------------------------------
    # 📊 Backtesting vs Benchmark
    # --------------------------------------------------
    def plot_backtesting_strategy(self, history, strategy, show=True):

        data = history[[strategy, "Benchmark"]]

        fig = go.Figure()

        colors = {
            strategy: "#424349",
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

        fig.update_layout(**self._base_layout(
            f'Capital Evolution: {strategy} vs Benchmark'
        ))

        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            tickfont=dict(color="grey")
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            tickfont=dict(color="grey")
        )

        return fig
    
    