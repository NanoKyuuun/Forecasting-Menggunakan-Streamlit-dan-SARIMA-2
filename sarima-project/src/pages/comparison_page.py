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
from src.utils.constants import SAMPLE_TAHUNAN, SAMPLE_BULANAN_10
from src.utils.helpers import format_number, format_percentage, get_data_quality_label


@st.cache_data(show_spinner=False)
def _load_sample_data():
    """Load dan proses kedua dataset sampel secara cached."""
    results = {}

    for key, path, col_p, col_v, col_c in [
        ("tahunan", SAMPLE_TAHUNAN, "tahun", "jumlah_pendaftar", "prodi"),
        ("bulanan",  SAMPLE_BULANAN_10, "tanggal", "jumlah_pendaftar", "program_studi"),
    ]:
        try:
            df = pd.read_csv(path, encoding="utf-8")
            clean, _ = preprocess(df, col_p, col_v, col_c)
            # Ambil satu kategori representatif
            cats = clean["kategori"].unique() if "kategori" in clean.columns else []
            cat  = cats[0] if len(cats) > 0 else None
            ts, freq, s = build_time_series(clean, cat)
            results[key] = {
                "df":       clean,
                "ts":       ts,
                "freq":     freq,
                "s":        s,
                "category": cat,
                "n_obs":    len(ts),
            }
        except Exception as e:
            results[key] = {"error": str(e)}

    return results


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
        "Membandingkan performa model pada data tahunan (terbatas) vs data bulanan (optimal).",
        "⚖️",
    )

    show_simulation_note()
    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Load Data ─────────────────────────────────────────────
    with st.spinner("Memuat dataset sampel..."):
        data = _load_sample_data()

    tahunan = data.get("tahunan", {})
    bulanan  = data.get("bulanan", {})

    # ── Kartu Penjelasan Dua Skenario ─────────────────────────
    show_section_title("📂 Dua Skenario Data")
    col_a, col_b = st.columns(2)

    with col_a:
        n_t = tahunan.get("n_obs", 0)
        ql_t, ql_level_t = get_data_quality_label(n_t)
        color_t = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}.get(ql_level_t, "#2196F3")
        st.markdown(
            f"""
            <div class="sarima-card" style="border-left:4px solid {color_t};">
                <div style="font-weight:800;font-size:1.1rem;color:#1E3A5F;margin-bottom:0.7rem;">
                    ⚠️ Data Tahunan (Belum Optimal)
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.88rem;">
                    <div><strong>Sumber:</strong> data_tahunan_per_prodi.csv</div>
                    <div><strong>Observasi:</strong> {n_t} (per kategori)</div>
                    <div><strong>Frekuensi:</strong> {tahunan.get('freq', '—')}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_t}">{ql_t}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Data empiris periode 2021–2025. Observasi sangat terbatas,
                    tidak ideal untuk menangkap pola musiman SARIMA.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        n_b = bulanan.get("n_obs", 0)
        ql_b, ql_level_b = get_data_quality_label(n_b)
        color_b = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}.get(ql_level_b, "#4CAF50")
        st.markdown(
            f"""
            <div class="sarima-card" style="border-left:4px solid {color_b};">
                <div style="font-weight:800;font-size:1.1rem;color:#1E3A5F;margin-bottom:0.7rem;">
                    ✅ Data Bulanan (Optimal)
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.88rem;">
                    <div><strong>Sumber:</strong> Data_Optimal_..._10Tahun.csv</div>
                    <div><strong>Observasi:</strong> {n_b} (per kategori)</div>
                    <div><strong>Frekuensi:</strong> {bulanan.get('freq', '—')}</div>
                    <div><strong>Kualitas:</strong> <span class="badge badge-{ql_level_b}">{ql_b}</span></div>
                </div>
                <div style="font-size:0.82rem;color:#718096;margin-top:0.8rem;">
                    Data simulasi untuk pengujian SARIMA. Mencakup 10 tahun bulanan,
                    lebih sesuai untuk mendeteksi pola musiman.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Perbandingan Jumlah Observasi ─────────────────────────
    show_section_title("📊 Perbandingan Jumlah Observasi")
    show_metrics_row([
        {"label": "Obs. Data Tahunan",     "value": str(tahunan.get("n_obs", "—")), "color": "#FF9800"},
        {"label": "Obs. Data Bulanan",     "value": str(bulanan.get("n_obs", "—")), "color": "#4CAF50"},
        {"label": "Selisih Observasi",     "value": str(bulanan.get("n_obs", 0) - tahunan.get("n_obs", 0)), "color": "#2196F3"},
        {"label": "Rasio Observasi",       "value": f"{bulanan.get('n_obs', 1) / max(tahunan.get('n_obs', 1), 1):.1f}x", "color": "#9C27B0"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Visualisasi Tren Masing-masing Data ───────────────────
    show_section_title("📈 Visualisasi Tren Masing-masing Dataset")
    col_c, col_d = st.columns(2)

    ts_t = tahunan.get("ts")
    ts_b = bulanan.get("ts")

    with col_c:
        if ts_t is not None and len(ts_t) > 0:
            fig_t = chart_historical_trend(ts_t, title=f"Tren Data Tahunan — {tahunan.get('category', '')}", y_label="Jumlah Pendaftar")
            st.plotly_chart(fig_t, use_container_width=True)
        else:
            st.warning(f"Data tahunan tidak dapat dimuat: {tahunan.get('error', '')}")

    with col_d:
        if ts_b is not None and len(ts_b) > 0:
            fig_b = chart_historical_trend(ts_b, title=f"Tren Data Bulanan — {bulanan.get('category', '')}", y_label="Jumlah Pendaftar")
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.warning(f"Data bulanan tidak dapat dimuat: {bulanan.get('error', '')}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Perbandingan Evaluasi Model ───────────────────────────
    show_section_title("📏 Perbandingan Metrik Evaluasi Model")
    show_info("Model SARIMA sederhana (1,1,0)(0,0,0)[s] dijalankan pada masing-masing dataset untuk perbandingan evaluasi.")

    with st.spinner("Menjalankan model untuk perbandingan..."):
        res_t, metrics_t = _run_model_for_series(ts_t, tahunan.get("s", 1)) if ts_t is not None else (None, None)
        res_b, metrics_b = _run_model_for_series(ts_b, bulanan.get("s", 12)) if ts_b is not None else (None, None)

    if metrics_t and metrics_b:
        comparison_rows = [
            ("MAE",  format_number(metrics_t.get("MAE"), 2),  format_number(metrics_b.get("MAE"), 2)),
            ("MSE",  format_number(metrics_t.get("MSE"), 2),  format_number(metrics_b.get("MSE"), 2)),
            ("RMSE", format_number(metrics_t.get("RMSE"), 2), format_number(metrics_b.get("RMSE"), 2)),
            ("MAPE", f"{metrics_t.get('MAPE', 0):.2f}%",      f"{metrics_b.get('MAPE', 0):.2f}%"),
        ]
        rows_html = "".join(
            f"""<tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
                <td style="padding:0.6rem 1rem;font-weight:700;color:#1E3A5F;">{r[0]}</td>
                <td style="padding:0.6rem 1rem;color:#FF9800;text-align:center;">{r[1]}</td>
                <td style="padding:0.6rem 1rem;color:#4CAF50;text-align:center;">{r[2]}</td>
            </tr>"""
            for r in comparison_rows
        )
        st.markdown(
            f"""
            <div class="sarima-card">
            <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
                <thead>
                    <tr style="background:#1E3A5F;color:white;">
                        <th style="padding:0.65rem 1rem;text-align:left;">Metrik</th>
                        <th style="padding:0.65rem 1rem;text-align:center;">Data Tahunan</th>
                        <th style="padding:0.65rem 1rem;text-align:center;">Data Bulanan</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Interpretasi ─────────────────────────────────────────
    show_section_title("🔍 Interpretasi Perbandingan")
    st.markdown(
        """
        <div class="sarima-card">
            <p style="color:#4a5568;line-height:1.8;margin:0;">
                Perbandingan di atas menunjukkan perbedaan performa model SARIMA ketika dijalankan pada
                dua jenis dataset yang berbeda struktur.<br/><br/>
                <strong>Data tahunan 5 tahun</strong> memiliki observasi yang sangat terbatas,
                sehingga model SARIMA tidak dapat menangkap pola musiman secara optimal.
                Hasil evaluasi dan prediksi harus dibaca sebagai estimasi awal.<br/><br/>
                <strong>Data bulanan optimal</strong> (data simulasi) memiliki lebih banyak observasi,
                memungkinkan model untuk mengidentifikasi pola tren dan musiman dengan lebih baik.
                Ini menunjukkan bahwa <em>kualitas dan jumlah data sangat memengaruhi hasil model SARIMA</em>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    show_methodological_note(
        "Data bulanan yang digunakan dalam halaman ini adalah data simulasi pembanding, "
        "bukan data empiris resmi. Perbandingan ini bertujuan untuk mendemonstrasikan "
        "pengaruh struktur data terhadap kualitas pemodelan SARIMA."
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
