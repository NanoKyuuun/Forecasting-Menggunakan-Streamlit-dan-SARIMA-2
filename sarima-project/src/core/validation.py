# ============================================================
# validation.py — Validasi Kelayakan Dataset (PRD §19)
# ============================================================

import pandas as pd
import numpy as np
from src.utils.constants import OBS_VERY_LIMITED, OBS_LIMITED, OBS_ADEQUATE
from src.utils.helpers import get_data_quality_label


def validate_dataset(
    df: pd.DataFrame,
    col_period: str,
    col_value: str,
    col_category: str = None,
) -> dict:
    """
    Menjalankan seluruh validasi dataset sesuai PRD §19.

    Returns:
        {
            "is_valid": bool,
            "checks": [{"check": str, "status": str, "detail": str}],
            "warnings": [str],
            "errors": [str],
            "n_obs": int,
            "quality_label": str,
            "quality_level": str,
        }
    """
    checks = []
    warnings = []
    errors = []

    # ── 1. Cek Kolom Wajib ──────────────────────────────────
    missing_cols = []
    for col in [col_period, col_value]:
        if col not in df.columns:
            missing_cols.append(col)
    if col_category and col_category not in df.columns:
        missing_cols.append(col_category)

    if missing_cols:
        checks.append({
            "check": "Kolom Wajib",
            "status": "❌ Error",
            "detail": f"Kolom tidak ditemukan: {', '.join(missing_cols)}",
        })
        errors.append(f"Kolom wajib tidak ditemukan: {', '.join(missing_cols)}")
    else:
        checks.append({
            "check": "Kolom Wajib",
            "status": "✅ OK",
            "detail": f"Kolom '{col_period}', '{col_value}'" + (f", '{col_category}'" if col_category else "") + " tersedia.",
        })

    # ── 2. Cek Missing Value ─────────────────────────────────
    mv_period = df[col_period].isna().sum() if col_period in df.columns else 0
    mv_value  = df[col_value].isna().sum()  if col_value in df.columns else 0
    total_mv  = mv_period + mv_value

    if total_mv == 0:
        checks.append({"check": "Missing Value", "status": "✅ OK", "detail": "Tidak ada nilai kosong."})
    elif total_mv < len(df) * 0.1:
        checks.append({"check": "Missing Value", "status": "⚠️ Peringatan", "detail": f"Ditemukan {total_mv} nilai kosong (akan ditangani preprocessing)."})
        warnings.append(f"Terdapat {total_mv} missing value.")
    else:
        checks.append({"check": "Missing Value", "status": "❌ Error", "detail": f"Terlalu banyak missing value: {total_mv} ({total_mv/len(df)*100:.1f}%)."})
        errors.append(f"Missing value terlalu banyak: {total_mv}.")

    # ── 3. Cek Duplikasi ─────────────────────────────────────
    if col_period in df.columns and col_value in df.columns:
        dup_cols = [col_period] + ([col_category] if col_category and col_category in df.columns else [])
        n_dup = df.duplicated(subset=dup_cols).sum()
        if n_dup == 0:
            checks.append({"check": "Duplikasi Data", "status": "✅ OK", "detail": "Tidak ada duplikasi."})
        else:
            checks.append({"check": "Duplikasi Data", "status": "⚠️ Peringatan", "detail": f"Ditemukan {n_dup} baris duplikat."})
            warnings.append(f"Terdapat {n_dup} baris duplikat.")

    # ── 4. Cek Tipe Data Numerik ─────────────────────────────
    if col_value in df.columns:
        non_num = pd.to_numeric(df[col_value], errors="coerce").isna().sum() - df[col_value].isna().sum()
        if non_num == 0:
            checks.append({"check": "Tipe Data Numerik", "status": "✅ OK", "detail": f"Kolom '{col_value}' berisi nilai numerik."})
        else:
            checks.append({"check": "Tipe Data Numerik", "status": "❌ Error", "detail": f"{non_num} nilai non-numerik ditemukan di kolom '{col_value}'."})
            errors.append(f"Kolom nilai mengandung {non_num} entri non-numerik.")

    # ── 5. Cek Format Periode ────────────────────────────────
    if col_period in df.columns:
        parsed = pd.to_datetime(df[col_period].astype(str), errors="coerce")
        n_invalid = parsed.isna().sum()
        if n_invalid == 0:
            checks.append({"check": "Format Periode", "status": "✅ OK", "detail": "Format periode dapat dibaca sebagai tanggal/tahun."})
        elif n_invalid < len(df) * 0.2:
            checks.append({"check": "Format Periode", "status": "⚠️ Peringatan", "detail": f"{n_invalid} periode tidak dapat diparse (pastikan format konsisten)."})
            warnings.append(f"{n_invalid} periode tidak dapat diparsing.")
        else:
            checks.append({"check": "Format Periode", "status": "❌ Error", "detail": f"{n_invalid} dari {len(df)} periode tidak valid. Cek format kolom periode."})
            errors.append(f"Format periode tidak valid: {n_invalid} baris.")

    # ── 6. Cek Jumlah Observasi ──────────────────────────────
    # Hitung per kategori jika ada
    if col_category and col_category in df.columns and col_period in df.columns:
        # Ambil jumlah period unik per kategori (worst case)
        n_obs = df.groupby(col_category)[col_period].nunique().min()
        detail_obs = f"Min. {n_obs} observasi per kategori (dari {df[col_category].nunique()} kategori)"
    else:
        n_obs = len(df)
        detail_obs = f"Total {n_obs} observasi"

    quality_label, quality_level = get_data_quality_label(n_obs)
    status_obs = "✅ OK" if quality_level in ("success", "info") else "⚠️ Peringatan"
    checks.append({
        "check": "Jumlah Observasi",
        "status": status_obs,
        "detail": f"{detail_obs} — Kualitas: {quality_label}",
    })
    if quality_level in ("danger", "warning"):
        warnings.append(f"Jumlah observasi terbatas ({n_obs}). Hasil forecast perlu diinterpretasi hati-hati.")

    # ── Hasil Akhir ──────────────────────────────────────────
    is_valid = len(errors) == 0
    return {
        "is_valid":      is_valid,
        "checks":        checks,
        "warnings":      warnings,
        "errors":        errors,
        "n_obs":         n_obs,
        "quality_label": quality_label,
        "quality_level": quality_level,
    }
