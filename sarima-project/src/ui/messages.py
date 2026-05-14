# ============================================================
# messages.py — Komponen Pesan (Alert/Info/Warning/Error)
# ============================================================

import streamlit as st


def show_success(message: str, icon: str = "✅"):
    """
    Menampilkan kotak pesan (alert) berwarna hijau untuk indikasi keberhasilan.
    Digunakan saat proses upload berhasil, model selesai dilatih, dsb.
    """
    st.markdown(
        f'<div class="alert alert-success"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_warning(message: str, icon: str = "⚠️"):
    """
    Menampilkan kotak pesan (alert) berwarna kuning/oranye untuk peringatan.
    Digunakan saat ada data yang kurang ideal tapi proses masih bisa dilanjut (misal missing value sikit).
    """
    st.markdown(
        f'<div class="alert alert-warning"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_error(message: str, icon: str = "❌"):
    """
    Menampilkan kotak pesan (alert) berwarna merah untuk error fatal.
    Digunakan saat proses harus dihentikan (misal: format file salah, data tidak cukup).
    """
    st.markdown(
        f'<div class="alert alert-danger"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_info(message: str, icon: str = "ℹ️"):
    """
    Menampilkan kotak pesan (alert) berwarna biru untuk informasi umum.
    Digunakan untuk memberikan panduan atau instruksi kepada user.
    """
    st.markdown(
        f'<div class="alert alert-info"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_methodological_note(message: str):
    """
    Menampilkan kotak peringatan khusus bertema 'Catatan Metodologis'.
    Fungsi ini khusus dibuat untuk keperluan akademis, di mana keterbatasan data 
    (seperti jumlah sampel yang sedikit) perlu di-disclaimer agar validitas penelitian terjaga.

    Args:
        message: Teks peringatan/keterbatasan metodologi.
    """
    st.markdown(
        f"""
        <div class="alert alert-warning" style="margin-top:1rem;">
            <span>📌</span>
            <div>
                <strong>Catatan Metodologis:</strong><br/>
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_simulation_note():
    """
    Menampilkan kotak informasi khusus yang menyatakan bahwa data yang sedang 
    dipakai adalah data simulasi (bukan data lapangan asli).
    Digunakan saat user menekan tombol 'Gunakan Data Simulasi' di halaman awal.
    """
    st.markdown(
        """
        <div class="alert alert-info" style="margin-top:0.5rem;">
            <span>🔬</span>
            <div>
                <strong>Data Simulasi:</strong>
                Data bulanan digunakan sebagai data simulasi pembanding untuk menguji performa
                dashboard pada struktur data yang lebih sesuai dengan pemodelan SARIMA.
                Data ini bukan data empiris resmi.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_section_title(title: str):
    """
    Menampilkan teks judul bagian (section) yang dicetak tebal dengan garis bawah.
    Berguna untuk membagi area UI menjadi sub-bagian yang rapi.
    
    Args:
        title: Teks judul.
    """
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def show_badge(label: str, level: str = "info") -> str:
    """
    Menghasilkan string HTML untuk membuat elemen badge (label kecil melingkar).
    Fungsi ini tidak langsung mencetak ke Streamlit (tidak pakai st.markdown), 
    melainkan me-return string HTML agar bisa disisipkan ke dalam teks lain.

    Args:
        label: Teks di dalam badge.
        level: Warna tema (info=biru, success=hijau, warning=kuning, danger=merah).
        
    Returns:
        str: String tag HTML badge siap pakai.
    """
    return f'<span class="badge badge-{level}">{label}</span>'
