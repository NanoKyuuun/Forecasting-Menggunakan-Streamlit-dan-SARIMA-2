# ============================================================
# preprocessing.py — Pembersihan Data (PRD §10.4)
# ============================================================

import pandas as pd
import numpy as np


def preprocess(
    df: pd.DataFrame,
    col_period: str,
    col_value: str,
    col_category: str = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Membersihkan dan menstandarisasi format dataset sebelum diubah menjadi format time series.
    Langkah-langkah yang dilakukan: Filter kolom, standarisasi nama kolom, hapus nilai kosong (NaN),
    konversi tipe data (numerik & datetime), hapus duplikasi, dan urutkan berdasarkan waktu.

    Args:
        df: DataFrame mentah yang baru di-load.
        col_period: Nama kolom yang dipilih user sebagai representasi waktu/periode.
        col_value: Nama kolom yang dipilih user sebagai nilai target (value).
        col_category: (Opsional) Nama kolom yang dipilih user sebagai kategori/dimensi.

    Returns:
        tuple (clean_df, summary):
            - clean_df: DataFrame yang sudah bersih dan terstandarisasi.
            - summary: dict berisi statistik proses pembersihan (jumlah baris dihapus, dll) untuk UI.
    """
    # Dictionary untuk menyimpan rekam jejak (log) apa saja yang telah dilakukan pada data.
    # Berguna untuk memberikan feedback transparan kepada user di halaman UI.
    summary = {
        "before_rows":         len(df), # Jumlah baris awal
        "after_rows":          0,       # Akan diisi nanti setelah proses selesai
        "dropped_empty":       0,       # Jumlah baris yang dibuang karena kosong/NaN
        "dropped_duplicates":  0,       # Jumlah baris yang dibuang karena duplikat
        "converted_numeric":   0,       # Jumlah baris yang gagal diubah jadi angka
        "sorted":              True,    # Penanda bahwa data telah diurutkan
    }

    # Buat salinan data agar tidak mengubah DataFrame asli (best practice pandas)
    clean = df.copy()

    # 1. Pilih hanya kolom yang relevan (Membuang kolom-kolom lain yang tidak dibutuhkan)
    relevant_cols = [col_period, col_value]
    if col_category and col_category in df.columns:
        relevant_cols.append(col_category)
    # Filter dataset hanya menyisakan kolom yang ada di daftar relevant_cols
    clean = clean[[c for c in relevant_cols if c in clean.columns]]

    # 2. Standarisasi nama kolom (Rename)
    # Ini sangat penting agar proses modeling dan visualisasi ke depannya lebih mudah,
    # karena kita selalu bekerja dengan kolom bernama "periode", "nilai", dan "kategori".
    rename = {col_period: "periode", col_value: "nilai"}
    if col_category:
        rename[col_category] = "kategori"
    clean.rename(columns=rename, inplace=True)

    # 3. Drop (hapus) baris yang periode atau nilainya kosong (missing values)
    before = len(clean)
    clean.dropna(subset=["periode", "nilai"], inplace=True)
    summary["dropped_empty"] = before - len(clean)

    # 4. Konversi nilai ke tipe data numerik (angka)
    # errors="coerce" berarti jika ada teks yang tidak bisa jadi angka (misal: "N/A", "kosong"),
    # maka akan diubah menjadi NaN.
    clean["nilai"] = pd.to_numeric(clean["nilai"], errors="coerce")
    summary["converted_numeric"] = clean["nilai"].isna().sum() # Hitung berapa yang jadi NaN
    clean.dropna(subset=["nilai"], inplace=True)               # Buang nilai NaN tersebut

    # 5. Konversi periode ke tipe data Datetime (Waktu)
    # Gunakan astype(str) terlebih dahulu. Ini trik krusial:
    # Jika tahun berupa integer (misal: 2016), tanpa astype(str) pandas bisa membacanya 
    # sebagai "2016 nanosecond sejak 1 Jan 1970", bukan tahun 2016.
    clean["periode"] = pd.to_datetime(clean["periode"].astype(str), errors="coerce")
    clean.dropna(subset=["periode"], inplace=True) # Buang jika format tanggal tidak valid

    # 6. Hapus duplikasi baris
    # Jika ada data yang memiliki periode yang persis sama (dan kategori yang sama jika ada),
    # kita hanya pertahankan kemunculan pertama ("first") agar tidak merusak urutan time series.
    dup_cols = ["periode"] + (["kategori"] if "kategori" in clean.columns else [])
    before_dup = len(clean)
    clean.drop_duplicates(subset=dup_cols, keep="first", inplace=True)
    summary["dropped_duplicates"] = before_dup - len(clean)

    # 7. Urutkan data berdasarkan periode secara kronologis (dari terlama ke terbaru)
    # Algoritma time series seperti SARIMA wajib menerima data yang urut secara waktu.
    sort_cols = (["kategori", "periode"] if "kategori" in clean.columns else ["periode"])
    clean.sort_values(sort_cols, inplace=True)
    
    # Reset index dari 0, 1, 2... setelah diurutkan agar lebih rapi, dan buang index lama
    clean.reset_index(drop=True, inplace=True)

    # Catat jumlah baris final setelah semua proses pembersihan selesai
    summary["after_rows"] = len(clean)

    return clean, summary
