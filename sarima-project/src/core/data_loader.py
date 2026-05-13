# ============================================================
# data_loader.py — Modul Baca File CSV / Excel
# ============================================================

import pandas as pd
import streamlit as st
from io import BytesIO


def load_file(uploaded_file) -> tuple[pd.DataFrame | None, str]:
    """
    Membaca file yang diunggah pengguna.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        (DataFrame, pesan_error) — jika berhasil, pesan_error kosong
    """
    if uploaded_file is None:
        return None, "Tidak ada file yang diunggah."

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".csv"):
            # Coba beberapa encoding
            for enc in ("utf-8", "utf-8-sig", "latin-1", "iso-8859-1"):
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc)
                    if len(df) > 0:
                        return df, ""
                except UnicodeDecodeError:
                    continue
            return None, "Encoding file CSV tidak dapat dideteksi. Coba simpan ulang sebagai UTF-8."

        elif filename.endswith((".xlsx", ".xls")):
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            return df, ""

        else:
            return None, f"Format file '{uploaded_file.name}' tidak didukung. Gunakan file CSV atau Excel (.xlsx)."

    except Exception as e:
        return None, f"Gagal membaca file: {str(e)}"


def get_file_info(df: pd.DataFrame, filename: str) -> dict:
    """Mengumpulkan informasi dasar tentang file yang dibaca."""
    return {
        "nama_file":   filename,
        "jumlah_baris": len(df),
        "jumlah_kolom": len(df.columns),
        "kolom":        list(df.columns),
        "ukuran_memori": f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
    }
