# ============================================================
# transformation_page.py — Transformasi Time Series (Issue 4&5)
# ============================================================

import streamlit as st
from src.core.transformation import build_time_series, get_available_categories
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import show_warning, show_success, show_error, show_section_title, show_methodological_note
from src.ui.charts import chart_historical_trend, chart_multi_category_trend
from src.ui.tables import show_dataframe
from src.utils.constants import (
    SS_CLEAN_DATA, SS_TIME_SERIES, SS_SELECTED_CATEGORY, SS_DATA_FREQUENCY, SS_COL_MAPPING,
)
import pandas as pd


def render():
    page_header(
        "Transformasi Time Series",
        "Membentuk indeks waktu dan mengubah data bersih menjadi format time series.",
        "🔄",
    )

    clean_df = st.session_state.get(SS_CLEAN_DATA)
    if clean_df is None:
        show_warning("Data belum diproses. Kembali ke Preprocessing.")
        if st.button("← Preprocessing"):
            st.session_state["current_page"] = "Preprocessing"
            st.rerun()
        return

    # ── Pilih Kategori ────────────────────────────────────────
    categories = get_available_categories(clean_df)

    if categories:
        show_section_title("🏷️ Pilih Kategori untuk Pemodelan")
        selected_cat = st.selectbox(
            "Pilih program studi / kategori yang akan dianalisis:",
            options=categories,
            index=0,
            label_visibility="collapsed",
        )
    else:
        selected_cat = None

    # ── Grafik Perbandingan Semua Kategori ─────────────────────
    # clean_df SELALU punya kolom standar: periode / nilai / kategori
    if "kategori" in clean_df.columns:
        show_section_title("📉 Tren Historis Seluruh Program Studi")
        fig_multi = chart_multi_category_trend(
            clean_df,
            col_period="periode",
            col_value="nilai",
            col_category="kategori",
            title="Tren Jumlah Pendaftar per Program Studi",
        )
        st.plotly_chart(fig_multi, use_container_width=True)
        st.markdown("<br/>", unsafe_allow_html=True)

    # ── Bangun Time Series ────────────────────────────────────
    try:
        ts, frequency, s_period = build_time_series(clean_df, selected_cat)
    except Exception as e:
        show_error(f"Gagal membentuk time series: {e}")
        return

    st.session_state[SS_TIME_SERIES]       = ts
    st.session_state[SS_SELECTED_CATEGORY] = selected_cat
    st.session_state[SS_DATA_FREQUENCY]    = frequency

    # ── Ringkasan Time Series ─────────────────────────────────
    show_section_title("📊 Ringkasan Time Series")
    show_metrics_row([
        {"label": "Jumlah Observasi", "value": str(len(ts)),        "color": "#2196F3"},
        {"label": "Frekuensi Data",   "value": frequency,           "color": "#4CAF50"},
        {"label": "Periode Musiman",  "value": f"s = {s_period}",  "color": "#9C27B0"},
        {"label": "Rentang",          "value": f"{str(ts.index[0])[:10]} – {str(ts.index[-1])[:10]}", "color": "#FF9800"},
    ])

    show_success(f"Time series terbentuk: {len(ts)} observasi, frekuensi {frequency}.")

    # ── Catatan keterbatasan ──────────────────────────────────
    if len(ts) < 30:
        show_methodological_note(
            "Data historis yang tersedia masih terbatas (kurang dari 30 observasi). "
            "Model SARIMA tetap dapat digunakan sesuai fokus analisis, tetapi hasil prediksi "
            "perlu ditafsirkan sebagai estimasi awal. Pertimbangkan menggunakan data bulanan optimal sebagai pembanding."
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tabel Time Series ─────────────────────────────────────
    show_section_title("📋 Tabel Data Time Series")
    ts_df = pd.DataFrame({"periode": ts.index.astype(str), "nilai": ts.values})
    show_dataframe(ts_df, max_rows=10)

    # ── Grafik Awal ───────────────────────────────────────────
    show_section_title("📈 Tren Historis Awal")
    cat_label = f" — {selected_cat}" if selected_cat else ""
    fig = chart_historical_trend(ts, title=f"Tren Historis{cat_label}", y_label="Jumlah Pendaftar")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Preprocessing", use_container_width=True):
            st.session_state["current_page"] = "Preprocessing"
            st.rerun()
    with col2:
        if st.button("📊  Lanjut ke Analisis", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Analisis Time Series"
            st.rerun()
