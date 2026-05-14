# ============================================================
# evaluation.py — Metrik Evaluasi Model (PRD §10.8)
# ============================================================

import pandas as pd
import numpy as np
from src.utils.helpers import get_mape_interpretation


def calculate_metrics(actual: pd.Series, fitted: pd.Series) -> dict:
    """
    Menghitung berbagai metrik evaluasi standar (MAE, MSE, RMSE, MAPE) 
    untuk membandingkan seberapa cocok model dengan data aslinya.
    Fungsi ini otomatis menangani data kosong (NaN) dan pembagian dengan nol.

    Args:
        actual: pd.Series nilai historis aktual
        fitted: pd.Series nilai hasil prediksi model (in-sample)

    Returns:
        dict: Berisi metrik-metrik evaluasi dan interpretasinya. 
        Akan me-return None/NaN jika datanya kosong atau tidak selaras.
    """
    # Menyelaraskan (align) indeks waktu antara data aktual dan fitted
    # Pastikan kita hanya membandingkan baris yang indeks waktunya ada di keduanya
    common_idx = actual.index.intersection(fitted.index)
    if len(common_idx) == 0:
        # Jika tidak ada indeks yang cocok, metrik tidak bisa dihitung
        return {"MAE": None, "MSE": None, "RMSE": None, "MAPE": None}

    # Mengambil nilai numerik (array) pada indeks yang sama dan memastikannya tipe float
    y_true = actual.loc[common_idx].values.astype(float)
    y_pred = fitted.loc[common_idx].values.astype(float)

    # Memfilter dan membuang baris yang salah satunya bernilai NaN
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true = y_true[mask]
    y_pred = y_pred[mask]

    # Cek ulang setelah difilter, jika habis (kosong), hentikan perhitungan
    if len(y_true) == 0:
        return {"MAE": None, "MSE": None, "RMSE": None, "MAPE": None}

    # Mean Absolute Error (MAE): Rata-rata dari nilai absolut kesalahan (selisih aktual - prediksi)
    mae  = float(np.mean(np.abs(y_true - y_pred)))
    
    # Mean Squared Error (MSE): Rata-rata dari kuadrat kesalahan (lebih menghukum error besar)
    mse  = float(np.mean((y_true - y_pred) ** 2))
    
    # Root Mean Squared Error (RMSE): Akar dari MSE (mengembalikan skala error ke skala asal data)
    rmse = float(np.sqrt(mse))

    # Mean Absolute Percentage Error (MAPE): Rata-rata persentase kesalahan absolut
    # Sangat rentan terhadap nilai aktual 0, sehingga perlu difilter (hindari ZeroDivisionError)
    nonzero = y_true != 0
    if nonzero.sum() > 0:
        # Hitung persentase hanya pada nilai y_true yang bukan nol, lalu kali 100
        mape = float(np.mean(np.abs((y_true[nonzero] - y_pred[nonzero]) / y_true[nonzero])) * 100)
    else:
        # Jika semua data aktual nol, MAPE tidak terdefinisi
        mape = float("nan")

    return {
        "MAE":  mae,        # Rata-rata galat absolut
        "MSE":  mse,        # Rata-rata galat kuadrat
        "RMSE": rmse,       # Akar rata-rata galat kuadrat
        "MAPE": mape,       # Rata-rata persentase galat
        "n_obs": int(len(y_true)), # Jumlah observasi valid yang dihitung
        # Memanggil helper get_mape_interpretation untuk mendapatkan status teks (Sangat Baik, Baik, dst)
        "mape_interpretation": get_mape_interpretation(mape) if not np.isnan(mape) else "—",
    }
