# ============================================================
# home_page.py — Halaman Beranda (Issue 1)
# ============================================================

import streamlit as st
from src.utils.constants import PAGE_ORDER, PAGE_ICONS, APP_TITLE, APP_AUTHOR


def render():
    """Render halaman Beranda."""

    # ── Hero Section ──────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-tag">📊 Tugas Akhir · Forecasting · SARIMA</div>
            <div class="hero-title">Dashboard Forecasting<br/>Menggunakan SARIMA</div>
            <div class="hero-subtitle">
                Sistem analisis dan prediksi data runtun waktu menggunakan metode
                <strong>Seasonal AutoRegressive Integrated Moving Average (SARIMA)</strong>.
                Visualisasikan pola historis, bangun model, dan hasilkan forecast secara sistematis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Info Cards Utama ──────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("🎯", "Metode", "SARIMA", "Seasonal ARIMA"),
        ("📂", "Format Data", "CSV / Excel", "Upload fleksibel"),
        ("📏", "Evaluasi", "MAE · RMSE · MAPE", "Metrik standar"),
        ("📥", "Output", "Forecast + CSV", "Dapat diunduh"),
    ]
    for col, (icon, label, val, sub) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color:#2196F3;text-align:center;">
                    <div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div style="font-size:0.95rem;font-weight:700;color:#1E3A5F;">{val}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Alur Kerja Aplikasi ───────────────────────────────────
    st.markdown('<div class="section-title">📋 Alur Kerja Aplikasi</div>', unsafe_allow_html=True)

    steps = [
        ("📤", "Upload\nDataset", "Unggah file CSV/Excel"),
        ("✅", "Validasi\nData", "Periksa kualitas data"),
        ("🔧", "Preprocessing", "Bersihkan & konversi"),
        ("🔄", "Time\nSeries", "Bentuk indeks waktu"),
        ("📊", "Analisis", "Visualisasi historis"),
        ("🤖", "Model\nSARIMA", "Fitting parameter"),
        ("📏", "Evaluasi", "MAE, RMSE, MAPE"),
        ("🔮", "Forecast", "Prediksi & export"),
    ]
    cols = st.columns(len(steps))
    for col, (icon, label, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div style="text-align:center;padding:0.5rem 0.2rem;">
                    <div style="
                        width:52px;height:52px;border-radius:50%;
                        background:rgba(33,150,243,0.1);
                        border:2px solid #2196F3;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.3rem;margin:0 auto 0.5rem auto;
                    ">{icon}</div>
                    <div style="font-size:0.7rem;font-weight:700;color:#1E3A5F;white-space:pre-line;">{label}</div>
                    <div style="font-size:0.63rem;color:#718096;margin-top:0.2rem;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tentang Metode SARIMA ─────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title">🤖 Tentang Metode SARIMA</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sarima-card">
                <p style="color:#4a5568;line-height:1.7;margin:0;">
                    <strong>SARIMA</strong> (Seasonal AutoRegressive Integrated Moving Average) adalah
                    metode statistik untuk memodelkan data runtun waktu yang memiliki pola tren dan
                    musiman. Model ini merupakan pengembangan dari ARIMA dengan tambahan komponen seasonal.
                </p>
                <br/>
                <p style="font-weight:600;color:#1E3A5F;margin:0 0 0.5rem 0;">Parameter Model:</p>
                <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:0.5rem;">
                    <div><span class="badge badge-info">p</span> AutoRegressive (non-musiman)</div>
                    <div><span class="badge badge-warning">P</span> AutoRegressive (musiman)</div>
                    <div><span class="badge badge-info">d</span> Differencing (non-musiman)</div>
                    <div><span class="badge badge-warning">D</span> Differencing (musiman)</div>
                    <div><span class="badge badge-info">q</span> Moving Average (non-musiman)</div>
                    <div><span class="badge badge-warning">Q</span> Moving Average (musiman)</div>
                    <div><span class="badge badge-success">s</span> Periode musiman (misal: 12 untuk bulanan)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown('<div class="section-title">📂 Skenario Data</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sarima-card" style="background:linear-gradient(135deg,#fff9f0,#fff);">
                <div style="font-weight:700;color:#F39C12;margin-bottom:0.5rem;">⚠️ Data Tahunan (5 Tahun)</div>
                <div style="font-size:0.85rem;color:#4a5568;line-height:1.6;">
                    Data terbatas dengan sedikit observasi.
                    Cocok untuk demonstrasi sistem, namun belum optimal
                    untuk menangkap pola musiman SARIMA.
                </div>
            </div>
            <div class="sarima-card" style="background:linear-gradient(135deg,#f0fff4,#fff);margin-top:0.5rem;">
                <div style="font-weight:700;color:#27AE60;margin-bottom:0.5rem;">✅ Data Bulanan (Optimal)</div>
                <div style="font-size:0.85rem;color:#4a5568;line-height:1.6;">
                    Data simulasi dengan observasi lebih banyak (60–120+).
                    Lebih sesuai untuk pengujian model SARIMA dengan pola musiman.
                    <br/><span style="font-size:0.78rem;color:#718096;">(Data Simulasi Pembanding)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tombol Mulai ─────────────────────────────────────────
    col_btn, _, _ = st.columns([2, 2, 2])
    with col_btn:
        if st.button("📤  Mulai — Upload Dataset", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Upload Dataset"
            st.rerun()

    # ── Catatan Akademik ─────────────────────────────────────
    st.markdown(
        """
        <div class="alert alert-info" style="margin-top:2rem;font-size:0.85rem;">
            <span>🎓</span>
            <div>
                <strong>Catatan Akademik:</strong>
                Aplikasi ini dikembangkan untuk kebutuhan Tugas Akhir.
                Hasil forecast dihasilkan berdasarkan pola historis data yang tersedia.
                Interpretasi hasil harus dilakukan dengan mempertimbangkan keterbatasan data.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
