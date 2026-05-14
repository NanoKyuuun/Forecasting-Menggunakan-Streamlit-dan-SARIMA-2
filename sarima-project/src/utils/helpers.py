# ============================================================
# helpers.py — Fungsi Pembantu Umum
# ============================================================

import pandas as pd
import numpy as np
from datetime import datetime


def format_number(value: float, decimals: int = 2) -> str:
    """
    Mengonversi angka mentah menjadi string (teks) yang lebih mudah dibaca 
    dengan menambahkan pemisah ribuan (koma) dan membatasi jumlah angka desimal.

    Args:
        value: Angka yang akan diformat (bisa integer atau float).
        decimals: Jumlah angka di belakang koma (default 2).
                  Jika 0, angka akan dibulatkan menjadi bilangan bulat.

    Returns:
        str: Angka yang sudah diformat (misal: 1,500.50). 
             Jika nilai kosong (None/NaN), mengembalikan garis putus-putus '—'.
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    try:
        if decimals == 0:
            return f"{int(value):,}"
        return f"{value:,.{decimals}f}"
    except Exception:
        # Jika gagal (misal value berupa string yang tidak bisa diubah ke angka),
        # kembalikan nilai aslinya dalam bentuk string
        return str(value)


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Mengonversi angka mentah menjadi format persentase.

    Args:
        value: Angka desimal (contoh: 15.456).
        decimals: Jumlah angka di belakang koma (default 2).

    Returns:
        str: String persentase (misal: '15.46%').
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    return f"{value:.{decimals}f}%"


def get_data_quality_label(n_obs: int) -> tuple[str, str]:
    """
    Mengevaluasi kualitas (kelayakan) dataset berdasarkan jumlah observasinya.
    Digunakan secara luas di UI untuk memberi warna badge peringatan.

    Args:
        n_obs: Jumlah baris data time series.

    Returns:
        tuple[str, str]: (Teks Label Status, Kode Warna Bootstrap)
                         Contoh: ("Cukup", "info")
    """
    if n_obs < 10:
        return "Sangat Terbatas", "danger"   # Merah (Sangat tidak layak untuk SARIMA)
    elif n_obs < 31:
        return "Terbatas", "warning"         # Kuning (Bisa jalan, tapi akurasi diragukan)
    elif n_obs < 61:
        return "Cukup", "info"               # Biru (Memenuhi standar minimum 3-5 tahun bulanan)
    else:
        return "Baik", "success"             # Hijau (Sangat ideal, > 5 tahun data bulanan)


def get_mape_interpretation(mape: float) -> str:
    """
    Memberikan penjelasan kualitatif untuk metrik evaluasi error MAPE
    (Mean Absolute Percentage Error) berdasarkan standar akademis Lewis (1982).

    Args:
        mape: Nilai error dalam persen.

    Returns:
        str: Teks interpretasi.
    """
    if mape < 10:
        return "Sangat Akurat (MAPE < 10%)"
    elif mape < 20:
        return "Baik (MAPE 10%–20%)"
    elif mape < 50:
        return "Cukup (MAPE 20%–50%)"
    else:
        return "Kurang Akurat (MAPE > 50%)"


def detect_frequency(series: pd.Series) -> str:
    """
    Mendeteksi pola frekuensi data runtun waktu secara otomatis berdasarkan jarak
    rata-rata (median) antar indeks tanggal.

    Args:
        series: Pandas Series dengan DatetimeIndex.

    Returns:
        str: "Bulanan", "Kuartalan", "Tahunan", atau "unknown".
    """
    if len(series) < 2:
        return "unknown"
    try:
        # Hitung selisih jarak hari antara baris ke-n dan ke-(n-1)
        diff = pd.Series(series.index).diff().dropna()
        median_days = diff.dt.days.median()
        
        if median_days <= 32:
            return "Bulanan"      # Jarak antar data ~30 hari
        elif median_days <= 100:
            return "Kuartalan"    # Jarak antar data ~90 hari
        else:
            return "Tahunan"      # Jarak antar data ~365 hari
    except Exception:
        return "unknown"


def get_seasonal_period(frequency: str) -> int:
    """
    Mendapatkan panjang siklus musiman (s) yang cocok untuk model SARIMA 
    berdasarkan frekuensi data.

    Args:
        frequency: "Bulanan", "Kuartalan", atau "Tahunan".

    Returns:
        int: Siklus musiman. 12 (untuk bulan), 4 (untuk kuartal), 1 (tidak ada musiman/tahunan).
    """
    mapping = {
        "Bulanan": 12,
        "Kuartalan": 4,
        "Tahunan": 1,
    }
    return mapping.get(frequency, 1)


def now_str() -> str:
    """
    Menghasilkan waktu saat ini dalam format string standar (YYYY-MM-DD HH:MM:SS).
    Digunakan untuk mencetak waktu proses ke log/UI.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_export_str() -> str:
    """
    Menghasilkan format tanggal yang sangat rapat (tanpa spasi/titik dua) 
    (YYYYMMDD_HHMMSS) untuk digunakan sebagai penamaan file CSV hasil download.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")
