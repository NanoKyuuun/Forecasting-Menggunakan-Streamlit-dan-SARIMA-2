# ============================================================
# upload_page.py — Halaman Upload Dataset (Issue 2&3)
# ============================================================

import streamlit as st
import pandas as pd
from src.core.data_loader import load_file, get_file_info
from src.ui.cards import page_header, show_metrics_row, info_card
from src.ui.messages import show_success, show_error, show_warning, show_info, show_section_title
from src.ui.tables import show_dataframe
from src.utils.constants import (
    SS_RAW_DATA, SS_COL_MAPPING, SS_FILE_NAME,
    SS_VALIDATION_RESULT, SS_CLEAN_DATA, SS_TIME_SERIES,
)


def render():
    page_header(
        "Upload Dataset",
        "Unggah file CSV atau Excel yang berisi data historis untuk dianalisis.",
        "📤",
    )

    # ── Reset ketika upload baru ──────────────────────────────
    st.markdown('<div class="section-title">📁 Pilih File Dataset</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Pilih file CSV atau Excel",
        type=["csv", "xlsx", "xls"],
        help="Maksimal 50MB. Format: CSV (UTF-8) atau Excel (.xlsx)",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        df, err = load_file(uploaded_file)

        if err:
            show_error(f"Gagal membaca file: {err}")
            return

        # Simpan ke session state
        st.session_state[SS_RAW_DATA]         = df
        st.session_state[SS_FILE_NAME]        = uploaded_file.name
        st.session_state[SS_VALIDATION_RESULT] = None  # Reset validasi
        st.session_state[SS_CLEAN_DATA]        = None
        st.session_state[SS_TIME_SERIES]       = None

        info = get_file_info(df, uploaded_file.name)
        show_success(f"File <strong>{uploaded_file.name}</strong> berhasil dibaca!")

        # ── Ringkasan File ────────────────────────────────────
        show_section_title("📊 Ringkasan File")
        show_metrics_row([
            {"label": "Jumlah Baris",  "value": f"{info['jumlah_baris']:,}",  "color": "#2196F3"},
            {"label": "Jumlah Kolom",  "value": str(info['jumlah_kolom']),    "color": "#4CAF50"},
            {"label": "Nama File",     "value": info['nama_file'],            "color": "#9C27B0"},
            {"label": "Ukuran",        "value": info['ukuran_memori'],        "color": "#FF9800"},
        ])

        # ── Kolom yang Ditemukan ──────────────────────────────
        show_section_title("🏷️ Kolom yang Ditemukan")
        cols_html = "".join(
            f'<span class="badge badge-info" style="margin:3px;">{c}</span>'
            for c in info["kolom"]
        )
        st.markdown(
            f'<div class="sarima-card" style="padding:1rem;">{cols_html}</div>',
            unsafe_allow_html=True,
        )

        # ── Mapping Kolom ─────────────────────────────────────
        show_section_title("🗺️ Pemetaan Kolom")
        show_info("Pilih kolom yang sesuai dari dataset kamu untuk kolom-kolom wajib berikut.")

        all_cols  = list(df.columns)
        none_opt  = ["— (tidak ada)"]

        # Coba tebak kolom berdasarkan nama
        def guess_col(keywords: list[str]) -> str:
            for kw in keywords:
                for c in all_cols:
                    if kw.lower() in c.lower():
                        return c
            return all_cols[0] if all_cols else none_opt[0]

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            # Prioritaskan kolom bertipe datetime/tanggal dulu, baru fallback ke integer tahun
            def guess_period_col(cols: list[str]) -> str:
                # Cek tipe data dulu — preferensikan kolom yang sudah datetime atau string tanggal
                date_keywords = ["tanggal", "date", "periode", "bulan", "month"]
                year_keywords = ["tahun", "year"]
                for kw in date_keywords:
                    for c in cols:
                        if kw.lower() in c.lower():
                            return c
                # Coba cek apakah isinya bisa jadi tanggal nyata
                for kw in year_keywords:
                    for c in cols:
                        if kw.lower() in c.lower():
                            try:
                                sample = df[c].dropna().head(3)
                                parsed = pd.to_datetime(sample, errors='coerce')
                                # Jika parsed jadi 1970 → ini integer, skip
                                if not all(parsed.dt.year < 1980):
                                    return c
                            except Exception:
                                pass
                return cols[0] if cols else none_opt[0]
            default_period = guess_period_col(all_cols)
            sel_period = st.selectbox(
                "📅 Kolom Periode *",
                options=all_cols,
                index=all_cols.index(default_period) if default_period in all_cols else 0,
                help="Kolom yang berisi informasi waktu (tahun/bulan/tanggal)",
            )

        with col_b:
            default_value = guess_col(["jumlah", "nilai", "value", "pendaftar", "count", "total"])
            sel_value = st.selectbox(
                "📈 Kolom Nilai *",
                options=all_cols,
                index=all_cols.index(default_value) if default_value in all_cols else 0,
                help="Kolom angka yang akan diprediksi",
            )

        with col_c:
            default_cat = guess_col(["prodi", "program_studi", "kategori", "kategory", "program", "group", "kelompok", "nama"])
            sel_category = st.selectbox(
                "🏷️ Kolom Kategori (opsional)",
                options=none_opt + all_cols,
                index=(none_opt + all_cols).index(default_cat) if default_cat in none_opt + all_cols else 0,
                help="Kolom pengelompokan data (mis: nama program studi). Pilih '— (tidak ada)' jika tidak ada.",
            )

        col_mapping = {
            "periode":   sel_period,
            "nilai":     sel_value,
            "kategori":  sel_category if sel_category != none_opt[0] else None,
        }
        st.session_state[SS_COL_MAPPING] = col_mapping

        # ── Preview Data ──────────────────────────────────────
        show_section_title("👁️ Preview Data (10 Baris Pertama)")
        show_dataframe(df, max_rows=10)

        st.markdown("<br/>", unsafe_allow_html=True)

        # ── Navigasi Lanjut ───────────────────────────────────
        col_btn, _, _ = st.columns([2, 2, 2])
        with col_btn:
            if st.button("✅  Lanjut ke Validasi Data", type="primary", use_container_width=True):
                st.session_state["current_page"] = "Validasi Data"
                st.rerun()

    else:
        # Belum ada file — tampilkan panduan
        st.markdown(
            """
            <div class="sarima-card" style="text-align:center;padding:3rem 2rem;border:2px dashed rgba(33,150,243,0.3);">
                <div style="font-size:3rem;margin-bottom:1rem;">📁</div>
                <div style="font-size:1.1rem;font-weight:700;color:#1E3A5F;margin-bottom:0.5rem;">
                    Belum ada file yang diunggah
                </div>
                <div style="color:#718096;font-size:0.9rem;max-width:400px;margin:0 auto;line-height:1.6;">
                    Klik tombol di atas untuk memilih file CSV atau Excel dari perangkat kamu.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        show_section_title("📋 Format Dataset yang Dibutuhkan")
        st.markdown(
            """
            <div class="sarima-card">
                <p style="color:#4a5568;margin:0 0 1rem 0;">Dataset minimal harus memiliki kolom-kolom berikut:</p>
                <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
                    <thead>
                        <tr style="background:#1E3A5F;color:white;">
                            <th style="padding:0.6rem 1rem;text-align:left;">Kolom</th>
                            <th style="padding:0.6rem 1rem;text-align:left;">Deskripsi</th>
                            <th style="padding:0.6rem 1rem;text-align:left;">Contoh</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
                            <td style="padding:0.55rem 1rem;font-weight:600;">periode</td>
                            <td style="padding:0.55rem 1rem;">Tahun atau bulan data</td>
                            <td style="padding:0.55rem 1rem;font-family:monospace;">2021 atau 2021-01</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
                            <td style="padding:0.55rem 1rem;font-weight:600;">nilai</td>
                            <td style="padding:0.55rem 1rem;">Angka yang akan diprediksi</td>
                            <td style="padding:0.55rem 1rem;font-family:monospace;">120</td>
                        </tr>
                        <tr>
                            <td style="padding:0.55rem 1rem;font-weight:600;">kategori</td>
                            <td style="padding:0.55rem 1rem;">Nama program studi / kelompok (opsional)</td>
                            <td style="padding:0.55rem 1rem;font-family:monospace;">Teknik Informatika</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Data contoh yang tersedia
        show_section_title("💡 Data Contoh Tersedia")
        show_info("Kamu dapat menggunakan data contoh yang tersedia di folder <code>data/raw/</code> untuk pengujian.")
