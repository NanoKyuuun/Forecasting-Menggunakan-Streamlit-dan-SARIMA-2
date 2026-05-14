# ============================================================
# cards.py — Komponen Card & Metric Reusable
# ============================================================

import streamlit as st
from src.utils.helpers import format_number, format_percentage


def metric_card(label: str, value: str, sub: str = "", accent_color: str = "#2196F3"):
    """
    Fungsi untuk membuat sebuah komponen visual berupa 'kartu metrik' (metric card).
    Kartu ini berguna untuk menampilkan satu angka penting secara menonjol,
    misalnya "Total Data", "MAE", atau "Akurasi".

    Args:
        label: Teks judul kecil di atas angka (misal: "Total Observasi").
        value: Teks atau angka utama yang dicetak besar (misal: "1,500").
        sub: (Opsional) Teks penjelasan tambahan berukuran kecil di bawah angka.
        accent_color: Kode warna hex/rgb untuk warna teks dan garis pinggir kiri.
    """
    # Menggunakan st.markdown dengan HTML dan CSS (kelas .metric-card sudah didefinisikan di theme.py)
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {accent_color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {accent_color};">{value}</div>
            {"" if not sub else f'<div class="metric-sub">{sub}</div>'}
        </div>
        """,
        unsafe_allow_html=True, # Wajib agar tag HTML dirender sebagai elemen asli, bukan teks biasa
    )


def page_header(title: str, description: str = "", icon: str = ""):
    """
    Fungsi untuk membuat bagian kepala (header) di setiap halaman aplikasi.
    Memiliki tampilan konsisten berupa background dengan gradient biru tua (didefinisikan di theme.py).

    Args:
        title: Judul utama halaman (dicetak dengan tag <h1>).
        description: (Opsional) Paragraf penjelasan singkat di bawah judul.
        icon: (Opsional) Emoji atau entitas HTML yang ditampilkan di sebelah kiri judul.
    """
    # Siapkan elemen icon jika argumen icon diberikan
    icon_html = f'<span style="font-size:2rem;margin-right:0.7rem;">{icon}</span>' if icon else ""
    
    st.markdown(
        f"""
        <div class="page-header">
            <div style="display:flex;align-items:center;">
                {icon_html}
                <h1>{title}</h1>
            </div>
            {"" if not description else f'<p>{description}</p>'}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(content: str, padding: str = "1.5rem"):
    """
    Fungsi pembungkus sederhana untuk meletakkan teks atau elemen HTML bebas 
    ke dalam sebuah kotak (card) berlatar putih dengan bayangan yang rapi.

    Args:
        content: Isi HTML atau teks mentah yang akan dimasukkan ke dalam card.
        padding: Jarak kosong antara tepi card dan isinya.
    """
    st.markdown(
        f'<div class="sarima-card" style="padding:{padding};">{content}</div>',
        unsafe_allow_html=True,
    )


def show_metrics_row(metrics: list[dict]):
    """
    Fungsi utilitas untuk menampilkan beberapa `metric_card` sekaligus dalam satu baris (row) sejajar.
    Secara otomatis akan membagi layar menjadi sejumlah kolom yang sama besar sesuai jumlah item.

    Args:
        metrics: Daftar (list) dictionary. Tiap dictionary berisi properti untuk 1 metric_card:
                 {"label": str, "value": str, "sub": str, "color": str}
    """
    # Membagi lebar layar Streamlit menjadi beberapa kolom sebanyak isi list
    cols = st.columns(len(metrics))
    
    # Loop secara bersamaan antara kolom dan data metrik
    for col, m in zip(cols, metrics):
        # with col: menginstruksikan Streamlit agar elemen berikutnya digambar di dalam kolom tersebut
        with col:
            # Panggil fungsi pembuat kartu tunggal untuk masing-masing data
            metric_card(
                label=m.get("label", ""),
                value=m.get("value", "—"), # '—' sebagai default fallback jika kosong
                sub=m.get("sub", ""),
                accent_color=m.get("color", "#2196F3"), # Biru sebagai fallback warna standar
            )


def sarima_params_card(params: dict):
    """
    Fungsi khusus untuk membuat kartu visualisasi parameter model SARIMA.
    Menampilkan representasi rumus SARIMA lengkap beserta badge warna-warni 
    untuk tiap komponen (p, d, q) dan musiman (P, D, Q, s).

    Args:
        params: Dictionary hasil fit_sarima yang berisi angka parameter:
                {"p": int, "d": int, "q": int, "P": int, "D": int, "Q": int, "s": int}
    """
    # Ekstrak masing-masing parameter dengan fallback angka 0 (atau 1 untuk s) jika tidak ada
    p, d, q = params.get("p", 0), params.get("d", 0), params.get("q", 0)
    P, D, Q, s = params.get("P", 0), params.get("D", 0), params.get("Q", 0), params.get("s", 1)
    
    # Rangkai string formula lengkap
    formula = f"SARIMA({p},{d},{q})({P},{D},{Q})[{s}]"
    
    # Render UI: Nama formula tercetak besar, di bawahnya terdapat chip/badge kecil per parameter
    st.markdown(
        f"""
        <div class="sarima-card">
            <div class="metric-label">Model yang Digunakan</div>
            <div style="font-size:1.5rem;font-weight:800;color:#1E3A5F;margin:0.4rem 0;">{formula}</div>
            <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:0.8rem;">
                <span class="badge badge-info">p={p}</span>
                <span class="badge badge-info">d={d}</span>
                <span class="badge badge-info">q={q}</span>
                <span class="badge badge-warning">P={P}</span>
                <span class="badge badge-warning">D={D}</span>
                <span class="badge badge-warning">Q={Q}</span>
                <span class="badge badge-success">s={s}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
