# ============================================================
# evaluation.py — Metrik Evaluasi Model (PRD §10.8)
# ============================================================

import pandas as pd
import numpy as np
from src.utils.helpers import get_mape_interpretation


def calculate_metrics(actual: pd.Series, fitted: pd.Series) -> dict:
    """
    Hitung MAE, MSE, RMSE, MAPE dari nilai aktual dan fitted.

    Args:
        actual: pd.Series nilai aktual
        fitted: pd.Series nilai fitted model

    Returns:
        dict metrik evaluasi
    """
    # Align index
    common_idx = actual.index.intersection(fitted.index)
    if len(common_idx) == 0:
        return {"MAE": None, "MSE": None, "RMSE": None, "MAPE": None}

    y_true = actual.loc[common_idx].values.astype(float)
    y_pred = fitted.loc[common_idx].values.astype(float)

    # Filter NaN
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true = y_true[mask]
    y_pred = y_pred[mask]

    if len(y_true) == 0:
        return {"MAE": None, "MSE": None, "RMSE": None, "MAPE": None}

    mae  = float(np.mean(np.abs(y_true - y_pred)))
    mse  = float(np.mean((y_true - y_pred) ** 2))
    rmse = float(np.sqrt(mse))

    # MAPE — hindari pembagian nol
    nonzero = y_true != 0
    if nonzero.sum() > 0:
        mape = float(np.mean(np.abs((y_true[nonzero] - y_pred[nonzero]) / y_true[nonzero])) * 100)
    else:
        mape = float("nan")

    return {
        "MAE":  mae,
        "MSE":  mse,
        "RMSE": rmse,
        "MAPE": mape,
        "n_obs": int(len(y_true)),
        "mape_interpretation": get_mape_interpretation(mape) if not np.isnan(mape) else "—",
    }
