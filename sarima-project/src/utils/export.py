# ============================================================
# export.py — Fungsi Export Hasil Forecast ke CSV
# ============================================================

import pandas as pd
import io
from datetime import datetime
from src.utils.helpers import date_export_str


def build_forecast_csv(
    forecast_df: pd.DataFrame,
    sarima_params: dict,
    category: str,
) -> bytes:
    """
    Fungsi untuk mengonversi DataFrame hasil forecasting menjadi format file CSV 
    dalam bentuk 'bytes' agar bisa langsung di-download pengguna dari browser tanpa
    perlu menyimpannya ke hard disk server terlebih dahulu.

    Args:
        forecast_df: DataFrame berisi tanggal/periode, prediksi rata-rata, batas bawah, dan batas atas.
        sarima_params: Dictionary konfigurasi parameter SARIMA (p, d, q, dll) 
                       untuk disisipkan sebagai informasi pelacak di file CSV.
        category: Nama program studi / kategori yang sedang diprediksi.

    Returns:
        bytes: Raw data CSV dalam encoding utf-8-sig (mendukung karakter khusus di MS Excel).
    """
    export_df = forecast_df.copy()

    # Menyisipkan kolom metadata di paling awal (index 0) agar pengguna 
    # tahu CSV ini adalah hasil prediksi kategori/prodi apa
    export_df.insert(0, "kategori", category)
    
    # Merangkai informasi parameter SARIMA menjadi format string standar
    export_df["parameter_SARIMA"] = (
        f"SARIMA({sarima_params.get('p', 0)},{sarima_params.get('d', 0)},{sarima_params.get('q', 0)})"
        f"({sarima_params.get('P', 0)},{sarima_params.get('D', 0)},{sarima_params.get('Q', 0)})"
        f"[{sarima_params.get('s', 1)}]"
    )
    # Menyimpan jam/tanggal saat tombol download ditekan
    export_df["tanggal_export"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pastikan nama kolom hasil prediksi (yang mungkin menggunakan bahasa Inggris default statsmodels)
    # diterjemahkan ke bahasa Indonesia agar selaras dengan UI aplikasi.
    rename_map = {}
    for col in export_df.columns:
        lower = col.lower()
        if "period" in lower or "tanggal" in lower or "bulan" in lower or "tahun" in lower:
            # Kecuali kolom tanggal_export yang baru kita buat
            if col not in ("tanggal_export",):
                rename_map[col] = "periode_forecast"
        elif "pred" in lower or "forecast" in lower or "nilai" in lower:
            rename_map[col] = "nilai_prediksi"
        elif "lower" in lower or "bawah" in lower:
            rename_map[col] = "batas_bawah"
        elif "upper" in lower or "atas" in lower:
            rename_map[col] = "batas_atas"
    
    # Terapkan perubahan nama kolom
    export_df.rename(columns=rename_map, inplace=True)

    # Gunakan io.StringIO sebagai memori virtual untuk menampung teks CSV 
    # tanpa perlu menyentuh sistem file I/O (disk).
    buffer = io.StringIO()
    export_df.to_csv(buffer, index=False, encoding="utf-8-sig")
    
    # Return string tersebut dalam format raw bytes
    return buffer.getvalue().encode("utf-8-sig")


def get_download_filename(category: str) -> str:
    """
    Membuat nama file otomatis untuk file CSV yang akan diunduh.
    Menggabungkan teks 'forecast', nama kategori, dan jam spesifik (format rapat).
    Spasi dan garis miring dibersihkan agar kompatibel di semua OS.

    Args:
        category: Nama kategori / prodi.

    Returns:
        str: Nama file yang aman, contoh: 'forecast_TI_20260513_120000.csv'
    """
    # Ganti spasi dengan underscore dan hapus karakter terlarang Windows (/)
    safe_cat = category.replace(" ", "_").replace("/", "-")
    return f"forecast_{safe_cat}_{date_export_str()}.csv"
