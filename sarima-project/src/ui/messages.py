# ============================================================
# messages.py — Komponen Pesan (Alert/Info/Warning/Error)
# ============================================================

import streamlit as st


def show_success(message: str, icon: str = "✅"):
    st.markdown(
        f'<div class="alert alert-success"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_warning(message: str, icon: str = "⚠️"):
    st.markdown(
        f'<div class="alert alert-warning"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_error(message: str, icon: str = "❌"):
    st.markdown(
        f'<div class="alert alert-danger"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_info(message: str, icon: str = "ℹ️"):
    st.markdown(
        f'<div class="alert alert-info"><span>{icon}</span><span>{message}</span></div>',
        unsafe_allow_html=True,
    )


def show_methodological_note(message: str):
    """Catatan metodologis khusus untuk pembatasan interpretasi."""
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
    """Catatan bahwa data yang digunakan adalah data simulasi."""
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
    """Tampilkan judul seksi dengan garis bawah."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def show_badge(label: str, level: str = "info") -> str:
    """Return HTML badge string."""
    return f'<span class="badge badge-{level}">{label}</span>'
