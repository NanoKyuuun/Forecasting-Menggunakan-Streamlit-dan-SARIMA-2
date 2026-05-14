# ============================================================
# sarima_model.py — Pemodelan SARIMA (PRD §10.7, §20)
# ============================================================

import pandas as pd
import numpy as np
import warnings
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.utils.constants import (
    AUTO_P_RANGE, AUTO_D_RANGE, AUTO_Q_RANGE,
    AUTO_P_SEASONAL, AUTO_D_SEASONAL, AUTO_Q_SEASONAL,
)


def fit_sarima(
    ts: pd.Series,
    order: tuple,
    seasonal_order: tuple,
) -> dict:
    """
    Melatih (fit) model SARIMA pada data time series menggunakan parameter yang telah ditentukan.
    Fungsi ini membungkus algoritma SARIMAX dari library statsmodels dengan penanganan error.

    Args:
        ts: Data time series historis dalam bentuk pd.Series.
        order: Tuple (p, d, q) untuk komponen non-musiman (AR, I, MA).
        seasonal_order: Tuple (P, D, Q, s) untuk komponen musiman dan panjang musim/siklus (s).

    Returns:
        dict: Hasil pemodelan, berisi:
            - "model": Objek model yang telah dilatih (ARIMAResultsWrapper).
            - "params": Parameter yang digunakan.
            - "fitted": pd.Series nilai tebakan in-sample.
            - "residuals": Selisih antara nilai asli dan nilai fitted.
            - "aic", "bic": Metrik evaluasi kebaikan model (makin kecil makin baik).
            - "success": Boolean penanda keberhasilan.
            - "error": Pesan error jika gagal.
    """
    try:
        # Menangkap dan mengabaikan pesan peringatan (warnings) bawaan dari statsmodels.
        # statsmodels sering memberikan peringatan teknis seperti non-invertible roots, 
        # yang normal terjadi terutama pada auto-search, agar tidak memenuhi log aplikasi.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            # Inisialisasi arsitektur model SARIMAX
            # enforce_stationarity=False & enforce_invertibility=False mempercepat proses komputasi 
            # dan mencegah error berlebih saat mencari parameter, walau sedikit mengorbankan ketepatan.
            model = SARIMAX(
                ts,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            # Mulai melatih model. disp=False mematikan print output langkah konvergensi ke konsol.
            # maxiter=200 membatasi jumlah iterasi pencarian optimasi.
            result = model.fit(disp=False, maxiter=200)

        # Jika sukses, kembalikan semua objek relevan
        return {
            "model":     result,
            "params":    {
                "p": order[0], "d": order[1], "q": order[2],
                "P": seasonal_order[0], "D": seasonal_order[1],
                "Q": seasonal_order[2], "s": seasonal_order[3],
            },
            "fitted":    result.fittedvalues, # Nilai tebakan model pada rentang data pelatihan
            "residuals": result.resid,        # Sisa error (aktual - tebakan)
            # Ambil nilai AIC & BIC jika ada. Gunakan float() untuk konversi aman.
            "aic":       float(result.aic) if hasattr(result, "aic") else None,
            "bic":       float(result.bic) if hasattr(result, "bic") else None,
            "success":   True,
            "error":     "",
        }

    except Exception as e:
        # Jika gagal (misal: matriks tidak konvergen), tangkap exception dan kembalikan state error.
        return {
            "model":     None,
            "params":    {"p": order[0], "d": order[1], "q": order[2],
                          "P": seasonal_order[0], "D": seasonal_order[1],
                          "Q": seasonal_order[2], "s": seasonal_order[3]},
            "fitted":    pd.Series(dtype=float),
            "residuals": pd.Series(dtype=float),
            "aic":       None,
            "bic":       None,
            "success":   False,
            "error":     str(e),
        }


def auto_search_sarima(
    ts: pd.Series,
    seasonal_period: int,
    progress_callback=None,
) -> dict:
    """
    Melakukan pencarian kombinasi parameter SARIMA terbaik (Auto-ARIMA sederhana).
    Fungsi ini akan mencoba berbagai kombinasi (p,d,q)(P,D,Q,s) yang ada di daftar range,
    lalu memilih kombinasi yang menghasilkan nilai AIC (Akaike Information Criterion) paling kecil.

    Args:
        ts: Data time series
        seasonal_period: Panjang siklus musiman yang ditetapkan (misal 12 untuk bulanan)
        progress_callback: Fungsi referensi untuk mengupdate progress bar di UI Streamlit.

    Returns:
        dict: Dictionary hasil keluaran fungsi fit_sarima() yang memenangkan kompetisi AIC.
    """
    # product() akan menghasilkan kombinasi permutasi dari seluruh elemen list
    # Misal: jika p=[0,1], d=[0,1], q=[0,1] dst, ini akan membuat matriks 2x2x2... kemungkinan.
    candidates = list(product(
        AUTO_P_RANGE, AUTO_D_RANGE, AUTO_Q_RANGE,
        AUTO_P_SEASONAL, AUTO_D_SEASONAL, AUTO_Q_SEASONAL,
    ))

    # Inisialisasi dengan AIC tak terhingga (infinity) agar kombinasi valid pertama pasti menang.
    best_aic = float("inf")
    best_result = None
    total = len(candidates)

    # Lakukan loop pada semua kemungkinan kombinasi parameter
    for i, (p, d, q, P, D, Q) in enumerate(candidates):
        # Jika ada fungsi callback untuk UI, panggil untuk menggeser progress bar
        if progress_callback:
            progress_callback(i + 1, total)

        # Coba fit model menggunakan kombinasi parameter iterasi ini
        result = fit_sarima(
            ts,
            order=(p, d, q),
            seasonal_order=(P, D, Q, seasonal_period),
        )
        
        # Jika proses fit berhasil dan AIC-nya lebih kecil (lebih baik) dari rekor sebelumnya
        if result["success"] and result["aic"] is not None:
            if result["aic"] < best_aic:
                best_aic = result["aic"] # Simpan rekor baru
                best_result = result     # Simpan model terbaik sejauh ini

    # Jika semua kombinasi gagal (kasus sangat jarang), beri fallback ke model ARIMA paling basic
    if best_result is None:
        best_result = fit_sarima(ts, (1, 1, 0), (0, 0, 0, seasonal_period))

    return best_result
