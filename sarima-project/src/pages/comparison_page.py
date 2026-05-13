# ============================================================
# comparison_page.py — Perbandingan Dataset (Issue 8)
# ============================================================

import streamlit as st
import pandas as pd
from src.core.preprocessing import preprocess
from src.core.transformation import build_time_series
from src.core.sarima_model import fit_sarima
from src.core.evaluation import calculate_metrics
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import (
    show_section_title, show_info, show_warning,
)
from src.ui.charts import chart_multi_category_trend, chart_historical_trend
from src.utils.constants import (
    SAMPLE_BULANAN_10,
    SS_TIME_SERIES, SS_SELECTED_CATEGORY, SS_DATA_FREQUENCY, SS_CLEAN_DATA,
)
from src.utils.helpers import format_number, get_data_quality_label, get_seasonal_period


@st.cache_data(show_spinner=False)
def _load_reference_data():
    """Load dataset ideal (bulanan 10 tahun) sebagai referensi perbandingan."""
    try:
        df = pd.read_csv(SAMPLE_BULANAN_10, encoding="utf-8")
        clean, _ = preprocess(df, "tanggal", "jumlah_pendaftar", "program_studi")
        cats = clean["kategori"].unique().tolist() if "kategori" in clean.columns else []
        # Bangun ts untuk satu kategori (untuk evaluasi model)
        cat  = cats[0] if cats else None
        ts, freq, s = build_time_series(clean, cat)
        return {
            "df":       clean,          # <── full dataframe, semua prodi
            "ts":       ts,             # <── satu kategori untuk evaluasi
            "freq":     freq,
            "s":        s,
            "category": cat,
            "n_cats":   len(cats),
            "n_obs_per_cat": len(ts),   # observasi per kategori
            "n_obs_total": len(clean),  # total baris
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
        clean_user = st.session_state.get(SS_CLEAN_DATA)
        n_cats_user = clean_user["kategori"].nunique() if (clean_user is not None and "kategori" in clean_user.columns) else 1
        n_obs_total_user = len(clean_user) if clean_user is not None else n_user
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
                    <div><strong>Program Studi:</strong> {n_cats_user} prodi</div>
                    <div><strong>Obs./Prodi:</strong> {n_user}</div>
                    <div><strong>Frekuensi:</strong> {freq_user}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_u}">{ql_u}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Data yang sedang kamu kerjakan. Kategori dipilih: <strong>{cat_user}</strong>.
                    Jika observasi per prodi terbatas, SARIMA mungkin kesulitan menangkap pola musiman.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        n_ref_per_cat = ref.get("n_obs_per_cat", ref.get("n_obs", 0))
        n_ref_cats    = ref.get("n_cats", 1)
        ql_r, ql_level_r = get_data_quality_label(n_ref_per_cat)
        color_r = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}.get(ql_level_r, "#4CAF50")
        st.markdown(
            f"""
            <div class="sarima-card" style="border-left:4px solid {color_r};">
                <div style="font-weight:800;font-size:1.1rem;color:#1E3A5F;margin-bottom:0.7rem;">
                    🌟 Data Ideal (Referensi 10 Tahun)
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.88rem;">
                    <div><strong>Program Studi:</strong> {n_ref_cats} prodi</div>
                    <div><strong>Obs./Prodi:</strong> {n_ref_per_cat}</div>
                    <div><strong>Frekuensi:</strong> {ref.get('freq', '—')}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_r}">{ql_r}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Dataset standar sistem (10 Tahun Bulanan). Memiliki 120 observasi per prodi —
                    cukup untuk mendeteksi pola musiman yang solid pada SARIMA.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Perbandingan Jumlah Observasi ─────────────────────────
    show_section_title("📊 Perbandingan Jumlah Observasi")
    show_metrics_row([
        {"label": "Obs./Prodi (Saat Ini)",  "value": str(n_user),              "color": color_u},
        {"label": "Obs./Prodi (Ideal)",     "value": str(n_ref_per_cat),       "color": color_r},
        {"label": "Selisih Observasi",      "value": str(n_ref_per_cat - n_user), "color": "#2196F3"},
        {"label": "Rasio Observasi",        "value": f"{n_ref_per_cat / max(n_user, 1):.1f}x", "color": "#9C27B0"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Visualisasi Tren: SEMUA PRODI per sisi ──────────────────
    show_section_title("📈 Visualisasi Tren Seluruh Program Studi")
    show_info("💡 Setiap garis mewakili satu Program Studi. Perhatikan perbedaan skala waktu dan kepadatan data antara kedua dataset.")
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("**⏰ Data Diunggah (Semua Prodi)**")
        clean_user = st.session_state.get(SS_CLEAN_DATA)
        if clean_user is not None and "kategori" in clean_user.columns:
            fig_u = chart_multi_category_trend(
                clean_user, col_period="periode", col_value="nilai", col_category="kategori",
                title=f"Tren Data Diunggah ({freq_user})",
            )
            st.plotly_chart(fig_u, use_container_width=True)
        else:
            fig_u = chart_historical_trend(ts_user, title=f"Tren — {cat_user}", y_label="Nilai")
            st.plotly_chart(fig_u, use_container_width=True)

    with col_d:
        st.markdown("**🌟 Data Referensi Ideal (Semua Prodi, 10 Tahun)**")
        ref_df = ref.get("df")
        if ref_df is not None and "kategori" in ref_df.columns:
            fig_r = chart_multi_category_trend(
                ref_df, col_period="periode", col_value="nilai", col_category="kategori",
                title="Tren Data Referensi (Bulanan, 10 Tahun)",
            )
            st.plotly_chart(fig_r, use_container_width=True)
        else:
            ts_ref = ref.get("ts")
            if ts_ref is not None:
                fig_r = chart_historical_trend(ts_ref, title="Tren Referensi", y_label="Nilai")
                st.plotly_chart(fig_r, use_container_width=True)
            else:
                st.warning(f"Data referensi tidak dapat dimuat: {ref.get('error', '')}")

    # ts_ref untuk evaluasi model di bawah
    ts_ref = ref.get("ts")


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
