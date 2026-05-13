# ============================================================
# Dockerfile — Dashboard Forecasting SARIMA
# ============================================================
# Base image: Python slim untuk ukuran image yang kecil
FROM python:3.11-slim

# Metadata
LABEL maintainer="Dashboard Forecasting SARIMA"
LABEL description="Streamlit app for SARIMA time series forecasting"

# ── Environment Variables ────────────────────────────────────
# Supaya Python tidak membuat file .pyc dan output langsung terlihat di log
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Port default Streamlit
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    # Nonaktifkan telemetry Streamlit
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    # Pastikan tema light mode dari environment
    STREAMLIT_THEME_BASE=light

# ── System Dependencies ──────────────────────────────────────
# statsmodels butuh compiler C (gcc) untuk beberapa komponen
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Working Directory ────────────────────────────────────────
WORKDIR /app

# ── Install Python Dependencies ──────────────────────────────
# Copy requirements dulu (agar Docker cache layer bisa dipakai ulang
# jika hanya source code yang berubah, bukan dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copy Source Code ─────────────────────────────────────────
COPY . .

# ── Streamlit Config ─────────────────────────────────────────
# Pastikan .streamlit/config.toml tersedia di container
# (sudah termasuk di COPY . . tapi pastikan directory ada)
RUN mkdir -p .streamlit

# ── Expose Port ──────────────────────────────────────────────
EXPOSE 8501

# ── Health Check ─────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Entry Point ──────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
