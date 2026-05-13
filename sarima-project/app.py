# ============================================================
# app.py — Entry Point Dashboard Forecasting SARIMA
# ============================================================

import streamlit as st
import sys
import os

# Tambahkan root project ke path agar import src.* bekerja
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.constants import (
    PAGE_HOME, PAGE_UPLOAD, PAGE_VALIDATION, PAGE_PREPROCESSING,
    PAGE_TRANSFORMATION, PAGE_ANALYSIS, PAGE_MODELING,
    PAGE_EVALUATION, PAGE_FORECASTING, PAGE_COMPARISON, PAGE_CONCLUSION,
    SS_RAW_DATA, SS_CLEAN_DATA, SS_VALIDATION_RESULT, SS_TIME_SERIES,
    SS_SELECTED_CATEGORY, SS_SARIMA_PARAMS, SS_MODEL_RESULT,
    SS_EVAL_METRICS, SS_FORECAST_RESULT, SS_WORKFLOW_STATUS,
    SS_COL_MAPPING, SS_DATA_FREQUENCY, SS_FILE_NAME,
    APP_TITLE,
)
from src.ui.theme import inject_global_css
from src.ui.sidebar import render_sidebar


# ── Konfigurasi Halaman ────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state():
    """Inisialisasi semua session state key yang diperlukan."""
    defaults = {
        "current_page":      PAGE_HOME,
        SS_RAW_DATA:         None,
        SS_CLEAN_DATA:       None,
        SS_VALIDATION_RESULT: None,
        SS_TIME_SERIES:      None,
        SS_SELECTED_CATEGORY: None,
        SS_SARIMA_PARAMS:    None,
        SS_MODEL_RESULT:     None,
        SS_EVAL_METRICS:     None,
        SS_FORECAST_RESULT:  None,
        SS_WORKFLOW_STATUS:  {},
        SS_COL_MAPPING:      {},
        SS_DATA_FREQUENCY:   None,
        SS_FILE_NAME:        None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def route_page(current_page: str):
    """Router halaman berdasarkan current_page di session state."""
    if current_page == PAGE_HOME:
        from src.pages.home_page import render
    elif current_page == PAGE_UPLOAD:
        from src.pages.upload_page import render
    elif current_page == PAGE_VALIDATION:
        from src.pages.validation_page import render
    elif current_page == PAGE_PREPROCESSING:
        from src.pages.preprocessing_page import render
    elif current_page == PAGE_TRANSFORMATION:
        from src.pages.transformation_page import render
    elif current_page == PAGE_ANALYSIS:
        from src.pages.analysis_page import render
    elif current_page == PAGE_MODELING:
        from src.pages.modeling_page import render
    elif current_page == PAGE_EVALUATION:
        from src.pages.evaluation_page import render
    elif current_page == PAGE_FORECASTING:
        from src.pages.forecasting_page import render
    elif current_page == PAGE_COMPARISON:
        from src.pages.comparison_page import render
    elif current_page == PAGE_CONCLUSION:
        from src.pages.conclusion_page import render
    else:
        from src.pages.home_page import render

    render()


def main():
    init_session_state()
    inject_global_css()
    render_sidebar()

    current_page = st.session_state.get("current_page", PAGE_HOME)
    route_page(current_page)


if __name__ == "__main__":
    main()
