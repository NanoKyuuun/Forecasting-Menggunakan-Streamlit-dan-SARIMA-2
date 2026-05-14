# ============================================================
# evaluation_page.py — Evaluasi Model (Issue 7)
# ============================================================

import streamlit as st
from src.core.evaluation import calculate_metrics
from src.ui.cards import page_header, show_metrics_row, sarima_params_card
from src.ui.messages import (
    show_warning, show_success, show_error, show_section_title,
    show_methodological_note, show_info,
)
from src.ui.charts import chart_actual_vs_fitted, chart_residuals
from src.ui.tables import show_metrics_table
from src.utils.constants import (
    SS_TIME_SERIES, SS_MODEL_RESULT, SS_SARIMA_PARAMS, SS_EVAL_METRICS,
)
from src.utils.helpers import format_number, format_percentage


def render():
    """
    M-render isi halaman 'Evaluasi Model'.
    Halaman ini bertugas untuk membuktikan secara kuantitatif apakah model SARIMA
    yang dibentuk di halaman sebelumnya layak dipakai atau tidak, 
    dengan menghitung selisih antara data asli (Aktual) dan garis prediksi (Fitted/Residuals).
    """
    page_header(
        "Evaluasi Model",
        "Penilaian performa model SARIMA menggunakan metrik MAE, MSE, RMSE, dan MAPE.",
        "📏",
    )

    # Tarik data dan hasil model dari session_state
    ts           = st.session_state.get(SS_TIME_SERIES)
    model_result = st.session_state.get(SS_MODEL_RESULT)
    sarima_params = st.session_state.get(SS_SARIMA_PARAMS)

    # Pastikan model sudah berhasil dibuat sebelumnya
    if ts is None or model_result is None:
        show_warning("Model SARIMA belum dijalankan. Kembali ke Pemodelan.")
        if st.button("← Pemodelan SARIMA"):
            st.session_state["current_page"] = "Pemodelan SARIMA"
            st.rerun()
        return

    # ── Hitung Metrik ─────────────────────────────────────────
    # Kirim data aktual (ts) dan data simulasi (fitted) untuk dihitung selisih errornya
    metrics = calculate_metrics(ts, model_result["fitted"])
    st.session_state[SS_EVAL_METRICS] = metrics

    # ── Metric Cards ──────────────────────────────────────────
    show_section_title("📊 Hasil Evaluasi Model")
    # Tampilkan error secara visual menggunakan card yang ada di ui.cards
    show_metrics_row([
        {"label": "MAE",  "value": format_number(metrics.get("MAE"),  4), "color": "#2196F3"},
        {"label": "MSE",  "value": format_number(metrics.get("MSE"),  4), "color": "#9C27B0"},
        {"label": "RMSE", "value": format_number(metrics.get("RMSE"), 4), "color": "#FF9800"},
        {"label": "MAPE", "value": f"{metrics.get('MAPE', 0):.2f}%" if metrics.get("MAPE") is not None else "—", "color": "#4CAF50"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tabel Metrik + Interpretasi ───────────────────────────
    show_section_title("📋 Detail Metrik Evaluasi")
    col_table, col_interp = st.columns([2, 1])

    with col_table:
        # Tampilkan penjelasan panjang dari masing-masing rumus MAE, MSE, dll.
        show_metrics_table(metrics)

    with col_interp:
        # Kotak penjelasan interpretasi untuk orang awam (Kurang/Cukup/Sangat Akurat)
        mape_val = metrics.get("MAPE", 0) or 0
        rmse_val = metrics.get("RMSE", 0) or 0
        interp   = metrics.get("mape_interpretation", "—")
        st.markdown(
            f"""
            <div class="sarima-card" style="height:100%;">
                <div class="metric-label">Interpretasi MAPE</div>
                <div style="font-size:1.05rem;font-weight:700;color:#1E3A5F;margin:0.5rem 0;">
                    {interp}
                </div>
                <div style="font-size:0.82rem;color:#718096;line-height:1.5;">
                    <strong>MAPE</strong> menunjukkan rata-rata persentase kesalahan prediksi.<br/>
                    <strong>RMSE</strong> menunjukkan besarnya kesalahan dalam satuan data asli ({format_number(rmse_val, 2)}).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Grafik Aktual vs Fitted ───────────────────────────────
    # Membandingkan secara visual seberapa dekat garis prediksi mengikuti garis aktual
    show_section_title("📈 Grafik Aktual vs Fitted")
    fig_avf = chart_actual_vs_fitted(ts, model_result["fitted"])
    st.plotly_chart(fig_avf, use_container_width=True)

    # ── Grafik Residual ───────────────────────────────────────
    # Residual adalah sisa error murni dari prediksi. Idealnya residual berada di sekitar garis nol (0).
    if len(model_result.get("residuals", [])) > 0:
        show_section_title("📉 Grafik Residual")
        fig_resid = chart_residuals(model_result["residuals"])
        st.plotly_chart(fig_resid, use_container_width=True)
        show_info(
            "Residual yang mendekati nol dan terdistribusi acak menunjukkan model telah menangkap "
            "pola utama dalam data dengan baik."
        )

    # ── Catatan Metodologis ───────────────────────────────────
    # Jika datanya terlalu sedikit (<= 30), ingatkan user bahwa error kecil belum tentu bagus
    # (bisa jadi cuma karena kebetulan overfitting terhadap data yg sedikit)
    if len(ts) < 30:
        show_methodological_note(
            "Nilai metrik evaluasi pada data terbatas perlu diinterpretasi dengan hati-hati. "
            "Nilai MAPE yang sangat kecil belum tentu mencerminkan performa model yang baik "
            "apabila data historis terlalu sedikit untuk menilai generalisasi model."
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Pemodelan SARIMA", use_container_width=True):
            st.session_state["current_page"] = "Pemodelan SARIMA"
            st.rerun()
    with col2:
        if st.button("🔮  Lanjut ke Forecasting", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Forecasting"
            st.rerun()
