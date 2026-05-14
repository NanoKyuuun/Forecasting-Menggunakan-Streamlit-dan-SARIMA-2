# ============================================================
# validation_page.py — Halaman Validasi Data (Issue 2&3)
# ============================================================

import streamlit as st
from src.core.validation import validate_dataset
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import (
    show_success, show_error, show_warning, show_info,
    show_section_title, show_methodological_note,
)
from src.ui.tables import show_validation_table
from src.utils.constants import (
    SS_RAW_DATA, SS_COL_MAPPING, SS_VALIDATION_RESULT,
)
from src.utils.helpers import get_data_quality_label


def render():
    """
    M-render isi halaman 'Validasi Data'.
    Halaman ini bertindak sebagai "Satpam". Ia mengecek apakah data yang baru diunggah
    punya nilai kosong, nilai bukan angka, atau salah format sebelum diizinkan masuk
    ke tahap preprocessing (pembersihan data).
    """
    page_header(
        "Validasi Data",
        "Pemeriksaan kelayakan dataset sebelum proses pemodelan dimulai.",
        "✅",
    )

    # Menarik data mentah dan hasil mapping (pilihan kolom user) dari session state
    raw_data   = st.session_state.get(SS_RAW_DATA)
    col_mapping = st.session_state.get(SS_COL_MAPPING, {})

    # Cegah user lompat halaman
    if raw_data is None:
        show_warning("Dataset belum diunggah. Silakan kembali ke halaman <strong>Upload Dataset</strong>.")
        if st.button("← Kembali ke Upload", use_container_width=False):
            st.session_state["current_page"] = "Upload Dataset"
            st.rerun()
        return

    col_period   = col_mapping.get("periode")
    col_value    = col_mapping.get("nilai")
    col_category = col_mapping.get("kategori")

    # Pastikan user memilih kolom esensial (periode & nilai)
    if not col_period or not col_value:
        show_error("Pemetaan kolom tidak lengkap. Kembali ke Upload Dataset dan pastikan kolom Periode dan Nilai dipilih.")
        if st.button("← Kembali ke Upload"):
            st.session_state["current_page"] = "Upload Dataset"
            st.rerun()
        return

    # ── Jalankan Validasi ─────────────────────────────────────
    # Panggil fungsi core/validation.py
    with st.spinner("Menjalankan pemeriksaan data..."):
        result = validate_dataset(raw_data, col_period, col_value, col_category)
    st.session_state[SS_VALIDATION_RESULT] = result

    # ── Status Utama ──────────────────────────────────────────
    if result["is_valid"]:
        show_success(
            f"✅ Validasi berhasil! Dataset layak untuk dilanjutkan ke preprocessing."
            + (f" ({len(result['warnings'])} peringatan ditemukan)" if result["warnings"] else ""),
        )
    else:
        # Jika is_valid False, berarti kerusakannya terlalu parah (misal: kolom gak ada isinya sama sekali)
        show_error(
            f"❌ Validasi gagal. Ditemukan {len(result['errors'])} kesalahan yang perlu diperbaiki."
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Metric Cards Ringkasan ────────────────────────────────
    # Tampilkan label kualitas (Sangat Baik / Baik / Buruk)
    ql, ql_level = result["quality_label"], result["quality_level"]
    color_map = {"success": "#4CAF50", "info": "#2196F3", "warning": "#FF9800", "danger": "#E74C3C"}
    show_metrics_row([
        {"label": "Jumlah Observasi",  "value": str(result["n_obs"]),         "color": color_map.get(ql_level, "#2196F3")},
        {"label": "Kualitas Data",     "value": ql,                           "color": color_map.get(ql_level, "#2196F3")},
        {"label": "Kesalahan",         "value": str(len(result["errors"])),   "color": "#E74C3C" if result["errors"] else "#4CAF50"},
        {"label": "Peringatan",        "value": str(len(result["warnings"])), "color": "#FF9800" if result["warnings"] else "#4CAF50"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tabel Hasil Pemeriksaan ───────────────────────────────
    # Rincian tes yang dilakukan (seperti tes darah di lab)
    show_section_title("📋 Hasil Pemeriksaan Detail")
    show_validation_table(result["checks"])

    # ── Peringatan & Error ────────────────────────────────────
    # Cetak merah jika ada error (harus diperbaiki)
    if result["errors"]:
        show_section_title("❌ Daftar Kesalahan")
        for e in result["errors"]:
            show_error(e)

    # Cetak kuning jika ada warning (masih bisa dilanjut tapi hati-hati)
    if result["warnings"]:
        show_section_title("⚠️ Daftar Peringatan")
        for w in result["warnings"]:
            show_warning(w)

    # ── Catatan Metodologis ───────────────────────────────────
    # Peringatkan user kalau datanya terlalu sedikit (misal < 30)
    if result["quality_level"] in ("danger", "warning"):
        show_methodological_note(
            "Data historis yang tersedia masih terbatas. Model SARIMA tetap dapat digunakan "
            "sesuai fokus analisis, tetapi hasil prediksi perlu ditafsirkan sebagai estimasi awal. "
            "Gunakan data bulanan optimal sebagai pembanding untuk melihat perbedaan hasil."
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Upload Dataset", use_container_width=True):
            st.session_state["current_page"] = "Upload Dataset"
            st.rerun()
    with col2:
        # Jika validasi gagal, tombol akan berubah warna atau redaksi untuk mengingatkan user
        btn_label = "🔧  Lanjut ke Preprocessing" if result["is_valid"] else "⚠️  Lanjut Preprocessing (ada error)"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state["current_page"] = "Preprocessing"
            st.rerun()
