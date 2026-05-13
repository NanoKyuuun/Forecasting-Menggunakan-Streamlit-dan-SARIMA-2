# ============================================================
# sidebar.py — Navigasi Sidebar dengan Status Tahapan
# ============================================================

import streamlit as st
from src.utils.constants import (
    PAGE_ORDER, PAGE_ICONS,
    SS_WORKFLOW_STATUS, SS_RAW_DATA, SS_VALIDATION_RESULT,
    SS_CLEAN_DATA, SS_TIME_SERIES, SS_MODEL_RESULT,
    SS_EVAL_METRICS, SS_FORECAST_RESULT,
    APP_TITLE, APP_VERSION,
)


def _compute_workflow_status() -> dict[str, str]:
    """
    Hitung status tiap tahapan berdasarkan session state.
    Returns dict: {page_name: "done" | "active" | "locked"}
    """
    status = {}
    current_page = st.session_state.get("current_page", PAGE_ORDER[0])

    # Kondisi "selesai" per halaman
    done_conditions = {
        "Beranda":                    True,
        "Upload Dataset":             SS_RAW_DATA in st.session_state and st.session_state[SS_RAW_DATA] is not None,
        "Validasi Data":              SS_VALIDATION_RESULT in st.session_state and st.session_state[SS_VALIDATION_RESULT] is not None,
        "Preprocessing":              SS_CLEAN_DATA in st.session_state and st.session_state[SS_CLEAN_DATA] is not None,
        "Transformasi Time Series":   SS_TIME_SERIES in st.session_state and st.session_state[SS_TIME_SERIES] is not None,
        "Analisis Time Series":       SS_TIME_SERIES in st.session_state and st.session_state[SS_TIME_SERIES] is not None,
        "Pemodelan SARIMA":           SS_MODEL_RESULT in st.session_state and st.session_state[SS_MODEL_RESULT] is not None,
        "Evaluasi Model":             SS_EVAL_METRICS in st.session_state and st.session_state[SS_EVAL_METRICS] is not None,
        "Forecasting":                SS_FORECAST_RESULT in st.session_state and st.session_state[SS_FORECAST_RESULT] is not None,
        "Perbandingan Dataset":       True,
        "Kesimpulan":                 True,
    }

    for page in PAGE_ORDER:
        is_done = done_conditions.get(page, False)
        if is_done:
            status[page] = "done"
        elif page == current_page:
            status[page] = "active"
        else:
            status[page] = "pending"

    return status


def render_sidebar():
    """Render sidebar navigasi lengkap dengan status tahapan."""
    with st.sidebar:
        # ── Logo / Brand ─────────────────────────────────────
        st.markdown(
            f"""
            <div style="padding:1.2rem 0.5rem 0.8rem 0.5rem;border-bottom:1px solid rgba(255,255,255,0.15);margin-bottom:1rem;">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.1em;opacity:0.6;text-transform:uppercase;">
                    Tugas Akhir
                </div>
                <div style="font-size:1.1rem;font-weight:800;margin-top:0.2rem;line-height:1.3;">
                    Dashboard Forecasting<br/>
                    <span style="color:rgba(33,150,243,0.9);">SARIMA</span>
                </div>
                <div style="font-size:0.7rem;opacity:0.5;margin-top:0.4rem;">v{APP_VERSION}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Menu Navigasi ─────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.08em;opacity:0.55;text-transform:uppercase;margin-bottom:0.4rem;padding:0 0.5rem;">NAVIGASI</div>',
            unsafe_allow_html=True,
        )

        current_page = st.session_state.get("current_page", PAGE_ORDER[0])
        workflow_status = _compute_workflow_status()

        for page in PAGE_ORDER:
            icon = PAGE_ICONS.get(page, "•")
            ws = workflow_status.get(page, "pending")

            # Status badge
            if ws == "done":
                badge = "✓"
                badge_color = "rgba(46,204,113,0.9)"
            else:
                badge = ""
                badge_color = "transparent"

            is_active = page == current_page
            active_style = (
                "background:rgba(33,150,243,0.2);border-left:3px solid #2196F3;font-weight:600;"
                if is_active else "border-left:3px solid transparent;"
            )

            clicked = st.button(
                f"{icon}  {page}",
                key=f"nav_{page}",
                use_container_width=True,
                help=f"Navigasi ke {page}",
            )
            if clicked:
                st.session_state["current_page"] = page
                st.rerun()

        # ── Footer Sidebar ────────────────────────────────────
        st.markdown(
            """
            <div style="
                position:fixed; bottom:0; left:0;
                padding:0.8rem 1.2rem;
                font-size:0.7rem;
                opacity:0.45;
                border-top:1px solid rgba(255,255,255,0.1);
                width:18rem;
                background:linear-gradient(160deg,#1E3A5F,#16324f);
            ">
                📌 Metode: SARIMA<br/>
                🔬 Data: Empiris & Simulasi
            </div>
            """,
            unsafe_allow_html=True,
        )
