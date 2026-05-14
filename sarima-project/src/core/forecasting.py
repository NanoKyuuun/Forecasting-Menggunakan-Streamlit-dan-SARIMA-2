# ============================================================
# forecasting.py — Generate Forecast (PRD §10.9)
# ============================================================

import pandas as pd
import numpy as np


def generate_forecast(
    model_result: dict,
    n_periods: int,
) -> dict:
    """
    Menghasilkan (generate) nilai peramalan/prediksi ke masa depan (out-of-sample) 
    menggunakan model SARIMA yang telah dilatih sebelumnya.

    Args:
        model_result: Dictionary hasil keluaran dari fungsi fit_sarima() yang berisi objek model statsmodels.
        n_periods: Jumlah periode/langkah ke depan yang ingin diprediksi.

    Returns:
        dict: Struktur kamus (dictionary) yang berisi:
            - "forecast_df": pd.DataFrame berisi periode, prediksi titik tengah, batas bawah, dan batas atas.
            - "forecast_mean": pd.Series nilai prediksi titik tengah (rata-rata).
            - "forecast_lower": pd.Series nilai batas bawah dari interval kepercayaan.
            - "forecast_upper": pd.Series nilai batas atas dari interval kepercayaan.
            - "success": boolean penanda apakah proses peramalan berhasil.
            - "error": pesan error berupa teks jika terjadi kegagalan.
    """
    # Ekstrak objek model statsmodels (ARIMAResultsWrapper) dari hasil pemodelan sebelumnya
    fitted_model = model_result.get("model")
    
    # Validasi awal: Pastikan model benar-benar ada. Jika tidak, batalkan proses.
    if fitted_model is None:
        return {
            "forecast_df":    pd.DataFrame(),
            "forecast_mean":  pd.Series(dtype=float),
            "forecast_lower": pd.Series(dtype=float),
            "forecast_upper": pd.Series(dtype=float),
            "success":        False,
            "error":          "Model belum tersedia. Jalankan pemodelan terlebih dahulu.",
        }

    try:
        # Panggil fungsi bawaan statsmodels untuk menghasilkan objek peramalan sebanyak n_periods
        forecast_obj = fitted_model.get_forecast(steps=n_periods)
        
        # Ambil nilai prediksi utama (garis tengah / mean)
        mean    = forecast_obj.predicted_mean
        
        # Hitung dan ambil Interval Kepercayaan (Confidence Interval) pada level signifikansi 5% (alpha=0.05).
        # Artinya, kita yakin 95% bahwa nilai aktual nanti akan jatuh di antara rentang ini.
        ci      = forecast_obj.conf_int(alpha=0.05)
        lower   = ci.iloc[:, 0] # Kolom pertama adalah batas bawah
        upper   = ci.iloc[:, 1] # Kolom kedua adalah batas atas

        # Susun semua hasil menjadi satu struktur DataFrame yang rapi untuk ditampilkan di tabel/grafik
        forecast_df = pd.DataFrame({
            "periode":     mean.index,             # Indeks waktu masa depan
            "prediksi":    mean.values.round(2),   # Nilai peramalan, dibulatkan 2 desimal
            "batas_bawah": lower.values.round(2),  # Batas bawah interval, dibulatkan
            "batas_atas":  upper.values.round(2),  # Batas atas interval, dibulatkan
        })

        # Kembalikan semua hasil jika eksekusi lancar tanpa error
        return {
            "forecast_df":    forecast_df,
            "forecast_mean":  mean,
            "forecast_lower": lower,
            "forecast_upper": upper,
            "success":        True,
            "error":          "",
        }

    except Exception as e:
        # Jika terjadi error saat memanggil metode statsmodels (misal: perhitungan matematis gagal,
        # matriks singular, atau data tidak konvergen), tangkap exception-nya
        return {
            "forecast_df":    pd.DataFrame(),
            "forecast_mean":  pd.Series(dtype=float),
            "forecast_lower": pd.Series(dtype=float),
            "forecast_upper": pd.Series(dtype=float),
            "success":        False,
            "error":          str(e), # Sertakan pesan error sistem untuk debugging
        }
