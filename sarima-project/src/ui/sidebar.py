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


def _inject_sidebar_toggle_js():
    """
    Inject tombol ☰ floating yang muncul saat sidebar tertutup.
    Streamlit menyembunyikan tombol buka sidebar via JavaScript,
    sehingga CSS override tidak cukup — perlu JS injection.
    """
    st.markdown("""
    <style>
    /* Tombol floating untuk membuka sidebar */
    #sarima-sidebar-open-btn {
        position: fixed;
        top: 50%;
        left: 0;
        transform: translateY(-50%);
        z-index: 99999;
        background: #0D3B66;
        color: white;
        border: none;
        border-radius: 0 8px 8px 0;
        width: 2rem;
        height: 3rem;
        cursor: pointer;
        font-size: 1.1rem;
        display: none;          /* default tersembunyi */
        align-items: center;
        justify-content: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
    }
    #sarima-sidebar-open-btn:hover {
        background: #0066CC;
        width: 2.4rem;
    }
    </style>

    <!-- Tombol floating -->
    <button id="sarima-sidebar-open-btn" title="Buka Navigasi">☰</button>

    <script>
    (function() {
        const btn = document.getElementById('sarima-sidebar-open-btn');
        if (!btn) return;

        // Klik tombol floating → klik tombol native Streamlit
        btn.addEventListener('click', function() {
            // Coba berbagai selector yang Streamlit gunakan
            const selectors = [
                '[data-testid="stSidebarCollapsedControl"] button',
                '[data-testid="collapsedControl"] button',
                'button[aria-label="Open sidebar"]',
                'button[aria-label="open sidebar"]',
                'section[data-testid="stSidebarCollapsedControl"] button',
            ];
            for (const sel of selectors) {
                const native = document.querySelector(sel);
                if (native) { native.click(); break; }
            }
        });

        // Amati perubahan DOM: tampilkan/sembunyikan sesuai state sidebar
        function checkSidebar() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;

            // Streamlit menambahkan aria-expanded atau mengubah class saat sidebar collapsed
            const isCollapsed =
                sidebar.getAttribute('aria-expanded') === 'false' ||
                sidebar.classList.contains('st-emotion-cache-collapsed') ||
                getComputedStyle(sidebar).transform.includes('matrix') ||
                sidebar.style.marginLeft === '-21rem' ||
                sidebar.offsetWidth < 10;

            btn.style.display = isCollapsed ? 'flex' : 'none';
        }

        // Jalankan segera dan amati perubahan
        checkSidebar();
        const observer = new MutationObserver(checkSidebar);
        observer.observe(document.body, { attributes: true, childList: true, subtree: true });

        // Fallback: cek setiap 500ms (jika MutationObserver miss event)
        setInterval(checkSidebar, 500);
    })();
    </script>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigasi lengkap dengan status tahapan."""
    # Inject tombol floating buka sidebar (di luar with st.sidebar)
    _inject_sidebar_toggle_js()

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
