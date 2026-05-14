# ============================================================
# theme.py — CSS Kustom & Konfigurasi Tema Visual
# ============================================================

import streamlit as st
from src.utils.constants import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS,
    COLOR_WARNING, COLOR_DANGER, COLOR_BG, COLOR_CARD,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
)


def inject_global_css():
    """Menyuntikkan CSS global ke seluruh aplikasi."""
    st.markdown(f"""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Root Variables ── */
    :root {{
        --primary: {COLOR_PRIMARY};
        --secondary: {COLOR_SECONDARY};
        --success: {COLOR_SUCCESS};
        --warning: {COLOR_WARNING};
        --danger: {COLOR_DANGER};
        --bg: {COLOR_BG};
        --card: {COLOR_CARD};
        --text: {COLOR_TEXT_MAIN};
        --muted: {COLOR_TEXT_MUTED};
        --radius: 12px;
        --shadow: 0 2px 12px rgba(0,0,0,0.08);
        --shadow-hover: 0 6px 24px rgba(0,0,0,0.14);
        --transition: all 0.2s ease;
    }}

    /* ── Global Reset ── */
    html, body {{
        font-family: 'Inter', sans-serif !important;
    }}
    /* Teks utama pada konten halaman — hanya area main content, bukan sidebar */
    .main .block-container, .main .block-container * {{
        font-family: 'Inter', sans-serif !important;
    }}
    /* Elemen teks umum di luar sidebar */
    p, li, span:not([data-testid]), label:not([data-testid]) {{
        color: var(--text);
    }}

    /* ── Sidebar Toggle Button (buka/tutup) ── */
    /* Streamlit punya tombol collapse bawaan tapi tersembunyi — kita paksa tampilkan */
    /* Selector untuk tombol toggle sidebar di berbagai versi Streamlit */
    [data-testid="collapsedControl"],
    button[kind="header"],
    .st-emotion-cache-1dp5vir,
    [data-testid="stSidebarCollapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }}

    /* Style tombol toggle agar serasi dengan tema */
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] button {{
        background-color: {COLOR_PRIMARY} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0 8px 8px 0 !important;
        width: 2rem !important;
        height: 2.5rem !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {{
        background-color: {COLOR_SECONDARY} !important;
        box-shadow: 3px 3px 12px rgba(0,0,0,0.3) !important;
    }}
    /* Icon svg di dalamnya tetap putih */
    [data-testid="collapsedControl"] button svg,
    [data-testid="stSidebarCollapsedControl"] button svg {{
        fill: #ffffff !important;
        stroke: #ffffff !important;
        color: #ffffff !important;
    }}

    /* Tombol collapse/expand yang ada di dalam sidebar (tanda >) */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {{
        background-color: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50% !important;
        width: 1.8rem !important;
        height: 1.8rem !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover {{
        background-color: rgba(255,255,255,0.25) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button svg {{
        fill: #ffffff !important;
    }}

    /* ── Background ── */
    .stApp {{
        background-color: var(--bg) !important;
    }}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {{
        background: var(--primary) !important;
        border-right: none !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}

    /* ── Override Tombol Navigasi Sidebar ── */
    section[data-testid="stSidebar"] .stButton button {{
        background: transparent !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.85) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        text-align: left !important;
        padding: 0.5rem 0.8rem !important;
        transition: all 0.15s ease !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        border-left-color: rgba(33,150,243,0.6) !important;
    }}
    section[data-testid="stSidebar"] .stButton button:focus {{
        box-shadow: none !important;
        outline: none !important;
    }}
    section[data-testid="stSidebar"] .stButton button p {{
        color: inherit !important;
        font-size: inherit !important;
    }}

    section[data-testid="stSidebar"] .stRadio label {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
        padding: 4px 0 !important;
        cursor: pointer !important;
        transition: var(--transition) !important;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{
        color: #ffffff !important;
        padding-left: 4px !important;
    }}

    /* ── Hide Streamlit Default Elements ── */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px !important;
    }}

    /* ── Main Content Buttons (non-sidebar) ── */
    /* Default / secondary button */
    .main .stButton button,
    .block-container .stButton button {{
        background-color: #ffffff !important;
        color: #1E3A5F !important;
        border: 1.5px solid #cbd5e0 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 1.2rem !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        color-scheme: light !important;
    }}
    .main .stButton button:hover,
    .block-container .stButton button:hover {{
        background-color: #f0f4f8 !important;
        border-color: #a0aec0 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
        transform: translateY(-1px) !important;
    }}
    /* Primary button (type="primary") */
    .main .stButton button[kind="primary"],
    .block-container .stButton button[kind="primary"] {{
        background-color: {COLOR_SECONDARY} !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,102,204,0.35) !important;
    }}
    .main .stButton button[kind="primary"]:hover,
    .block-container .stButton button[kind="primary"]:hover {{
        background-color: #0055aa !important;
        box-shadow: 0 4px 14px rgba(0,102,204,0.45) !important;
    }}
    /* Teks dalam button selalu inherit warna button */
    .main .stButton button p,
    .block-container .stButton button p {{
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }}

    /* ── Card ── */
    .sarima-card {{
        background: var(--card);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(0,0,0,0.05);
        transition: var(--transition);
        margin-bottom: 1rem;
    }}
    .sarima-card:hover {{
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }}

    /* ── Metric Cards ── */
    .metric-card {{
        background: var(--card);
        border-radius: var(--radius);
        padding: 1.2rem 1.4rem;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--secondary);
        transition: var(--transition);
        text-align: center;
    }}
    .metric-card:hover {{
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }}
    .metric-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1.1;
    }}
    .metric-sub {{
        font-size: 0.75rem;
        color: var(--muted);
        margin-top: 0.3rem;
    }}

    /* ── Page Header ── */
    .page-header {{
        background: var(--primary);
        color: #ffffff;
        padding: 2rem 2.5rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    .page-header::after {{
        content: '';
        position: absolute;
        top: -40%;
        right: -5%;
        width: 250px;
        height: 250px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }}
    .page-header h1 {{
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }}
    .page-header p {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.95rem !important;
        margin: 0.5rem 0 0 0 !important;
    }}

    /* ── Alert Boxes ── */
    .alert {{
        padding: 0.9rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
    }}
    .alert-success {{
        background: rgba(46,204,113,0.1);
        border-left: 4px solid {COLOR_SUCCESS};
        color: #1a7a45;
    }}
    .alert-warning {{
        background: rgba(243,156,18,0.1);
        border-left: 4px solid {COLOR_WARNING};
        color: #7a5a00;
    }}
    .alert-danger {{
        background: rgba(231,76,60,0.1);
        border-left: 4px solid {COLOR_DANGER};
        color: #7a1a1a;
    }}
    .alert-info {{
        background: rgba(33,150,243,0.1);
        border-left: 4px solid {COLOR_SECONDARY};
        color: #0d47a1;
    }}

    /* ── Step Indicator ── */
    .step-flow {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1.5rem 0;
    }}
    .step-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
        flex: 1;
        min-width: 70px;
    }}
    .step-icon {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: rgba(33,150,243,0.12);
        border: 2px solid {COLOR_SECONDARY};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        transition: var(--transition);
    }}
    .step-icon.done {{
        background: {COLOR_SUCCESS};
        border-color: {COLOR_SUCCESS};
    }}
    .step-icon.active {{
        background: {COLOR_SECONDARY};
        border-color: {COLOR_SECONDARY};
        box-shadow: 0 0 0 4px rgba(33,150,243,0.2);
    }}
    .step-label {{
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--muted);
        text-align: center;
        max-width: 80px;
    }}
    .step-connector {{
        height: 2px;
        flex: 1;
        background: rgba(33,150,243,0.2);
        min-width: 10px;
        max-width: 40px;
        margin-top: -20px;
    }}

    /* ── Tabel ── */
    .dataframe {{
        border: none !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}
    .dataframe th {{
        background: {COLOR_PRIMARY} !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.03em !important;
    }}
    .dataframe td {{
        padding: 0.5rem 1rem !important;
        font-size: 0.88rem !important;
        border-bottom: 1px solid rgba(0,0,0,0.05) !important;
    }}
    .dataframe tr:hover td {{
        background: rgba(33,150,243,0.04) !important;
    }}

    /* ── Sidebar Nav Button ── */
    .nav-btn {{
        width: 100%;
        background: transparent;
        border: none;
        text-align: left;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        cursor: pointer;
        transition: var(--transition);
        color: rgba(255,255,255,0.85);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .nav-btn:hover {{
        background: rgba(255,255,255,0.1);
        color: #ffffff;
    }}
    .nav-btn.active {{
        background: rgba(33,150,243,0.25);
        color: #ffffff;
        font-weight: 600;
        border-left: 3px solid {COLOR_SECONDARY};
    }}

    /* ── Badge Status ── */
    .badge {{
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }}
    .badge-success {{ background: rgba(46,204,113,0.15); color: #1a7a45; }}
    .badge-warning {{ background: rgba(243,156,18,0.15); color: #7a5a00; }}
    .badge-danger  {{ background: rgba(231,76,60,0.15);  color: #7a1a1a; }}
    .badge-info    {{ background: rgba(33,150,243,0.15); color: #0d47a1; }}

    /* ── Section Title ── */
    .section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--primary);
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid rgba(33,150,243,0.2);
    }}

    /* ── Hero Home ── */
    .hero-container {{
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #1565C0 100%);
        border-radius: 16px;
        padding: 3rem 3.5rem;
        color: white;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }}
    .hero-container::before {{
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }}
    .hero-container::after {{
        content: '';
        position: absolute;
        bottom: -80px;
        right: 100px;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }}
    .hero-tag {{
        background: rgba(255,255,255,0.15);
        color: rgba(255,255,255,0.9);
        border-radius: 99px;
        padding: 0.25rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
    }}
    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }}
    .hero-subtitle {{
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 0.7rem;
        max-width: 600px;
        line-height: 1.6;
    }}

    /* ── Force Light Mode — override OS/browser dark preference ── */
    /* Ini memastikan semua elemen native browser (scrollbar, input, dll)
       ikut render dalam mode terang tanpa terpengaruh setting sistem. */
    :root, html, body {{
        color-scheme: light !important;
    }}

    </style>
    """, unsafe_allow_html=True)

