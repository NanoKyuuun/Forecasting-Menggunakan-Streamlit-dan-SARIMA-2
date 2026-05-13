# ============================================================
# analysis_page.py — Analisis Time Series (Issue 4&5)
# ============================================================

import streamlit as st
import pandas as pd
from src.core.transformation import get_descriptive_stats
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import show_warning, show_section_title
from src.ui.charts import chart_historical_trend, chart_bar_changes
from src.utils.constants import SS_TIME_SERIES, SS_SELECTED_CATEGORY, SS_DATA_FREQUENCY
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

    # ── Grafik Tren Historis ──────────────────────────────────
    show_section_title("📈 Grafik Tren Historis")
    cat_label = f" — {category}" if category else ""
    fig_trend = chart_historical_trend(
        ts,
        title=f"Tren Historis Data{cat_label}",
        y_label="Nilai",
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
