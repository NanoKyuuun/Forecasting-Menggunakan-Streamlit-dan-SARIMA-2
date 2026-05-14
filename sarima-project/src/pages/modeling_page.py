# ============================================================
# modeling_page.py — Pemodelan SARIMA (Issue 6)
# ============================================================

import streamlit as st
from src.core.sarima_model import fit_sarima, auto_search_sarima
from src.ui.cards import page_header, show_metrics_row, sarima_params_card
from src.ui.messages import (
    show_warning, show_success, show_error, show_section_title,
    show_methodological_note, show_info,
)
from src.ui.charts import chart_actual_vs_fitted
from src.utils.constants import (
    SS_TIME_SERIES, SS_DATA_FREQUENCY, SS_SARIMA_PARAMS,
    SS_MODEL_RESULT, SS_EVAL_METRICS, SS_FORECAST_RESULT,
)
from src.utils.helpers import get_seasonal_period


def render():
    """
    M-render isi halaman 'Pemodelan SARIMA'.
    Inti (Core) dari aplikasi. Tempat dimana pengguna menentukan parameter:
    p, d, q (Non-musiman) dan P, D, Q (Musiman), atau menyerahkan pencarian parameter
    kepada fungsi Grid Search otomatis (Auto-search).
    """
    page_header(
        "Pemodelan SARIMA",
        "Fitting model SARIMA dengan parameter manual atau auto-search terbatas.",
        "🤖",
    )

    # Tarik data time series dan tipe frekuensinya (Tahunan/Bulanan)
    ts        = st.session_state.get(SS_TIME_SERIES)
    frequency = st.session_state.get(SS_DATA_FREQUENCY, "Tahunan")

    if ts is None or len(ts) == 0:
        show_warning("Time series belum tersedia. Kembali ke Transformasi.")
        if st.button("← Transformasi"):
            st.session_state["current_page"] = "Transformasi Time Series"
            st.rerun()
        return

    # Ambil periode musiman dasar (misal s=12 jika bulanan)
    s_default = get_seasonal_period(frequency)

    # ── Mode Parameter ────────────────────────────────────────
    # Pengguna bisa memilih antara mode Manual atau Otomatis
    show_section_title("⚙️ Mode Parameter SARIMA")
    mode = st.radio(
        "Pilih mode parameter:",
        options=["Manual", "Auto-search Terbatas (AIC terkecil)"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if mode == "Manual":
        # ── Input Manual ──────────────────────────────────────
        show_info("Masukkan parameter SARIMA secara manual. Untuk data tahunan dengan observasi sedikit, mulai dengan parameter sederhana (1,1,0)(0,0,0)[1].")
        st.markdown("<br/>", unsafe_allow_html=True)

        # Buat UI berupa 4 kolom agar kotak-kotak input terlihat rapi berdampingan
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Non-Musiman**")
            p = st.number_input("p (AutoRegressive)", 0, 5, 1, key="p")
            d = st.number_input("d (Differencing)",   0, 2, 1, key="d")
            q = st.number_input("q (Moving Average)", 0, 5, 0, key="q")

        with col2:
            st.markdown("**Musiman**")
            P = st.number_input("P (SAR)", 0, 2, 0, key="P")
            D = st.number_input("D (SDiff)", 0, 1, 0, key="D")
            Q = st.number_input("Q (SMA)", 0, 2, 0, key="Q")

        with col3:
            st.markdown("**Periode Musiman**")
            s = st.number_input("s", 1, 24, s_default, key="s",
                                help="12 untuk data bulanan, 4 untuk kuartalan, 1 untuk tahunan")

        with col4:
            st.markdown("**&nbsp;**", unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
            # Preview visual parameter yang sedang dipilih di kotak kecil
            sarima_params_card({"p": p, "d": d, "q": q, "P": P, "D": D, "Q": Q, "s": s})

        run_btn = st.button("🚀 Jalankan Model SARIMA", type="primary", use_container_width=False)

        # Proses fitting hanya dijalankan ketika tombol diklik
        if run_btn:
            with st.spinner("Menjalankan fitting model..."):
                result = fit_sarima(ts, (p, d, q), (P, D, Q, s))
            # Panggil fungsi khusus internal di bawah file ini untuk menampilkan hasilnya
            _display_result(result, ts, frequency)

    else:
        # ── Auto-search ───────────────────────────────────────
        show_info(
            f"Auto-search akan mencoba kombinasi parameter dalam range terbatas "
            f"(p,d,q: 0–2, P,D,Q: 0–1) dan memilih model dengan AIC terkecil. "
            f"Periode musiman s={s_default} (deteksi otomatis dari {frequency})."
        )
        st.markdown("<br/>", unsafe_allow_html=True)

        # Total loop simulasi yang akan dicoba (3x2x3 x 2x2x2) = 144 kombinasi maksimal
        total_combinations = 3 * 2 * 3 * 2 * 2 * 2  
        st.markdown(
            f'<div class="alert alert-warning"><span>⏱️</span>'
            f'<span>Akan mencoba <strong>{total_combinations}</strong> kombinasi parameter. Proses mungkin memakan beberapa menit.</span></div>',
            unsafe_allow_html=True,
        )

        run_auto = st.button("🔍 Mulai Auto-search", type="primary")

        if run_auto:
            # Sediakan UI indikator proses (Loading Bar) yang bergerak maju
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(current, total):
                progress_bar.progress(current / total)
                status_text.text(f"Menguji kombinasi {current}/{total}...")

            with st.spinner("Mencari parameter terbaik..."):
                # Kirim callback update_progress agar bar bisa bergerak
                result = auto_search_sarima(ts, s_default, progress_callback=update_progress)

            progress_bar.progress(1.0)
            status_text.text("Auto-search selesai!")
            _display_result(result, ts, frequency)

    # ── Navigasi Permanen (selalu tampil, baca dari session state) ────
    # Jika model sudah sukses dikalkulasi sebelumnya, buka akses ke halaman evaluasi
    st.markdown("<br/>", unsafe_allow_html=True)
    model_ready = st.session_state.get(SS_MODEL_RESULT) is not None
    col_nav1, col_nav2, _ = st.columns([2, 2, 2])
    with col_nav1:
        if st.button("← Analisis", use_container_width=True, key="btn_back_analisis"):
            st.session_state["current_page"] = "Analisis Time Series"
            st.rerun()
    with col_nav2:
        if st.button(
            "📏  Lanjut ke Evaluasi Model",
            type="primary",
            use_container_width=True,
            key="btn_next_evaluasi",
            disabled=not model_ready, # Tombol abu-abu tidak bisa diklik jika belum ada model
        ):
            st.session_state["current_page"] = "Evaluasi Model"
            st.rerun()
            
    if not model_ready:
        st.caption("⬆️ Jalankan model terlebih dahulu untuk melanjutkan.")



def _display_result(result: dict, ts, frequency: str):
    """
    Fungsi internal/helper untuk mencetak hasil fitting SARIMA ke layar.
    Fungsi ini dipisahkan agar bisa dipakai dua kali (oleh mode Manual dan Auto-Search)
    tanpa harus mengulang/menulis ulang (duplikasi) blok kode UI yang sama.
    """
    # 1. Cek apakah ada pesan kegagalan matematis
    if not result["success"]:
        show_error(
            f"Model SARIMA gagal dijalankan. Error: {result['error']}<br/>"
            f"Saran: coba parameter yang lebih sederhana, misalnya (1,1,0)(0,0,0)[1] untuk data tahunan."
        )
        return

    # 2. Amankan hasil yang sukses ke Memori Session
    st.session_state[SS_SARIMA_PARAMS]    = result["params"]
    st.session_state[SS_MODEL_RESULT]     = result
    # Jika model berubah, maka hasil evaluasi dan ramalan di memori dibersihkan (reset)
    st.session_state[SS_EVAL_METRICS]     = None  
    st.session_state[SS_FORECAST_RESULT]  = None

    params = result["params"]
    show_success(
        f"Model SARIMA({params['p']},{params['d']},{params['q']})"
        f"({params['P']},{params['D']},{params['Q']})[{params['s']}] "
        f"berhasil dijalankan!"
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Card Parameter & AIC/BIC ──────────────────────────────
    col_a, col_b = st.columns([2, 1])
    with col_a:
        sarima_params_card(params)
    with col_b:
        show_metrics_row([
            {"label": "AIC", "value": f"{result['aic']:.2f}" if result.get('aic') else "—", "color": "#9C27B0"},
        ])
        show_metrics_row([
            {"label": "BIC", "value": f"{result['bic']:.2f}" if result.get('bic') else "—", "color": "#FF9800"},
        ])

    # ── Grafik Actual vs Fitted ───────────────────────────────
    # Memeriksa sekilas bentuk kurva hasil model dibandingkan aslinya
    if len(result["fitted"]) > 0:
        show_section_title("📊 Aktual vs Nilai Tebakan Model")
        fig = chart_actual_vs_fitted(ts, result["fitted"], title="Aktual vs Nilai Fitted")
        st.plotly_chart(fig, use_container_width=True)

    # ── Catatan Metodologis ───────────────────────────────────
    if len(ts) < 30:
        show_methodological_note(
            "Data historis yang digunakan masih terbatas. "
            "Model SARIMA tetap digunakan sesuai fokus analisis, "
            "namun hasil prediksi harus dipahami sebagai estimasi awal berbasis data terbatas."
        )

