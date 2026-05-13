# ============================================================
# forecasting_page.py — Halaman Forecasting (Issue 7)
# ============================================================

import streamlit as st
import pandas as pd
from src.core.forecasting import generate_forecast
from src.utils.export import build_forecast_csv, get_download_filename
from src.ui.cards import page_header, show_metrics_row, sarima_params_card
from src.ui.messages import (
    show_warning, show_success, show_error, show_section_title,
    show_methodological_note, show_info, show_simulation_note,
)
from src.ui.charts import chart_forecast
from src.ui.tables import show_forecast_table
from src.utils.constants import (
    SS_TIME_SERIES, SS_MODEL_RESULT, SS_SARIMA_PARAMS,
    SS_SELECTED_CATEGORY, SS_FORECAST_RESULT,
)
from src.utils.helpers import format_number, get_seasonal_period


def render():
    page_header(
        "Forecasting",
        "Prediksi nilai untuk periode mendatang berdasarkan model SARIMA yang telah dilatih.",
        "🔮",
    )

    ts            = st.session_state.get(SS_TIME_SERIES)
    model_result  = st.session_state.get(SS_MODEL_RESULT)
    sarima_params = st.session_state.get(SS_SARIMA_PARAMS)
    category      = st.session_state.get(SS_SELECTED_CATEGORY, "Data")

    if ts is None or model_result is None:
        show_warning("Model SARIMA belum tersedia. Kembali ke Pemodelan.")
        if st.button("← Pemodelan SARIMA"):
            st.session_state["current_page"] = "Pemodelan SARIMA"
            st.rerun()
        return

    # ── Konfigurasi Forecast ──────────────────────────────────
    show_section_title("⚙️ Konfigurasi Forecast")
    col_param, col_info = st.columns([2, 3])

    with col_param:
        n_periods = st.slider(
            "Jumlah Periode Forecast",
            min_value=1,
            max_value=24,
            value=6,
            help="Pilih berapa periode ke depan yang ingin diprediksi.",
        )

    with col_info:
        if sarima_params:
            sarima_params_card(sarima_params)

    run_btn = st.button("🚀 Generate Forecast", type="primary", use_container_width=False)

    if run_btn or st.session_state.get(SS_FORECAST_RESULT) is not None:
        # Generate jika belum ada atau tombol ditekan
        if run_btn:
            with st.spinner("Menghasilkan prediksi..."):
                forecast_result = generate_forecast(model_result, n_periods)
            st.session_state[SS_FORECAST_RESULT] = forecast_result
        else:
            forecast_result = st.session_state.get(SS_FORECAST_RESULT)

        if not forecast_result or not forecast_result.get("success"):
            show_error(f"Gagal menghasilkan forecast: {forecast_result.get('error', 'Unknown error')}")
            return

        show_success(f"Forecast berhasil dihasilkan untuk {n_periods} periode ke depan!")

        forecast_df   = forecast_result["forecast_df"]
        forecast_mean = forecast_result["forecast_mean"]
        forecast_lower = forecast_result["forecast_lower"]
        forecast_upper = forecast_result["forecast_upper"]

        # ── Ringkasan Forecast ────────────────────────────────
        show_section_title("📊 Ringkasan Forecast")
        first_val = float(forecast_mean.iloc[0]) if len(forecast_mean) > 0 else 0
        last_val  = float(forecast_mean.iloc[-1]) if len(forecast_mean) > 0 else 0
        show_metrics_row([
            {"label": "Periode Forecast", "value": str(n_periods),              "color": "#2196F3"},
            {"label": "Nilai Awal",       "value": format_number(first_val, 0), "color": "#4CAF50"},
            {"label": "Nilai Akhir",      "value": format_number(last_val, 0),  "color": "#FF9800"},
            {"label": "Kategori",         "value": str(category or "—"),        "color": "#9C27B0"},
        ])

        st.markdown("<br/>", unsafe_allow_html=True)

        # ── Grafik Forecast ───────────────────────────────────
        show_section_title("📈 Grafik Aktual + Forecast")
        fig = chart_forecast(
            actual=ts,
            forecast_mean=forecast_mean,
            forecast_lower=forecast_lower,
            forecast_upper=forecast_upper,
            title=f"Forecasting — {category or 'Data'}",
            y_label="Nilai",
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Tabel Forecast ────────────────────────────────────
        show_section_title("📋 Tabel Hasil Forecast")
        display_df = forecast_df.copy()
        display_df.columns = ["Periode", "Prediksi", "Batas Bawah", "Batas Atas"]
        show_forecast_table(display_df)

        # ── Download CSV ──────────────────────────────────────
        show_section_title("📥 Export Hasil Forecast")
        if sarima_params:
            csv_bytes = build_forecast_csv(forecast_df, sarima_params, category or "Data")
            filename  = get_download_filename(category or "Data")
            st.download_button(
                label="⬇️ Download Hasil Forecast (CSV)",
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
                use_container_width=False,
            )

        # ── Catatan Metodologis ───────────────────────────────
        if len(ts) < 30:
            show_methodological_note(
                "Berdasarkan data historis yang tersedia, hasil forecast ini merupakan estimasi awal. "
                "Dengan jumlah observasi yang masih terbatas, interval kepercayaan yang lebih lebar "
                "menunjukkan ketidakpastian prediksi yang lebih tinggi."
            )

        st.markdown("<br/>", unsafe_allow_html=True)

        # ── Navigasi ──────────────────────────────────────────
        col1, col2, _ = st.columns([2, 2, 2])
        with col1:
            if st.button("← Evaluasi Model", use_container_width=True):
                st.session_state["current_page"] = "Evaluasi Model"
                st.rerun()
        with col2:
            if st.button("⚖️  Lanjut ke Perbandingan Dataset", type="primary", use_container_width=True):
                st.session_state["current_page"] = "Perbandingan Dataset"
                st.rerun()
