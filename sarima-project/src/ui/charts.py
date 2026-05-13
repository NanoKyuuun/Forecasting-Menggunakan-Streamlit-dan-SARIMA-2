# ============================================================
# charts.py — Komponen Grafik Plotly Reusable
# ============================================================

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.utils.constants import (
    COLOR_PRIMARY, CHART_ACTUAL_COLOR, CHART_FITTED_COLOR,
    CHART_FORECAST_COLOR, CHART_CI_COLOR, CHART_RESIDUAL_COLOR,
)

_LAYOUT_BASE = dict(
    font=dict(family="Inter, sans-serif", size=12, color="#1A202C"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=50, b=20),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="rgba(0,0,0,0.1)",
        borderwidth=1,
    ),
    xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False),
)


def chart_historical_trend(ts: pd.Series, title: str = "Tren Historis", y_label: str = "Nilai") -> go.Figure:
    """Grafik tren historis (line chart)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts.index,
        y=ts.values,
        mode="lines+markers",
        name="Data Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5, color=CHART_ACTUAL_COLOR),
        fill="tozeroy",
        fillcolor="rgba(33,150,243,0.07)",
        hovertemplate="%{x|%Y-%m}<br>Nilai: %{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title=y_label,
        height=380,
    )
    return fig


def chart_actual_vs_fitted(
    actual: pd.Series,
    fitted: pd.Series,
    title: str = "Aktual vs Fitted",
    y_label: str = "Nilai",
) -> go.Figure:
    """Grafik aktual vs nilai fitted model."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actual.index, y=actual.values,
        mode="lines+markers", name="Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5),
        hovertemplate="Aktual: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=fitted.index, y=fitted.values,
        mode="lines", name="Fitted",
        line=dict(color=CHART_FITTED_COLOR, width=2, dash="dash"),
        hovertemplate="Fitted: %{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title=y_label,
        height=380,
    )
    return fig


def chart_forecast(
    actual: pd.Series,
    forecast_mean: pd.Series,
    forecast_lower: pd.Series = None,
    forecast_upper: pd.Series = None,
    title: str = "Hasil Forecasting",
    y_label: str = "Nilai",
) -> go.Figure:
    """Grafik aktual + forecast + confidence interval."""
    fig = go.Figure()

    # Confidence interval (fill)
    if forecast_lower is not None and forecast_upper is not None:
        fig.add_trace(go.Scatter(
            x=list(forecast_upper.index) + list(forecast_lower.index[::-1]),
            y=list(forecast_upper.values) + list(forecast_lower.values[::-1]),
            fill="toself",
            fillcolor=CHART_CI_COLOR,
            line=dict(color="rgba(0,0,0,0)"),
            name="Confidence Interval 95%",
            hoverinfo="skip",
        ))

    # Aktual
    fig.add_trace(go.Scatter(
        x=actual.index, y=actual.values,
        mode="lines+markers", name="Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5),
        hovertemplate="Aktual: %{y:,.0f}<extra></extra>",
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_mean.index, y=forecast_mean.values,
        mode="lines+markers", name="Forecast",
        line=dict(color=CHART_FORECAST_COLOR, width=2.5),
        marker=dict(size=6, symbol="diamond"),
        hovertemplate="Forecast: %{y:,.0f}<extra></extra>",
    ))

    # Garis pemisah aktual/forecast — konversi index ke string agar kompatibel Plotly + Pandas v3
    if len(actual) > 0:
        try:
            last_x = actual.index[-1]
            # Konversi Timestamp ke string ISO agar tidak crash di Plotly
            if hasattr(last_x, "isoformat"):
                last_x = last_x.isoformat()
            else:
                last_x = str(last_x)
            fig.add_vline(
                x=last_x,
                line_dash="dot",
                line_color="rgba(0,0,0,0.3)",
                annotation_text="Batas Historis",
                annotation_position="top right",
            )
        except Exception:
            pass  # Abaikan jika tetap gagal

    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title=y_label,
        height=420,
    )
    return fig


def chart_residuals(residuals: pd.Series, title: str = "Grafik Residual") -> go.Figure:
    """Grafik residual model."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=residuals.index, y=residuals.values,
        name="Residual",
        marker_color=[
            CHART_RESIDUAL_COLOR if v >= 0 else CHART_FITTED_COLOR
            for v in residuals.values
        ],
        hovertemplate="Residual: %{y:,.4f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.4)", line_width=1)
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title="Residual",
        height=300,
    )
    return fig


def chart_comparison(
    series_a: pd.Series,
    series_b: pd.Series,
    label_a: str = "Data A",
    label_b: str = "Data B",
    title: str = "Perbandingan Dataset",
    y_label: str = "Nilai",
) -> go.Figure:
    """Grafik perbandingan dua time series."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=series_a.index, y=series_a.values,
        mode="lines", name=label_a,
        line=dict(color=CHART_ACTUAL_COLOR, width=2),
    ))
    fig.add_trace(go.Scatter(
        x=series_b.index, y=series_b.values,
        mode="lines", name=label_b,
        line=dict(color=CHART_FORECAST_COLOR, width=2),
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title=y_label,
        height=380,
    )
    return fig


def chart_bar_changes(ts: pd.Series, title: str = "Perubahan Antar Periode") -> go.Figure:
    """Bar chart perubahan nilai antar periode."""
    changes = ts.diff().dropna()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=changes.index,
        y=changes.values,
        name="Perubahan",
        marker_color=[
            "rgba(46,204,113,0.7)" if v >= 0 else "rgba(231,76,60,0.7)"
            for v in changes.values
        ],
        hovertemplate="%{x}<br>Perubahan: %{y:,.0f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.3)")
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title="Perubahan",
        height=300,
    )
    return fig
