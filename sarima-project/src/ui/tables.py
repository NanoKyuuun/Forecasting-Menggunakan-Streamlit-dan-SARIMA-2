# ============================================================
# tables.py — Komponen Tabel Reusable
# ============================================================

import pandas as pd
import streamlit as st


def show_dataframe(df: pd.DataFrame, max_rows: int = 10, use_container_width: bool = True):
    """
    Menampilkan data (DataFrame) dalam format tabel standar interaktif bawaan Streamlit.
    Hanya menampilkan n baris pertama (head) agar UI tidak melambat jika data terlalu besar.

    Args:
        df: Pandas DataFrame yang akan ditampilkan.
        max_rows: Batas maksimal baris yang ditampilkan (default: 10).
        use_container_width: Jika True, tabel akan meregang penuh menyesuaikan lebar layar.
    """
    st.dataframe(df.head(max_rows), use_container_width=use_container_width)


def show_full_table(df: pd.DataFrame, use_container_width: bool = True):
    """
    Menampilkan seluruh baris dari DataFrame tanpa ada pemotongan.
    Hati-hati digunakan untuk dataset yang barisnya sangat banyak (>10.000) karena bisa bikin lag.
    """
    st.dataframe(df, use_container_width=use_container_width)


def show_validation_table(results: list[dict]):
    """
    Fungsi khusus untuk membuat dan merender tabel HTML custom yang menampilkan 
    hasil proses validasi kelayakan dataset (dari validation.py).
    
    Tabel ini diberikan styling CSS warna-warni secara manual:
    - Hijau untuk status "✅ OK"
    - Kuning pucat untuk "⚠️ Peringatan"
    - Merah muda untuk "❌ Error"

    Args:
        results: List hasil dari fungsi validate_dataset()
                 Bentuk per item: {"check": "Nama Ujian", "status": "✅ OK", "detail": "Pesan..."}
    """
    # Siapkan string kosong penampung elemen <tr>
    rows_html = ""
    for r in results:
        status = r.get("status", "")
        
        # Tentukan warna teks (color) dan warna background (bg) baris berdasarkan status
        if status == "✅ OK":
            color = "#1a7a45"
            bg = "rgba(46,204,113,0.06)"
        elif status in ("⚠️ Peringatan", "⚠️ Warning"):
            color = "#7a5a00"
            bg = "rgba(243,156,18,0.06)"
        else:
            color = "#7a1a1a"
            bg = "rgba(231,76,60,0.06)"

        # Tambahkan 1 baris HTML untuk hasil ini
        rows_html += f"""
        <tr style="background:{bg};">
            <td style="padding:0.55rem 1rem;font-weight:500;">{r.get("check", "")}</td>
            <td style="padding:0.55rem 1rem;color:{color};font-weight:600;">{status}</td>
            <td style="padding:0.55rem 1rem;font-size:0.85rem;color:#4a5568;">{r.get("detail", "")}</td>
        </tr>"""

    # Cetak keseluruhan tabel HTML menggunakan st.markdown
    # overflow-x:auto berguna agar di layar HP tabel ini bisa di-scroll kiri-kanan
    st.markdown(
        f"""
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
            <thead>
                <tr style="background:#1E3A5F;color:white;">
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Pemeriksaan</th>
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Status</th>
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Keterangan</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_metrics_table(metrics: dict):
    """
    Fungsi khusus untuk membuat dan merender tabel HTML custom yang menampilkan 
    nilai-nilai metrik evaluasi (MAE, MSE, RMSE, MAPE).
    Dibuat dengan styling khusus agar terlihat profesional dan bersih.

    Args:
        metrics: Dictionary hasil dari calculate_metrics() di evaluation.py
    """
    # Siapkan daftar baris (tuples). Kolom nilai di-format:
    # - float biasa format ',.4f' (pemisah ribuan koma, 4 desimal)
    # - MAPE format '.2f%' (2 desimal plus tanda %)
    rows = [
        ("MAE", f"{metrics.get('MAE', 0):,.4f}", "Mean Absolute Error — rata-rata kesalahan absolut"),
        ("MSE", f"{metrics.get('MSE', 0):,.4f}", "Mean Squared Error — rata-rata kuadrat kesalahan"),
        ("RMSE", f"{metrics.get('RMSE', 0):,.4f}", "Root MSE — kesalahan dalam satuan data asli"),
        ("MAPE", f"{metrics.get('MAPE', 0):.2f}%", "Mean Absolute Percentage Error — kesalahan dalam persen"),
    ]
    
    # Loop untuk membangkitkan string tag <tr> untuk setiap baris di atas
    rows_html = "".join(
        f"""<tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
            <td style="padding:0.6rem 1rem;font-weight:700;color:#1E3A5F;">{r[0]}</td>
            <td style="padding:0.6rem 1rem;font-size:1.1rem;font-weight:600;color:#2196F3;">{r[1]}</td>
            <td style="padding:0.6rem 1rem;font-size:0.83rem;color:#718096;">{r[2]}</td>
        </tr>"""
        for r in rows
    )
    
    st.markdown(
        f"""
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
            <thead>
                <tr style="background:#1E3A5F;color:white;">
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Metrik</th>
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Nilai</th>
                    <th style="padding:0.65rem 1rem;text-align:left;font-size:0.85rem;">Keterangan</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_forecast_table(forecast_df: pd.DataFrame):
    """
    Menampilkan tabel hasil prediksi ke masa depan menggunakan tabel interaktif Streamlit,
    tetapi dengan styling tambahan khusus agar tampilannya rapi.

    Args:
        forecast_df: DataFrame output dari generate_forecast()
    """
    # .style.format() digunakan untuk memformat semua kolom bertipe numerik (angka)
    # menjadi "{:,.2f}" -> pemisah ribuan dengan koma, dan 2 angka di belakang koma (misal: 1,500.50).
    st.dataframe(
        forecast_df.style.format({
            col: "{:,.2f}" for col in forecast_df.select_dtypes("number").columns
        }),
        use_container_width=True,
    )
