# ============================================================
# comparison_page.py — Perbandingan Dataset (Issue 8)
# ============================================================

import streamlit as st
import pandas as pd
from src.core.data_loader import load_file
from src.core.preprocessing import preprocess
from src.core.transformation import build_time_series
from src.core.sarima_model import fit_sarima
from src.core.evaluation import calculate_metrics
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import (
    show_section_title, show_simulation_note, show_info,
    show_methodological_note, show_warning,
)
from src.ui.charts import chart_comparison, chart_historical_trend
from src.utils.constants import SAMPLE_BULANAN_10, SS_TIME_SERIES, SS_SELECTED_CATEGORY, SS_DATA_FREQUENCY
from src.utils.helpers import format_number, format_percentage, get_data_quality_label, get_seasonal_period


@st.cache_data(show_spinner=False)
def _load_reference_data():
    """Load dataset ideal (bulanan) sebagai referensi perbandingan."""
    try:
        df = pd.read_csv(SAMPLE_BULANAN_10, encoding="utf-8")
        clean, _ = preprocess(df, "tanggal", "jumlah_pendaftar", "program_studi")
        # Ambil satu kategori representatif (Akuntansi biasanya pertama)
        cats = clean["kategori"].unique() if "kategori" in clean.columns else []
        cat  = cats[0] if len(cats) > 0 else None
        ts, freq, s = build_time_series(clean, cat)
        return {
            "df":       clean,
            "ts":       ts,
            "freq":     freq,
            "s":        s,
            "category": cat,
            "n_obs":    len(ts),
        }
    except Exception as e:
        return {"error": str(e)}


def _run_model_for_series(ts, s):
    """Fit SARIMA sederhana untuk perbandingan cepat."""
    try:
        r = fit_sarima(ts, (1, 1, 0), (0, 0, 0, s))
        if r["success"]:
            from src.core.evaluation import calculate_metrics
            m = calculate_metrics(ts, r["fitted"])
            return r, m
    except Exception:
        pass
    return None, None


def render():
    page_header(
        "Perbandingan Dataset",
        "Membandingkan kualitas data yang sedang kamu analisis dengan standar data ideal.",
        "⚖️",
    )

    ts_user = st.session_state.get(SS_TIME_SERIES)
    cat_user = st.session_state.get(SS_SELECTED_CATEGORY, "Keseluruhan")
    freq_user = st.session_state.get(SS_DATA_FREQUENCY, "—")

    if ts_user is None:
        show_warning("Belum ada data time series yang aktif. Silakan selesaikan tahap Transformasi terlebih dahulu.")
        if st.button("← Kembali ke Transformasi"):
            st.session_state["current_page"] = "Transformasi Time Series"
            st.rerun()
        return

    s_user = get_seasonal_period(freq_user)

    # ── Load Data Referensi ───────────────────────────────────
    with st.spinner("Memuat dataset referensi..."):
        ref = _load_reference_data()

    # ── Kartu Penjelasan Dua Skenario ─────────────────────────
    show_section_title("📂 Perbandingan Data")
    col_a, col_b = st.columns(2)

    with col_a:
        n_user = len(ts_user)
        ql_u, ql_level_u = get_data_quality_label(n_user)
        color_u = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}.get(ql_level_u, "#2196F3")
        icon_u = "⚠️" if ql_level_u in ["warning", "danger"] else "✅"
        
        st.markdown(
            f"""
            <div class="sarima-card" style="border-left:4px solid {color_u};">
                <div style="font-weight:800;font-size:1.1rem;color:#1E3A5F;margin-bottom:0.7rem;">
                    {icon_u} Data Saat Ini (Diunggah)
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.88rem;">
                    <div><strong>Kategori:</strong> {cat_user}</div>
                    <div><strong>Observasi:</strong> {n_user}</div>
                    <div><strong>Frekuensi:</strong> {freq_user}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_u}">{ql_u}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Data yang sedang kamu kerjakan saat ini. Jika observasi terbatas, 
                    SARIMA mungkin kesulitan menangkap pola musiman dengan baik.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        n_ref = ref.get("n_obs", 0)
        ql_r, ql_level_r = get_data_quality_label(n_ref)
        color_r = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}.get(ql_level_r, "#4CAF50")
        st.markdown(
            f"""
            <div class="sarima-card" style="border-left:4px solid {color_r};">
                <div style="font-weight:800;font-size:1.1rem;color:#1E3A5F;margin-bottom:0.7rem;">
                    🌟 Data Ideal (Referensi)
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.88rem;">
                    <div><strong>Kategori:</strong> {ref.get('category', '—')}</div>
                    <div><strong>Observasi:</strong> {n_ref}</div>
                    <div><strong>Frekuensi:</strong> {ref.get('freq', '—')}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_r}">{ql_r}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Dataset standar sistem (10 Tahun Bulanan). Memiliki cukup observasi 
                    untuk membentuk pola tren dan musiman yang solid pada SARIMA.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Perbandingan Jumlah Observasi ─────────────────────────
    show_section_title("📊 Perbandingan Jumlah Observasi")
    show_metrics_row([
        {"label": "Obs. Data Saat Ini",    "value": str(n_user), "color": color_u},
        {"label": "Obs. Data Ideal",       "value": str(n_ref), "color": color_r},
        {"label": "Selisih Observasi",     "value": str(n_ref - n_user), "color": "#2196F3"},
        {"label": "Rasio Observasi",       "value": f"{n_ref / max(n_user, 1):.1f}x", "color": "#9C27B0"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Visualisasi Tren Masing-masing Data ───────────────────
    show_section_title("📈 Visualisasi Tren Masing-masing Dataset")
    col_c, col_d = st.columns(2)

    with col_c:
        fig_u = chart_historical_trend(ts_user, title=f"Tren Saat Ini — {cat_user}", y_label="Nilai")
        st.plotly_chart(fig_u, use_container_width=True)

    with col_d:
        ts_ref = ref.get("ts")
        if ts_ref is not None and len(ts_ref) > 0:
            fig_r = chart_historical_trend(ts_ref, title=f"Tren Referensi — {ref.get('category', '')}", y_label="Nilai")
            st.plotly_chart(fig_r, use_container_width=True)
        else:
            st.warning(f"Data referensi tidak dapat dimuat: {ref.get('error', '')}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Perbandingan Evaluasi Model ───────────────────────────
    show_section_title("📏 Perbandingan Metrik Evaluasi Model")
    show_info("Model SARIMA berjalan di latar belakang untuk membandingkan seberapa akurat prediksi pada data saat ini vs data ideal.")

    with st.spinner("Menjalankan pemodelan untuk perbandingan..."):
        res_u, metrics_u = _run_model_for_series(ts_user, s_user)
        res_r, metrics_r = _run_model_for_series(ts_ref, ref.get("s", 12)) if ts_ref is not None else (None, None)

    if metrics_u and metrics_r:
        comparison_rows = [
            ("MAE",  format_number(metrics_u.get("MAE"), 2),  format_number(metrics_r.get("MAE"), 2)),
            ("MSE",  format_number(metrics_u.get("MSE"), 2),  format_number(metrics_r.get("MSE"), 2)),
            ("RMSE", format_number(metrics_u.get("RMSE"), 2), format_number(metrics_r.get("RMSE"), 2)),
            ("MAPE", f"{metrics_u.get('MAPE', 0):.2f}%",      f"{metrics_r.get('MAPE', 0):.2f}%"),
        ]
        
        # Highlight mana yang lebih baik (lebih kecil lebih baik)
        def highlight(val_u, val_r):
            # Simplifikasi perbandingan dengan mengambil angka mentah (buang %, titik, koma)
            try:
                num_u = float(val_u.replace('%','').replace(',',''))
                num_r = float(val_r.replace('%','').replace(',',''))
                if num_u < num_r:
                    return f'<td style="padding:0.6rem 1rem;color:#4CAF50;text-align:center;font-weight:700;">{val_u}</td><td style="padding:0.6rem 1rem;color:#718096;text-align:center;">{val_r}</td>'
                else:
                    return f'<td style="padding:0.6rem 1rem;color:#718096;text-align:center;">{val_u}</td><td style="padding:0.6rem 1rem;color:#4CAF50;text-align:center;font-weight:700;">{val_r}</td>'
            except:
                return f'<td style="padding:0.6rem 1rem;text-align:center;">{val_u}</td><td style="padding:0.6rem 1rem;text-align:center;">{val_r}</td>'

        rows_html = "".join(
            f"""<tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
                <td style="padding:0.6rem 1rem;font-weight:700;color:#1E3A5F;">{r[0]}</td>
                {highlight(r[1], r[2])}
            </tr>"""
            for r in comparison_rows
        )
        st.markdown(
            f"""
            <div class="sarima-card">
            <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
                <thead>
                    <tr style="background:#1E3A5F;color:white;">
                        <th style="padding:0.65rem 1rem;text-align:left;">Metrik Error</th>
                        <th style="padding:0.65rem 1rem;text-align:center;">Data Saat Ini (Diunggah)</th>
                        <th style="padding:0.65rem 1rem;text-align:center;">Data Ideal (Referensi)</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            <div style="font-size:0.8rem;color:#718096;margin-top:10px;text-align:center;">
                * Nilai yang berwarna hijau dan lebih tebal menunjukkan tingkat error yang lebih kecil (Lebih Akurat).
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        show_warning("Model gagal hội tụ (converge) pada salah satu dataset, metrik tidak dapat dibandingkan.")

    # ── Interpretasi ─────────────────────────────────────────
    show_section_title("🔍 Interpretasi Perbandingan")
    
    # Berikan interpretasi dinamis berdasarkan observasi
    if n_user >= 30:
        interpretasi_text = "Data yang kamu gunakan saat ini sudah memiliki jumlah observasi yang cukup memadai (Mirip dengan dataset referensi). Model SARIMA seharusnya bisa mengenali pola historis dengan sangat baik."
    else:
        interpretasi_text = "Data yang kamu gunakan saat ini memiliki observasi yang terbatas jika dibandingkan dengan data referensi ideal (10 Tahun). Oleh karena itu, metrik error pada data kamu mungkin sedikit lebih tinggi karena model kesulitan menangkap siklus musiman jangka panjang."
        
    st.markdown(
        f"""
        <div class="sarima-card">
            <p style="color:#4a5568;line-height:1.8;margin:0;">
                {interpretasi_text} <br/><br/>
                Perbandingan ini membuktikan bahwa <em>kualitas dan kuantitas data sangat memengaruhi akurasi hasil akhir model peramalan SARIMA</em>. 
                Semakin panjang rentang waktu datanya, semakin cerdas model dalam memprediksi masa depan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Forecasting", use_container_width=True):
            st.session_state["current_page"] = "Forecasting"
            st.rerun()
    with col2:
        if st.button("📋  Lanjut ke Kesimpulan", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Kesimpulan"
            st.rerun()
