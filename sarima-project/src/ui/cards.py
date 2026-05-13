# ============================================================
# cards.py — Komponen Card & Metric Reusable
# ============================================================

import streamlit as st
from src.utils.helpers import format_number, format_percentage


def metric_card(label: str, value: str, sub: str = "", accent_color: str = "#2196F3"):
    """Card metrik tunggal dengan label, nilai, dan sub-teks."""
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {accent_color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {accent_color};">{value}</div>
            {"" if not sub else f'<div class="metric-sub">{sub}</div>'}
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, description: str = "", icon: str = ""):
    """Header halaman dengan gradient biru tua."""
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
    """Card putih dengan konten HTML bebas."""
    st.markdown(
        f'<div class="sarima-card" style="padding:{padding};">{content}</div>',
        unsafe_allow_html=True,
    )


def show_metrics_row(metrics: list[dict]):
    """
    Tampilkan baris metric card.
    metrics = [{"label": str, "value": str, "sub": str, "color": str}]
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            metric_card(
                label=m.get("label", ""),
                value=m.get("value", "—"),
                sub=m.get("sub", ""),
                accent_color=m.get("color", "#2196F3"),
            )


def sarima_params_card(params: dict):
    """Card tampilan parameter SARIMA."""
    p, d, q = params.get("p", 0), params.get("d", 0), params.get("q", 0)
    P, D, Q, s = params.get("P", 0), params.get("D", 0), params.get("Q", 0), params.get("s", 1)
    formula = f"SARIMA({p},{d},{q})({P},{D},{Q})[{s}]"
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
