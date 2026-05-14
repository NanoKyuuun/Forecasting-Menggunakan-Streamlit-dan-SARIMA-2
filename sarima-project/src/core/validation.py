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
    Menjalankan serangkaian uji kelayakan pada dataset mentah sebelum masuk ke tahap preprocessing.
    Ini sesuai dengan dokumen PRD Bab 19 untuk mencegah error di tengah jalan akibat data yang buruk.

    Args:
        df: DataFrame mentah yang baru saja di-load oleh user.
        col_period: Nama kolom yang dipilih sebagai waktu/periode.
        col_value: Nama kolom yang dipilih sebagai nilai target.
        col_category: (Opsional) Nama kolom yang dipilih sebagai kategori.

    Returns:
        dict: Hasil evaluasi komprehensif berisi:
            - "is_valid": boolean (True jika tidak ada error fatal/blocker)
            - "checks": list of dict, rincian tiap uji (status, detail pesan) untuk UI
            - "warnings": list of string, kumpulan peringatan yang tidak menghentikan proses
            - "errors": list of string, kumpulan error fatal yang membuat is_valid = False
            - "n_obs": integer, jumlah minimum observasi yang ditemukan
            - "quality_label": string teks interpretasi kualitas (misal: "Sangat Terbatas")
            - "quality_level": string badge level untuk UI (misal: "danger", "success")
    """
    # Inisialisasi wadah penampung hasil uji
    checks = []
    warnings = []
    errors = []

    # ── 1. Cek Kolom Wajib ──────────────────────────────────
    # Pastikan kolom yang dipilih user benar-benar eksis di dalam dataset.
    # Meskipun UI dropdown sudah membatasi, pengecekan ini penting di level backend/core.
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

    # ── 2. Cek Missing Value (Data Kosong) ─────────────────────────────────
    # Hitung jumlah baris yang memiliki nilai NaN/null pada kolom waktu atau nilai
    mv_period = df[col_period].isna().sum() if col_period in df.columns else 0
    mv_value  = df[col_value].isna().sum()  if col_value in df.columns else 0
    total_mv  = mv_period + mv_value

    if total_mv == 0:
        checks.append({"check": "Missing Value", "status": "✅ OK", "detail": "Tidak ada nilai kosong."})
    elif total_mv < len(df) * 0.1: # Toleransi: Jika missing value kurang dari 10% total data
        checks.append({"check": "Missing Value", "status": "⚠️ Peringatan", "detail": f"Ditemukan {total_mv} nilai kosong (akan ditangani preprocessing)."})
        warnings.append(f"Terdapat {total_mv} missing value.")
    else: # Jika missing value > 10%, anggap fatal karena imputasi/pembersihan akan terlalu merusak struktur data
        checks.append({"check": "Missing Value", "status": "❌ Error", "detail": f"Terlalu banyak missing value: {total_mv} ({total_mv/len(df)*100:.1f}%)."})
        errors.append(f"Missing value terlalu banyak: {total_mv}.")

    # ── 3. Cek Duplikasi ─────────────────────────────────────
    # Mengecek apakah ada data dengan waktu yang sama (dan kategori yang sama).
    if col_period in df.columns and col_value in df.columns:
        dup_cols = [col_period] + ([col_category] if col_category and col_category in df.columns else [])
        n_dup = df.duplicated(subset=dup_cols).sum()
        if n_dup == 0:
            checks.append({"check": "Duplikasi Data", "status": "✅ OK", "detail": "Tidak ada duplikasi."})
        else:
            checks.append({"check": "Duplikasi Data", "status": "⚠️ Peringatan", "detail": f"Ditemukan {n_dup} baris duplikat."})
            warnings.append(f"Terdapat {n_dup} baris duplikat.")

    # ── 4. Cek Tipe Data Numerik ─────────────────────────────
    # Memastikan kolom nilai target benar-benar berisi angka, bukan hanya teks sembarangan.
    if col_value in df.columns:
        # Konversi paksa ke angka. Nilai teks murni akan jadi NaN.
        # Hitung selisih NaN baru vs NaN bawaan untuk melihat berapa banyak teks non-angka.
        non_num = pd.to_numeric(df[col_value], errors="coerce").isna().sum() - df[col_value].isna().sum()
        if non_num == 0:
            checks.append({"check": "Tipe Data Numerik", "status": "✅ OK", "detail": f"Kolom '{col_value}' berisi nilai numerik."})
        else:
            checks.append({"check": "Tipe Data Numerik", "status": "❌ Error", "detail": f"{non_num} nilai non-numerik ditemukan di kolom '{col_value}'."})
            errors.append(f"Kolom nilai mengandung {non_num} entri non-numerik.")

    # ── 5. Cek Format Periode ────────────────────────────────
    # Memastikan kolom waktu bisa diparsing (diubah) menjadi objek datetime oleh Pandas.
    if col_period in df.columns:
        parsed = pd.to_datetime(df[col_period].astype(str), errors="coerce")
        n_invalid = parsed.isna().sum()
        if n_invalid == 0:
            checks.append({"check": "Format Periode", "status": "✅ OK", "detail": "Format periode dapat dibaca sebagai tanggal/tahun."})
        elif n_invalid < len(df) * 0.2: # Toleransi 20% format aneh
            checks.append({"check": "Format Periode", "status": "⚠️ Peringatan", "detail": f"{n_invalid} periode tidak dapat diparse (pastikan format konsisten)."})
            warnings.append(f"{n_invalid} periode tidak dapat diparsing.")
        else:
            checks.append({"check": "Format Periode", "status": "❌ Error", "detail": f"{n_invalid} dari {len(df)} periode tidak valid. Cek format kolom periode."})
            errors.append(f"Format periode tidak valid: {n_invalid} baris.")

    # ── 6. Cek Jumlah Observasi ──────────────────────────────
    # Syarat mutlak SARIMA: butuh data historis yang cukup panjang untuk menangkap pola musim dan tren.
    if col_category and col_category in df.columns and col_period in df.columns:
        # Jika ada kategori, ambil kelompok kategori dengan jumlah data (baris) paling sedikit (worst case scenario)
        n_obs = df.groupby(col_category)[col_period].nunique().min()
        detail_obs = f"Min. {n_obs} observasi per kategori (dari {df[col_category].nunique()} kategori)"
    else:
        # Jika tanpa kategori, hitung total baris biasa
        n_obs = len(df)
        detail_obs = f"Total {n_obs} observasi"

    # Evaluasi kualitas berdasarkan standar jumlah baris (Sangat Terbatas, Terbatas, Cukup, dst)
    quality_label, quality_level = get_data_quality_label(n_obs)
    
    # Jika kualitas masuk zona merah (danger) atau kuning (warning), berikan peringatan ekstra
    status_obs = "✅ OK" if quality_level in ("success", "info") else "⚠️ Peringatan"
    checks.append({
        "check": "Jumlah Observasi",
        "status": status_obs,
        "detail": f"{detail_obs} — Kualitas: {quality_label}",
    })
    
    if quality_level in ("danger", "warning"):
        warnings.append(f"Jumlah observasi terbatas ({n_obs}). Hasil forecast perlu diinterpretasi hati-hati.")

    # ── Hasil Akhir ──────────────────────────────────────────
    # Dataset dinyatakan VALID dan boleh diproses lanjut HANYA JIKA tidak ada ERROR fatal sama sekali.
    # Peringatan (warnings) masih diizinkan lolos.
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
