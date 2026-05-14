# ============================================================
# conclusion_page.py — Halaman Kesimpulan (Issue 8)
# ============================================================

import streamlit as st
from src.ui.cards import page_header, show_metrics_row, sarima_params_card
from src.ui.messages import (
    show_section_title, show_methodological_note, show_warning,
    show_info, show_success,
)
from src.utils.constants import (
    SS_TIME_SERIES, SS_SARIMA_PARAMS, SS_MODEL_RESULT,
    SS_EVAL_METRICS, SS_FORECAST_RESULT, SS_SELECTED_CATEGORY,
    SS_DATA_FREQUENCY, SS_FILE_NAME,
)
from src.utils.helpers import format_number, format_percentage
from src.utils.export import build_forecast_csv, get_download_filename


def render():
    """
    M-render isi halaman 'Kesimpulan'.
    Halaman terakhir dari alur aplikasi utama. Berfungsi merangkum semua yang telah 
    terjadi dari awal (data yang dipakai, model terpilih, error yang didapat, 
    hingga hasil prediksi masa depan) dan memberikan rekomendasi penggunaan hasil.
    """
    page_header(
        "Kesimpulan",
        "Ringkasan akhir hasil analisis, evaluasi model, dan rekomendasi penggunaan forecast.",
        "📋",
    )

    # Tarik semua state penting dari memori Streamlit
    ts             = st.session_state.get(SS_TIME_SERIES)
    sarima_params  = st.session_state.get(SS_SARIMA_PARAMS)
    model_result   = st.session_state.get(SS_MODEL_RESULT)
    eval_metrics   = st.session_state.get(SS_EVAL_METRICS)
    forecast_result = st.session_state.get(SS_FORECAST_RESULT)
    category       = st.session_state.get(SS_SELECTED_CATEGORY, "—")
    frequency      = st.session_state.get(SS_DATA_FREQUENCY, "—")
    file_name      = st.session_state.get(SS_FILE_NAME, "—")

    # Cek kelengkapan
    has_model    = model_result is not None
    has_forecast = forecast_result is not None and forecast_result.get("success", False)

    # Cegah user lompat ke halaman ini jika model belum pernah dihitung
    if not has_model:
        show_warning(
            "Analisis belum selesai. Harap menyelesaikan proses dari Upload Dataset hingga Forecasting "
            "sebelum membaca kesimpulan."
        )
        if st.button("← Kembali ke Beranda"):
            st.session_state["current_page"] = "Beranda"
            st.rerun()
        return

    show_success("Analisis selesai! Berikut ringkasan hasil pemodelan SARIMA.")
    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 1. Ringkasan Dataset ──────────────────────────────────
    # Menampilkan ulang data apa yang barusan diolah
    show_section_title("📂 1. Ringkasan Dataset")
    n_obs = len(ts) if ts is not None else 0
    show_metrics_row([
        {"label": "File Dataset",      "value": file_name,             "color": "#2196F3"},
        {"label": "Kategori Analisis", "value": category or "Semua",   "color": "#9C27B0"},
        {"label": "Frekuensi Data",    "value": frequency,             "color": "#4CAF50"},
        {"label": "Jumlah Observasi",  "value": str(n_obs),            "color": "#FF9800"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 2. Model SARIMA ───────────────────────────────────────
    # Menampilkan ulang kombinasi parameter terbaik yang ditemukan
    show_section_title("🤖 2. Model SARIMA yang Digunakan")
    if sarima_params:
        col_model, col_fit = st.columns([2, 1])
        with col_model:
            sarima_params_card(sarima_params)
        with col_fit:
            show_metrics_row([
                {"label": "AIC", "value": f"{model_result.get('aic', 0):.2f}" if model_result.get("aic") else "—", "color": "#9C27B0"},
            ])
            show_metrics_row([
                {"label": "BIC", "value": f"{model_result.get('bic', 0):.2f}" if model_result.get("bic") else "—", "color": "#FF9800"},
            ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 3. Evaluasi Model ─────────────────────────────────────
    # Menampilkan tingkat error (MAE, RMSE, MAPE)
    show_section_title("📏 3. Evaluasi Model")
    if eval_metrics:
        show_metrics_row([
            {"label": "MAE",  "value": format_number(eval_metrics.get("MAE"),  4), "color": "#2196F3"},
            {"label": "RMSE", "value": format_number(eval_metrics.get("RMSE"), 4), "color": "#FF9800"},
            {"label": "MAPE", "value": f"{eval_metrics.get('MAPE', 0):.2f}%",     "color": "#4CAF50"},
            {"label": "Interpretasi", "value": eval_metrics.get("mape_interpretation", "—"), "color": "#9C27B0"},
        ])
    else:
        show_info("Evaluasi model belum dilakukan. Kembali ke halaman Evaluasi Model.")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 4. Hasil Forecast ─────────────────────────────────────
    # Menampilkan kesimpulan masa depan (angka prediksi pertama dan terakhir)
    show_section_title("🔮 4. Hasil Forecast")
    if has_forecast:
        forecast_df = forecast_result["forecast_df"]
        forecast_mean = forecast_result["forecast_mean"]

        col_fc_a, col_fc_b = st.columns(2)
        with col_fc_a:
            first_val = float(forecast_mean.iloc[0]) if len(forecast_mean) > 0 else 0
            last_val  = float(forecast_mean.iloc[-1]) if len(forecast_mean) > 0 else 0
            st.markdown(
                f"""
                <div class="sarima-card">
                    <div class="metric-label">Periode Pertama Forecast</div>
                    <div style="font-size:1.5rem;font-weight:700;color:#2196F3;">
                        {format_number(first_val, 0)}
                    </div>
                    <div class="metric-sub">Estimasi nilai pada periode pertama</div>
                    <br/>
                    <div class="metric-label">Periode Terakhir Forecast</div>
                    <div style="font-size:1.5rem;font-weight:700;color:#4CAF50;">
                        {format_number(last_val, 0)}
                    </div>
                    <div class="metric-sub">Estimasi nilai pada periode terakhir</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_fc_b:
            st.dataframe(
                forecast_df.head(6).rename(columns={
                    "periode": "Periode", "prediksi": "Prediksi",
                    "batas_bawah": "Batas Bawah", "batas_atas": "Batas Atas",
                }),
                use_container_width=True,
                hide_index=True,
            )
    else:
        show_info("Forecast belum dijalankan. Kembali ke halaman Forecasting.")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 5. Narasi Kesimpulan ──────────────────────────────────
    # Merangkai kalimat otomatis berdasarkan kombinasi parameter dan evaluasi (Auto-generated Text)
    show_section_title("📝 5. Narasi Kesimpulan")
    mape_str = f"{eval_metrics.get('MAPE', 0):.2f}%" if eval_metrics else "—"
    rmse_str = format_number(eval_metrics.get("RMSE"), 2) if eval_metrics else "—"
    p_str = sarima_params.get("p", "?") if sarima_params else "?"
    d_str = sarima_params.get("d", "?") if sarima_params else "?"
    q_str = sarima_params.get("q", "?") if sarima_params else "?"
    P_str = sarima_params.get("P", "?") if sarima_params else "?"
    D_str = sarima_params.get("D", "?") if sarima_params else "?"
    Q_str = sarima_params.get("Q", "?") if sarima_params else "?"
    s_str = sarima_params.get("s", "?") if sarima_params else "?"

    narasi = (
        f"Berdasarkan data historis {file_name} yang digunakan dengan {n_obs} observasi "
        f"pada kategori <strong>{category}</strong> berfrekuensi <strong>{frequency}</strong>, "
        f"model <strong>SARIMA({p_str},{d_str},{q_str})({P_str},{D_str},{Q_str})[{s_str}]</strong> "
        f"telah dijalankan dan menghasilkan nilai evaluasi MAPE sebesar <strong>{mape_str}</strong> "
        f"dengan RMSE sebesar <strong>{rmse_str}</strong>. "
        f"Model ini kemudian digunakan untuk menghasilkan forecast pada periode mendatang."
    )

    if n_obs < 30:
        narasi += (
            f"<br/><br/>Karena jumlah observasi historis masih terbatas ({n_obs} observasi), "
            f"hasil forecast perlu dipahami sebagai <strong>estimasi awal</strong>. "
            f"Penggunaan data bulanan dengan jumlah observasi lebih banyak dapat memberikan "
            f"dasar pemodelan yang lebih kuat."
        )

    st.markdown(
        f'<div class="sarima-card"><p style="color:#4a5568;line-height:1.8;margin:0;">{narasi}</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 6. Catatan Keterbatasan ───────────────────────────────
    show_section_title("⚠️ 6. Catatan Keterbatasan")
    show_methodological_note(
        "Hasil forecast pada aplikasi ini dihasilkan berdasarkan pola historis data yang tersedia. "
        "Aplikasi tidak menjamin keakuratan prediksi untuk kondisi nyata yang dapat dipengaruhi "
        "oleh faktor-faktor di luar pola historis. Data simulasi yang digunakan sebagai pembanding "
        "tidak merepresentasikan data empiris resmi dari institusi terkait."
    )

    # ── 7. Rekomendasi ────────────────────────────────────────
    show_section_title("💡 7. Rekomendasi Penggunaan")
    st.markdown(
        """
        <div class="sarima-card">
            <ol style="color:#4a5568;line-height:2;margin:0;padding-left:1.2rem;">
                <li>Gunakan hasil forecast sebagai <strong>referensi awal</strong>, bukan keputusan final.</li>
                <li>Lengkapi dengan data empiris yang lebih panjang untuk hasil yang lebih akurat.</li>
                <li>Pertimbangkan faktor eksternal (kebijakan, tren industri) dalam interpretasi.</li>
                <li>Bandingkan hasil SARIMA dengan metode lain jika tersedia data yang cukup.</li>
                <li>Perbarui model secara berkala saat data historis baru tersedia.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Download Akhir ────────────────────────────────────────
    # Tombol download di paling bawah halaman untuk mengambil laporan final
    if has_forecast and sarima_params:
        show_section_title("📥 Download Hasil Forecast")
        csv_bytes = build_forecast_csv(
            forecast_result["forecast_df"], sarima_params, category or "Data"
        )
        filename = get_download_filename(category or "Data")
        st.download_button(
            label="⬇️ Download Hasil Forecast (CSV)",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
            use_container_width=False,
            type="primary",
        )

    # ── Navigasi ──────────────────────────────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Perbandingan Dataset", use_container_width=True):
            st.session_state["current_page"] = "Perbandingan Dataset"
            st.rerun()
    with col2:
        if st.button("🏠  Kembali ke Beranda", use_container_width=True):
            st.session_state["current_page"] = "Beranda"
            st.rerun()
