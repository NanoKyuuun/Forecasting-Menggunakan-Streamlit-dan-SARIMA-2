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
    Fit model SARIMA dengan parameter manual.

    Args:
        ts: Time series pd.Series
        order: (p, d, q)
        seasonal_order: (P, D, Q, s)

    Returns:
        {
            "model": fitted model,
            "params": dict,
            "fitted": pd.Series,
            "residuals": pd.Series,
            "aic": float | None,
            "bic": float | None,
            "success": bool,
            "error": str,
        }
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = SARIMAX(
                ts,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            result = model.fit(disp=False, maxiter=200)

        return {
            "model":     result,
            "params":    {
                "p": order[0], "d": order[1], "q": order[2],
                "P": seasonal_order[0], "D": seasonal_order[1],
                "Q": seasonal_order[2], "s": seasonal_order[3],
            },
            "fitted":    result.fittedvalues,
            "residuals": result.resid,
            "aic":       float(result.aic) if hasattr(result, "aic") else None,
            "bic":       float(result.bic) if hasattr(result, "bic") else None,
            "success":   True,
            "error":     "",
        }

    except Exception as e:
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
    Auto-search parameter SARIMA dalam range terbatas (PRD §20.3).
    Pilih model dengan AIC terkecil.

    Args:
        ts: Time series
        seasonal_period: panjang musiman (misal 12 untuk bulanan)
        progress_callback: fungsi(current, total) untuk update UI

    Returns:
        dict hasil fit_sarima terbaik
    """
    candidates = list(product(
        AUTO_P_RANGE, AUTO_D_RANGE, AUTO_Q_RANGE,
        AUTO_P_SEASONAL, AUTO_D_SEASONAL, AUTO_Q_SEASONAL,
    ))

    best_aic = float("inf")
    best_result = None
    total = len(candidates)

    for i, (p, d, q, P, D, Q) in enumerate(candidates):
        if progress_callback:
            progress_callback(i + 1, total)

        result = fit_sarima(
            ts,
            order=(p, d, q),
            seasonal_order=(P, D, Q, seasonal_period),
        )
        if result["success"] and result["aic"] is not None:
            if result["aic"] < best_aic:
                best_aic = result["aic"]
                best_result = result

    if best_result is None:
        # Fallback ke model paling sederhana
        best_result = fit_sarima(ts, (1, 1, 0), (0, 0, 0, seasonal_period))

    return best_result
