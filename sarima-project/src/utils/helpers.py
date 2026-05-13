# ============================================================
# helpers.py — Fungsi Pembantu Umum
# ============================================================

import pandas as pd
import numpy as np
from datetime import datetime


def format_number(value: float, decimals: int = 2) -> str:
    """Format angka menjadi string dengan pemisah ribuan."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    try:
        if decimals == 0:
            return f"{int(value):,}"
        return f"{value:,.{decimals}f}"
    except Exception:
        return str(value)


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format angka sebagai persentase."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    return f"{value:.{decimals}f}%"


def get_data_quality_label(n_obs: int) -> tuple[str, str]:
    """
    Mengembalikan (label, level) berdasarkan jumlah observasi.
    level: 'danger' | 'warning' | 'info' | 'success'
    """
    if n_obs < 10:
        return "Sangat Terbatas", "danger"
    elif n_obs < 31:
        return "Terbatas", "warning"
    elif n_obs < 61:
        return "Cukup", "info"
    else:
        return "Baik", "success"


def get_mape_interpretation(mape: float) -> str:
    """Interpretasi nilai MAPE."""
    if mape < 10:
        return "Sangat Akurat (MAPE < 10%)"
    elif mape < 20:
        return "Baik (MAPE 10%–20%)"
    elif mape < 50:
        return "Cukup (MAPE 20%–50%)"
    else:
        return "Kurang Akurat (MAPE > 50%)"


def detect_frequency(series: pd.Series) -> str:
    """Deteksi frekuensi data dari index datetime."""
    if len(series) < 2:
        return "unknown"
    try:
        diff = pd.Series(series.index).diff().dropna()
        median_days = diff.dt.days.median()
        if median_days <= 32:
            return "Bulanan"
        elif median_days <= 100:
            return "Kuartalan"
        else:
            return "Tahunan"
    except Exception:
        return "unknown"


def get_seasonal_period(frequency: str) -> int:
    """Mendapatkan periode musiman berdasarkan frekuensi."""
    mapping = {
        "Bulanan": 12,
        "Kuartalan": 4,
        "Tahunan": 1,
    }
    return mapping.get(frequency, 1)


def now_str() -> str:
    """Timestamp saat ini dalam string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_export_str() -> str:
    """Timestamp untuk nama file export."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
