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

# Template dasar (base layout) untuk semua grafik agar tampilannya konsisten
# Mengatur jenis font, warna background, margin, dan posisi legend secara global.
_LAYOUT_BASE = dict(
    font=dict(family="Inter, sans-serif", size=12, color="#1A202C"),
    plot_bgcolor="white",  # Warna latar dalam grafik
    paper_bgcolor="white", # Warna latar luar grafik
    margin=dict(l=20, r=20, t=50, b=20),
    hovermode="x unified", # Menyatukan tooltip saat di-hover pada sumbu x yang sama
    legend=dict(
        orientation="h",   # Legend horizontal
        yanchor="bottom",
        y=1.02,            # Posisi legend di atas grafik
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
    """
    Membuat grafik garis (line chart) untuk menampilkan tren data historis mentah.
    Sering digunakan di halaman awal setelah data di-load.

    Args:
        ts: pd.Series berisi data time series.
        title: Judul grafik.
        y_label: Label untuk sumbu Y.

    Returns:
        go.Figure: Objek figure Plotly yang siap dirender oleh Streamlit (st.plotly_chart).
    """
    fig = go.Figure()
    
    # Menambahkan garis utama dengan titik (markers)
    fig.add_trace(go.Scatter(
        x=ts.index,
        y=ts.values,
        mode="lines+markers",
        name="Data Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5, color=CHART_ACTUAL_COLOR),
        fill="tozeroy", # Memberi warna isian (area) dari garis ke sumbu bawah (y=0)
        fillcolor="rgba(33,150,243,0.07)", # Warna biru sangat transparan
        hovertemplate="%{x|%Y-%m}<br>Nilai: %{y:,.0f}<extra></extra>", # Format tooltip
    ))
    
    # Menggabungkan layout bawaan dengan layout khusus grafik ini
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
    """
    Membuat grafik untuk membandingkan data asli (aktual) dengan hasil tebakan model (fitted) 
    pada periode waktu yang sama (in-sample). Berguna untuk melihat seberapa pas model "memahami" pola data.

    Args:
        actual: Data asli.
        fitted: Data hasil tebakan model SARIMA.
    """
    fig = go.Figure()
    
    # Garis data asli (solid line)
    fig.add_trace(go.Scatter(
        x=actual.index, y=actual.values,
        mode="lines+markers", name="Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5),
        hovertemplate="Aktual: %{y:,.0f}<extra></extra>",
    ))
    
    # Garis data tebakan (dashed line / putus-putus) untuk membedakan dengan data asli
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
    """
    Membuat grafik lengkap peramalan masa depan (out-of-sample).
    Menampilkan data historis asli, garis prediksi ke depan, dan pita interval kepercayaan (Confidence Interval).
    """
    fig = go.Figure()

    # 1. Menggambar Pita Confidence Interval (CI) terlebih dahulu agar berada di layer bawah (background)
    if forecast_lower is not None and forecast_upper is not None:
        # Trik Plotly untuk menggambar area: 
        # Gabungkan titik x batas atas maju, lalu titik x batas bawah mundur, lalu isi tengahnya (toself).
        fig.add_trace(go.Scatter(
            x=list(forecast_upper.index) + list(forecast_lower.index[::-1]),
            y=list(forecast_upper.values) + list(forecast_lower.values[::-1]),
            fill="toself",
            fillcolor=CHART_CI_COLOR, # Warna pita transparan
            line=dict(color="rgba(0,0,0,0)"), # Garis tepinya dihilangkan
            name="Confidence Interval 95%",
            hoverinfo="skip", # Jangan munculkan tooltip untuk pitanya
        ))

    # 2. Garis Historis Aktual
    fig.add_trace(go.Scatter(
        x=actual.index, y=actual.values,
        mode="lines+markers", name="Aktual",
        line=dict(color=CHART_ACTUAL_COLOR, width=2.5),
        marker=dict(size=5),
        hovertemplate="Aktual: %{y:,.0f}<extra></extra>",
    ))

    # 3. Garis Prediksi Masa Depan (Forecast)
    fig.add_trace(go.Scatter(
        x=forecast_mean.index, y=forecast_mean.values,
        mode="lines+markers", name="Forecast",
        line=dict(color=CHART_FORECAST_COLOR, width=2.5),
        marker=dict(size=6, symbol="diamond"), # Pakai simbol wajik agar berbeda dengan aktual
        hovertemplate="Forecast: %{y:,.0f}<extra></extra>",
    ))

    # 4. Garis Vertikal Pemisah (Pembatas antara masa lalu dan masa depan)
    if len(actual) > 0:
        try:
            # Cari titik waktu terakhir dari data aktual
            last_x = actual.index[-1]
            # Konversi objek Timestamp Pandas ke format string ISO standar 
            # untuk menghindari bug/crash kompatibilitas antara Pandas v3 dan Plotly
            if hasattr(last_x, "isoformat"):
                last_x = last_x.isoformat()
            else:
                last_x = str(last_x)
                
            # Tambahkan garis vertikal putus-putus
            fig.add_vline(
                x=last_x,
                line_dash="dot",
                line_color="rgba(0,0,0,0.3)",
                annotation_text="Batas Historis",
                annotation_position="top right",
            )
        except Exception:
            pass  # Jika gagal memformat tanggal, abaikan saja garis pembatasnya

    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title=y_label,
        height=420,
    )
    return fig


def chart_residuals(residuals: pd.Series, title: str = "Grafik Residual") -> go.Figure:
    """
    Membuat grafik batang (bar chart) untuk menampilkan selisih error (residual) dari model tiap periode.
    Warna hijau untuk error positif (tebakan < asli), merah untuk error negatif (tebakan > asli).
    """
    fig = go.Figure()
    
    # Gunakan list comprehension untuk memberi warna dinamis pada setiap bar
    fig.add_trace(go.Bar(
        x=residuals.index, y=residuals.values,
        name="Residual",
        marker_color=[
            CHART_RESIDUAL_COLOR if v >= 0 else CHART_FITTED_COLOR
            for v in residuals.values
        ],
        hovertemplate="Residual: %{y:,.4f}<extra></extra>",
    ))
    
    # Garis nol horizon di tengah grafik
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
    """
    Membuat grafik garis sederhana untuk membandingkan dua dataset time series secara langsung (overlay).
    """
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
    """
    Membuat grafik batang yang menunjukkan laju perubahan naik/turun nilai dibanding periode sebelumnya.
    """
    # .diff() menghitung selisih dengan nilai sebelumnya. Baris pertama pasti NaN, jadi di-dropna.
    changes = ts.diff().dropna()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=changes.index,
        y=changes.values,
        name="Perubahan",
        marker_color=[
            "rgba(46,204,113,0.7)" if v >= 0 else "rgba(231,76,60,0.7)" # Hijau jika naik, merah jika turun
            for v in changes.values
        ],
        hovertemplate="%{x}<br>Perubahan: %{y:,.0f}<extra></extra>",
    ))
    
    # Garis nol sebagai baseline
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.3)")
    
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0),
        xaxis_title="Periode",
        yaxis_title="Perubahan",
        height=300,
    )
    return fig


def chart_multi_category_trend(df: pd.DataFrame, col_period: str, col_value: str, col_category: str, title: str = "Tren Multi-Kategori") -> go.Figure:
    """
    Membuat grafik multi-garis menggunakan Plotly Express untuk membandingkan banyak kategori sekaligus.
    Warna garis akan diberikan secara otomatis berbeda untuk tiap kategori.
    """
    fig = px.line(
        df,
        x=col_period,
        y=col_value,
        color=col_category, # Variabel ini yang membuat plotly otomatis membuat banyak garis
        markers=True,
    )

    # Bangun layout dengan mencopy dari _LAYOUT_BASE tapi timpa/override key yang bentrok.
    # Karena legend untuk multi-kategori biasanya panjang, kita taruh legend-nya secara vertikal di sebelah kanan, 
    # bukan horizontal di atas (agar tidak menutupi grafik).
    layout = _LAYOUT_BASE.copy()
    layout["legend"] = dict(
        orientation="v",   # Legend vertikal
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,            # Digeser ke sisi luar kanan
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="rgba(0,0,0,0.1)",
        borderwidth=1,
    )
    layout["margin"] = dict(l=20, r=160, t=50, b=20)  # Beri ruang (padding) ekstra 160px di kanan untuk legend
    layout["height"] = 500
    layout["title"] = dict(text=title, font=dict(size=16, color=COLOR_PRIMARY, weight=700), x=0)
    layout["xaxis_title"] = "Periode"
    layout["yaxis_title"] = "Nilai"

    # Terapkan layout yang sudah dimodifikasi
    fig.update_layout(**layout)
    return fig
