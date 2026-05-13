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
    Generate prediksi untuk n_periods periode ke depan.

    Args:
        model_result: hasil dari fit_sarima()
        n_periods: jumlah periode yang akan diprediksi

    Returns:
        {
            "forecast_df": pd.DataFrame (periode, prediksi, batas_bawah, batas_atas),
            "forecast_mean": pd.Series,
            "forecast_lower": pd.Series,
            "forecast_upper": pd.Series,
            "success": bool,
            "error": str,
        }
    """
    fitted_model = model_result.get("model")
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
        forecast_obj = fitted_model.get_forecast(steps=n_periods)
        mean    = forecast_obj.predicted_mean
        ci      = forecast_obj.conf_int(alpha=0.05)
        lower   = ci.iloc[:, 0]
        upper   = ci.iloc[:, 1]

        forecast_df = pd.DataFrame({
            "periode":     mean.index,
            "prediksi":    mean.values.round(2),
            "batas_bawah": lower.values.round(2),
            "batas_atas":  upper.values.round(2),
        })

        return {
            "forecast_df":    forecast_df,
            "forecast_mean":  mean,
            "forecast_lower": lower,
            "forecast_upper": upper,
            "success":        True,
            "error":          "",
        }

    except Exception as e:
        return {
            "forecast_df":    pd.DataFrame(),
            "forecast_mean":  pd.Series(dtype=float),
            "forecast_lower": pd.Series(dtype=float),
            "forecast_upper": pd.Series(dtype=float),
            "success":        False,
            "error":          str(e),
        }
