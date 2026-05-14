# ============================================================
# transformation.py — Transformasi ke Time Series (PRD §10.5)
# ============================================================

import pandas as pd
from src.utils.helpers import detect_frequency, get_seasonal_period


def build_time_series(
    clean_df: pd.DataFrame,
    category: str = None,
) -> tuple[pd.Series, str, int]:
    """
    Mengubah DataFrame tabular biasa (hasil preprocessing) menjadi format objek Time Series (pd.Series) 
    yang diindeks berdasarkan waktu. Ini adalah syarat wajib sebelum algoritma SARIMA bisa bekerja.

    Args:
        clean_df: DataFrame hasil preprocessing yang kolom-kolomnya sudah terstandarisasi.
        category: (Opsional) Nama kategori spesifik yang ingin dianalisis, jika user tidak memilih "Semua Kategori".

    Returns:
        tuple: (time_series_data, frequency_string, seasonal_period_integer)
            - ts_df: Objek pd.Series dengan nilai sebagai data dan periode waktu sebagai indeks.
            - frequency: Teks frekuensi yang dideteksi (misal: "Bulanan", "Tahunan").
            - seasonal_period: Angka yang merepresentasikan siklus musim (misal 12 untuk bulanan).
    """
    df = clean_df.copy()

    # Jika dataset memiliki kolom kategori dan user memilih kategori spesifik (bukan "Semua")
    if "kategori" in df.columns and category and category != "Semua Kategori (Keseluruhan)":
        # Saring data, hanya ambil baris yang sesuai dengan kategori pilihan user
        df = df[df["kategori"] == category]

    # Mengelompokkan data berdasarkan periode waktu (groupby) dan menjumlahkan nilainya.
    # Jika dalam 1 bulan ada beberapa record transaksi, maka akan di-SUM menjadi total bulanan.
    # sort_index() memastikan urutannya kronologis.
    ts_df = df.groupby("periode")["nilai"].sum().sort_index()

    # Panggil fungsi helper untuk menebak frekuensi data secara otomatis (harian/bulanan/tahunan)
    frequency = detect_frequency(ts_df)
    # Tentukan panjang satu siklus berdasarkan frekuensinya (misal bulanan -> siklusnya 12 bulan)
    seasonal_period = get_seasonal_period(frequency)

    # Menstandarisasi indeks Pandas agar dikenali oleh statsmodels sebagai indeks waktu penuh.
    # Statsmodels memerlukan frekuensi (freq) yang eksplisit untuk beberapa operasi.
    freq_alias_map = {
        "Bulanan":    "MS",   # Month Start (Awal bulan)
        "Kuartalan":  "QS",   # Quarter Start (Awal kuartal)
        "Tahunan":    "YS",   # Year Start (Awal tahun)
    }
    
    freq_alias = freq_alias_map.get(frequency, None)
    if freq_alias:
        try:
            # Pastikan indeks benar-benar berformat DatetimeIndex
            ts_df.index = pd.DatetimeIndex(ts_df.index, freq=None)
            # asfreq akan melengkapi tanggal yang mungkin bolong/hilang sesuai frekuensi.
            # method="pad" (forward fill) akan mengisi tanggal yang kosong dengan nilai dari tanggal sebelumnya.
            ts_df = ts_df.asfreq(freq_alias, method="pad")
        except Exception:
            # Jika gagal mengatur frekuensi (biasanya karena jarak antar tanggal sangat tidak beraturan),
            # biarkan indeks seperti apa adanya tanpa frekuensi kaku (statsmodels masih bisa bekerja walau dengan peringatan).
            pass

    return ts_df, frequency, seasonal_period


def get_available_categories(clean_df: pd.DataFrame) -> list[str]:
    """
    Mengambil semua nilai kategori yang unik dari dataframe untuk ditampilkan di dropdown UI.
    
    Args:
        clean_df: DataFrame bersih.
        
    Returns:
        list[str]: Daftar nama kategori, selalu diawali dengan opsi "Semua Kategori (Keseluruhan)".
    """
    if "kategori" in clean_df.columns:
        # Ambil nilai unik, buang NaN, jadikan list, lalu urutkan sesuai abjad
        cats = sorted(clean_df["kategori"].dropna().unique().tolist())
        return ["Semua Kategori (Keseluruhan)"] + cats
    # Jika tidak ada kolom kategori, kembalikan list kosong
    return []


def get_descriptive_stats(ts: pd.Series) -> dict:
    """
    Menghitung metrik-metrik ringkasan statistik deskriptif dari data time series.
    Metrik ini digunakan untuk ditampilkan pada "Kartu Informasi" di halaman transformasi.
    
    Args:
        ts: Objek pd.Series time series.
        
    Returns:
        dict: Kamus berisi rata-rata, min, max, standar deviasi, dan rentang waktu.
    """
    # Menghitung selisih (diferensiasi ordo 1) antar waktu berturut-turut untuk mencari lonjakan tertinggi
    changes = ts.diff().dropna()
    
    return {
        "n_obs":      len(ts),            # Jumlah total observasi data
        "min":        float(ts.min()),    # Nilai terkecil sepanjang sejarah
        "max":        float(ts.max()),    # Nilai terbesar sepanjang sejarah
        "mean":       float(ts.mean()),   # Rata-rata nilai keseluruhan
        "std":        float(ts.std()),    # Standar deviasi (simpangan baku / volatilitas)
        # Ambil tanggal mulai dan selesai (format string agar mudah di-render di UI)
        "start":      str(ts.index[0].date()) if hasattr(ts.index[0], "date") else str(ts.index[0]),
        "end":        str(ts.index[-1].date()) if hasattr(ts.index[-1], "date") else str(ts.index[-1]),
        # Loncatan naik tertinggi dan penurunan terdalam antar 2 periode berturutan
        "max_change": float(changes.max()) if len(changes) > 0 else 0.0,
        "min_change": float(changes.min()) if len(changes) > 0 else 0.0,
    }
