# ============================================================
# analysis_page.py — Analisis Time Series (Issue 4&5)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.core.transformation import get_descriptive_stats
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import show_warning, show_section_title, show_info
from src.ui.charts import chart_historical_trend, chart_bar_changes
from src.utils.constants import SS_TIME_SERIES, SS_SELECTED_CATEGORY, SS_DATA_FREQUENCY, COLOR_PRIMARY
from src.utils.helpers import format_number, get_data_quality_label


def render():
    page_header(
        "Analisis Time Series",
        "Eksplorasi pola historis: statistik deskriptif, tren, dan visualisasi perubahan antar periode.",
        "📊",
    )

    ts          = st.session_state.get(SS_TIME_SERIES)
    category    = st.session_state.get(SS_SELECTED_CATEGORY, "")
    frequency   = st.session_state.get(SS_DATA_FREQUENCY, "—")

    if ts is None:
        show_warning("Time series belum tersedia. Kembali ke Transformasi.")
        if st.button("← Transformasi"):
            st.session_state["current_page"] = "Transformasi Time Series"
            st.rerun()
        return

    stats = get_descriptive_stats(ts)
    quality_label, quality_level = get_data_quality_label(stats["n_obs"])
    color_map = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}

    # ── Statistik Deskriptif ───────────────────────────────────
    show_section_title("📐 Statistik Deskriptif")
    show_metrics_row([
        {"label": "Total Observasi", "value": str(stats["n_obs"]),             "color": color_map.get(quality_level, "#2196F3")},
        {"label": "Nilai Minimum",   "value": format_number(stats["min"], 0),  "color": "#E74C3C"},
        {"label": "Nilai Maksimum",  "value": format_number(stats["max"], 0),  "color": "#4CAF50"},
        {"label": "Rata-rata",       "value": format_number(stats["mean"], 1), "color": "#2196F3"},
    ])
    st.markdown("<br/>", unsafe_allow_html=True)
    show_metrics_row([
        {"label": "Frekuensi Data",    "value": frequency,                           "color": "#9C27B0"},
        {"label": "Periode Awal",      "value": stats["start"],                      "color": "#607D8B"},
        {"label": "Periode Akhir",     "value": stats["end"],                        "color": "#607D8B"},
        {"label": "Kualitas Data",     "value": quality_label,                       "color": color_map.get(quality_level)},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Grafik Tren + Rolling Mean ────────────────────────────
    show_section_title("📈 Grafik Tren Historis & Rolling Mean")
    cat_label = f" — {category}" if category else ""

    window = max(3, len(ts) // 6)
    rolling_mean = ts.rolling(window=window, min_periods=1).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=list(ts.index), y=ts.values,
        mode="lines+markers", name="Aktual",
        line=dict(color="#2196F3", width=2),
        marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(33,150,243,0.07)",
    ))
    fig_trend.add_trace(go.Scatter(
        x=list(rolling_mean.index), y=rolling_mean.values,
        mode="lines", name=f"Rolling Mean (window={window})",
        line=dict(color="#FF6B35", width=2.5, dash="dash"),
    ))
    fig_trend.update_layout(
        font=dict(family="Inter, sans-serif", size=12),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)"),
        title=dict(text=f"Tren Historis{cat_label}", font=dict(size=16, color=COLOR_PRIMARY), x=0),
        xaxis_title="Periode", yaxis_title="Nilai", height=380,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Grafik Perubahan Antar Periode ────────────────────────
    show_section_title("📉 Perubahan Antar Periode")
    if len(ts) > 1:
        fig_change = chart_bar_changes(ts, title=f"Perubahan Per Periode{cat_label}")
        st.plotly_chart(fig_change, use_container_width=True)

        changes = ts.diff().dropna()
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f"""
                <div class="sarima-card">
                    <div class="metric-label">Perubahan Tertinggi</div>
                    <div style="font-size:1.4rem;font-weight:700;color:#4CAF50;">
                        +{format_number(float(changes.max()), 0)}
                    </div>
                    <div class="metric-sub">pada periode {str(changes.idxmax())[:10]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                f"""
                <div class="sarima-card">
                    <div class="metric-label">Perubahan Terendah</div>
                    <div style="font-size:1.4rem;font-weight:700;color:#E74C3C;">
                        {format_number(float(changes.min()), 0)}
                    </div>
                    <div class="metric-sub">pada periode {str(changes.idxmin())[:10]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Distribusi Nilai (Boxplot) ────────────────────────────
    show_section_title("📦 Distribusi Nilai")
    col_box, col_stats = st.columns([1, 1])
    with col_box:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=ts.values, name="Distribusi",
            marker_color="#2196F3", boxmean="sd",
            hovertemplate="Nilai: %{y:,.0f}<extra></extra>",
        ))
        fig_box.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis_title="Nilai", height=300,
            title=dict(text="Boxplot Distribusi", font=dict(size=14, color=COLOR_PRIMARY), x=0),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_stats:
        q1  = float(np.percentile(ts.values, 25))
        q3  = float(np.percentile(ts.values, 75))
        med = float(np.median(ts.values))
        std = float(ts.std())
        st.markdown(
            f"""
            <div class="sarima-card" style="height:100%;">
                <div class="metric-label" style="margin-bottom:0.8rem;">Statistik Lanjutan</div>
                <table style="width:100%;font-size:0.88rem;border-collapse:collapse;">
                    <tr><td style="padding:0.3rem 0;color:#718096;">Median</td>
                        <td style="font-weight:700;color:#1E3A5F;">{format_number(med, 0)}</td></tr>
                    <tr><td style="padding:0.3rem 0;color:#718096;">Q1 (25%)</td>
                        <td style="font-weight:700;color:#1E3A5F;">{format_number(q1, 0)}</td></tr>
                    <tr><td style="padding:0.3rem 0;color:#718096;">Q3 (75%)</td>
                        <td style="font-weight:700;color:#1E3A5F;">{format_number(q3, 0)}</td></tr>
                    <tr><td style="padding:0.3rem 0;color:#718096;">IQR</td>
                        <td style="font-weight:700;color:#1E3A5F;">{format_number(q3-q1, 0)}</td></tr>
                    <tr><td style="padding:0.3rem 0;color:#718096;">Std. Dev</td>
                        <td style="font-weight:700;color:#1E3A5F;">{format_number(std, 2)}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── ACF Sederhana (manual via Plotly) ────────────────────
    show_section_title("📊 Autokorelasi (ACF)")
    show_info("ACF menunjukkan korelasi data dengan lag sebelumnya. Nilai signifikan (di luar batas biru) mengindikasikan pola yang dapat dimodelkan.")
    if len(ts) >= 8:
        max_lags = min(20, len(ts) // 2 - 1)
        lags = list(range(1, max_lags + 1))
        acf_values = []
        ts_mean = ts.mean()
        ts_var  = float(np.var(ts.values))
        for lag in lags:
            cov = float(np.mean((ts.values[lag:] - ts_mean) * (ts.values[:-lag] - ts_mean)))
            acf_values.append(cov / ts_var if ts_var != 0 else 0)

        ci = 1.96 / np.sqrt(len(ts))
        fig_acf = go.Figure()
        for i, (lag, acf_val) in enumerate(zip(lags, acf_values)):
            color = "#2196F3" if abs(acf_val) > ci else "rgba(33,150,243,0.35)"
            fig_acf.add_trace(go.Bar(
                x=[lag], y=[acf_val], marker_color=color,
                showlegend=False, hovertemplate=f"Lag {lag}: %{{y:.3f}}<extra></extra>",
            ))
        fig_acf.add_hline(y=ci,  line_dash="dash", line_color="rgba(255,0,0,0.5)", line_width=1.5)
        fig_acf.add_hline(y=-ci, line_dash="dash", line_color="rgba(255,0,0,0.5)", line_width=1.5)
        fig_acf.add_hline(y=0,   line_dash="solid", line_color="rgba(0,0,0,0.3)", line_width=1)
        fig_acf.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Lag", yaxis_title="Korelasi",
            title=dict(text="Autocorrelation Function (ACF)", font=dict(size=14, color=COLOR_PRIMARY), x=0),
            height=300, bargap=0.3,
        )
        st.plotly_chart(fig_acf, use_container_width=True)
    else:
        show_info("Jumlah observasi terlalu sedikit untuk menampilkan grafik ACF yang bermakna (minimal 8 observasi).")

    # ── Indikasi Pola ─────────────────────────────────────────
    show_section_title("🔍 Indikasi Pola Data")
    ts_values = ts.values
    trend_indicator = "Meningkat 📈" if ts_values[-1] > ts_values[0] else ("Menurun 📉" if ts_values[-1] < ts_values[0] else "Stagnan ➡️")
    seasonal_note = (
        "✅ Data bulanan — berpotensi memiliki pola musiman yang dapat dideteksi SARIMA."
        if frequency == "Bulanan"
        else f"⚠️ Data {frequency} — jumlah observasi mungkin tidak cukup untuk mendeteksi pola musiman yang kuat."
    )
    st.markdown(
        f"""
        <div class="sarima-card">
            <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                <div>
                    <div class="metric-label">Tren Keseluruhan</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#1E3A5F;">{trend_indicator}</div>
                </div>
                <div>
                    <div class="metric-label">Indikasi Musiman</div>
                    <div style="font-size:0.88rem;color:#4a5568;margin-top:0.3rem;">{seasonal_note}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Transformasi", use_container_width=True):
            st.session_state["current_page"] = "Transformasi Time Series"
            st.rerun()
    with col2:
        if st.button("🤖  Lanjut ke Pemodelan SARIMA", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Pemodelan SARIMA"
            st.rerun()
