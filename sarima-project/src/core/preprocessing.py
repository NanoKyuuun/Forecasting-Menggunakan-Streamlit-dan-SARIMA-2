# ============================================================
# preprocessing.py — Pembersihan Data (PRD §10.4)
# ============================================================

import pandas as pd
import numpy as np


def preprocess(
    df: pd.DataFrame,
    col_period: str,
    col_value: str,
    col_category: str = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Membersihkan dataset sebelum transformasi time series.

    Returns:
        (clean_df, summary)
    """
    summary = {
        "before_rows":         len(df),
        "after_rows":          0,
        "dropped_empty":       0,
        "dropped_duplicates":  0,
        "converted_numeric":   0,
        "sorted":              True,
    }

    clean = df.copy()

    # 1. Pilih hanya kolom yang relevan
    relevant_cols = [col_period, col_value]
    if col_category and col_category in df.columns:
        relevant_cols.append(col_category)
    clean = clean[[c for c in relevant_cols if c in clean.columns]]

    # 2. Rename ke nama standar
    rename = {col_period: "periode", col_value: "nilai"}
    if col_category:
        rename[col_category] = "kategori"
    clean.rename(columns=rename, inplace=True)

    # 3. Drop baris dengan periode atau nilai kosong
    before = len(clean)
    clean.dropna(subset=["periode", "nilai"], inplace=True)
    summary["dropped_empty"] = before - len(clean)

    # 4. Konversi nilai ke numerik
    clean["nilai"] = pd.to_numeric(clean["nilai"], errors="coerce")
    summary["converted_numeric"] = clean["nilai"].isna().sum()
    clean.dropna(subset=["nilai"], inplace=True)

    # 5. Konversi periode ke datetime
    # Gunakan astype(str) agar integer (misal: 2016) tidak dibaca sebagai epoch nanosecond
    clean["periode"] = pd.to_datetime(clean["periode"].astype(str), errors="coerce")
    clean.dropna(subset=["periode"], inplace=True)

    # 6. Hapus duplikasi
    dup_cols = ["periode"] + (["kategori"] if "kategori" in clean.columns else [])
    before_dup = len(clean)
    clean.drop_duplicates(subset=dup_cols, keep="first", inplace=True)
    summary["dropped_duplicates"] = before_dup - len(clean)

    # 7. Urutkan berdasarkan periode
    sort_cols = (["kategori", "periode"] if "kategori" in clean.columns else ["periode"])
    clean.sort_values(sort_cols, inplace=True)
    clean.reset_index(drop=True, inplace=True)

    summary["after_rows"] = len(clean)

    return clean, summary
