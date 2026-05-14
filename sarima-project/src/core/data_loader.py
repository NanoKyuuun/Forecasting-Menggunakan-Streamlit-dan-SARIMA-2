# ============================================================
# data_loader.py — Modul Baca File CSV / Excel
# ============================================================

import pandas as pd
import streamlit as st
from io import BytesIO


def load_file(uploaded_file) -> tuple[pd.DataFrame | None, str]:
    """
    Membaca file yang diunggah pengguna dan mengubahnya menjadi pandas DataFrame.
    Fungsi ini menangani file CSV maupun Excel dengan mencoba beberapa encoding
    agar tidak error saat file mengandung karakter khusus.

    Args:
        uploaded_file: Objek file hasil unggahan dari widget st.file_uploader

    Returns:
        tuple (DataFrame, pesan_error): Jika berhasil, DataFrame terisi dan pesan_error kosong.
        Jika gagal, DataFrame None dan pesan_error berisi penjelasan error.
    """
    # Validasi awal: pastikan file benar-benar ada
    if uploaded_file is None:
        return None, "Tidak ada file yang diunggah."

    # Ambil nama file dan ubah ke huruf kecil untuk memudahkan pengecekan ekstensi
    filename = uploaded_file.name.lower()

    try:
        # Penanganan khusus untuk file CSV
        if filename.endswith(".csv"):
            # Coba beberapa jenis encoding teks yang umum digunakan (terutama di Windows)
            for enc in ("utf-8", "utf-8-sig", "latin-1", "iso-8859-1"):
                try:
                    # Kembalikan pointer file ke awal (byte 0) sebelum membaca ulang
                    # Ini penting karena iterasi sebelumnya mungkin sudah membaca sebagian isi file
                    uploaded_file.seek(0)
                    # Baca CSV menggunakan pandas
                    df = pd.read_csv(uploaded_file, encoding=enc)
                    
                    # Jika berhasil dibaca dan datanya ada (tidak kosong)
                    if len(df) > 0:
                        return df, ""
                except UnicodeDecodeError:
                    # Jika gagal decode dengan encoding ini, lanjut coba encoding berikutnya di loop
                    continue
            
            # Jika semua encoding gagal, berikan pesan error yang informatif
            return None, "Encoding file CSV tidak dapat dideteksi. Coba simpan ulang sebagai UTF-8."

        # Penanganan untuk file Excel (mendukung ekstensi baru .xlsx dan lama .xls)
        elif filename.endswith((".xlsx", ".xls")):
            uploaded_file.seek(0)
            # Baca menggunakan engine openpyxl yang lebih aman untuk Excel modern
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            return df, ""

        # Jika ekstensi tidak dikenali (bukan CSV atau Excel)
        else:
            return None, f"Format file '{uploaded_file.name}' tidak didukung. Gunakan file CSV atau Excel (.xlsx)."

    except Exception as e:
        # Penanganan error global (misal: file corrupt, out of memory, dll)
        # Tangkap semua exception dan kembalikan pesan error yang aman
        return None, f"Gagal membaca file: {str(e)}"


def get_file_info(df: pd.DataFrame, filename: str) -> dict:
    """
    Mengumpulkan statistik dan informasi metadata dasar tentang dataset yang baru saja dibaca.
    Fungsi ini dipanggil untuk menampilkan ringkasan data di UI setelah upload berhasil.
    
    Args:
        df: DataFrame yang sudah dimuat
        filename: Nama asli dari file
        
    Returns:
        dict: Berisi metrik-metrik dasar mengenai dimensi dan memori data
    """
    return {
        "nama_file":    filename,                    # Nama file asli untuk referensi
        "jumlah_baris": len(df),                     # Jumlah record/observasi
        "jumlah_kolom": len(df.columns),             # Jumlah fitur/variabel
        "kolom":        list(df.columns),            # Daftar nama-nama kolom
        # Hitung total memori aktual yang dipakai oleh dataframe, 
        # konversi ke KB, dan format jadi string 1 desimal
        "ukuran_memori": f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
    }
