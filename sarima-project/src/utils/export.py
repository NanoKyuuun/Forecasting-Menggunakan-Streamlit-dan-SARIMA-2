# ============================================================
# export.py — Fungsi Export Hasil Forecast ke CSV
# ============================================================

import pandas as pd
import io
from datetime import datetime
from src.utils.helpers import date_export_str


def build_forecast_csv(
    forecast_df: pd.DataFrame,
    sarima_params: dict,
    category: str,
) -> bytes:
    """
    Membangun konten CSV dari hasil forecast.

    Args:
        forecast_df: DataFrame dengan kolom periode, prediksi, lower, upper
        sarima_params: dict berisi parameter SARIMA yang digunakan
        category: nama kategori/program studi

    Returns:
        bytes: konten CSV siap download
    """
    export_df = forecast_df.copy()

    # Tambahkan metadata kolom
    export_df.insert(0, "kategori", category)
    export_df["parameter_SARIMA"] = (
        f"SARIMA({sarima_params.get('p', 0)},{sarima_params.get('d', 0)},{sarima_params.get('q', 0)})"
        f"({sarima_params.get('P', 0)},{sarima_params.get('D', 0)},{sarima_params.get('Q', 0)})"
        f"[{sarima_params.get('s', 1)}]"
    )
    export_df["tanggal_export"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pastikan nama kolom konsisten
    rename_map = {}
    for col in export_df.columns:
        lower = col.lower()
        if "period" in lower or "tanggal" in lower or "bulan" in lower or "tahun" in lower:
            if col not in ("tanggal_export",):
                rename_map[col] = "periode_forecast"
        elif "pred" in lower or "forecast" in lower or "nilai" in lower:
            rename_map[col] = "nilai_prediksi"
        elif "lower" in lower or "bawah" in lower:
            rename_map[col] = "batas_bawah"
        elif "upper" in lower or "atas" in lower:
            rename_map[col] = "batas_atas"
    export_df.rename(columns=rename_map, inplace=True)

    buffer = io.StringIO()
    export_df.to_csv(buffer, index=False, encoding="utf-8-sig")
    return buffer.getvalue().encode("utf-8-sig")


def get_download_filename(category: str) -> str:
    """Generate nama file download."""
    safe_cat = category.replace(" ", "_").replace("/", "-")
    return f"forecast_{safe_cat}_{date_export_str()}.csv"
