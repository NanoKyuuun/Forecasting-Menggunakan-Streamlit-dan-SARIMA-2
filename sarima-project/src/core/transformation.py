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
    Mengubah clean_df menjadi time series untuk satu kategori.

    Args:
        clean_df: DataFrame hasil preprocessing (kolom: periode, nilai, [kategori])
        category: nama kategori yang dipilih (None jika tidak ada kolom kategori)

    Returns:
        (time_series, frequency_str, seasonal_period)
    """
    df = clean_df.copy()

    # Filter per kategori jika ada
    if "kategori" in df.columns and category and category != "Semua Kategori (Keseluruhan)":
        df = df[df["kategori"] == category]

    # Group by periode (sum jika ada duplikasi setelah filter)
    ts_df = df.groupby("periode")["nilai"].sum().sort_index()

    # Deteksi frekuensi
    frequency = detect_frequency(ts_df)
    seasonal_period = get_seasonal_period(frequency)

    # Set frekuensi pada index pandas
    freq_alias_map = {
        "Bulanan":    "MS",   # Month Start
        "Kuartalan":  "QS",   # Quarter Start
        "Tahunan":    "YS",   # Year Start
    }
    freq_alias = freq_alias_map.get(frequency, None)
    if freq_alias:
        try:
            ts_df.index = pd.DatetimeIndex(ts_df.index, freq=None)
            ts_df = ts_df.asfreq(freq_alias, method="pad")
        except Exception:
            pass  # Biarkan tanpa freq jika gagal set

    return ts_df, frequency, seasonal_period


def get_available_categories(clean_df: pd.DataFrame) -> list[str]:
    """Ambil daftar kategori unik dari dataframe bersih."""
    if "kategori" in clean_df.columns:
        cats = sorted(clean_df["kategori"].dropna().unique().tolist())
        return ["Semua Kategori (Keseluruhan)"] + cats
    return []


def get_descriptive_stats(ts: pd.Series) -> dict:
    """Hitung statistik deskriptif dasar untuk time series."""
    changes = ts.diff().dropna()
    return {
        "n_obs":      len(ts),
        "min":        float(ts.min()),
        "max":        float(ts.max()),
        "mean":       float(ts.mean()),
        "std":        float(ts.std()),
        "start":      str(ts.index[0].date()) if hasattr(ts.index[0], "date") else str(ts.index[0]),
        "end":        str(ts.index[-1].date()) if hasattr(ts.index[-1], "date") else str(ts.index[-1]),
        "max_change": float(changes.max()) if len(changes) > 0 else 0.0,
        "min_change": float(changes.min()) if len(changes) > 0 else 0.0,
    }
