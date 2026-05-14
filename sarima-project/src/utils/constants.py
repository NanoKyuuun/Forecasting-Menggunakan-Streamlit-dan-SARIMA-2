# ============================================================
# constants.py — Konstanta Global Dashboard Forecasting SARIMA
# ============================================================

# ── Identitas Aplikasi ──────────────────────────────────────
# Kumpulan teks statis untuk nama aplikasi, versi, dan hak cipta.
APP_TITLE = "Dashboard Forecasting SARIMA"
APP_SUBTITLE = "Forecasting Data Runtun Waktu Menggunakan Metode SARIMA"
APP_VERSION = "1.0"
APP_AUTHOR = "Tugas Akhir - Forecasting Menggunakan Streamlit dan SARIMA"

# ── Halaman (Page Keys) ─────────────────────────────────────
# Nama/label untuk setiap halaman (menu) yang ada di sidebar.
PAGE_HOME = "Beranda"
PAGE_UPLOAD = "Upload Dataset"
PAGE_VALIDATION = "Validasi Data"
PAGE_PREPROCESSING = "Preprocessing"
PAGE_TRANSFORMATION = "Transformasi Time Series"
PAGE_ANALYSIS = "Analisis Time Series"
PAGE_MODELING = "Pemodelan SARIMA"
PAGE_EVALUATION = "Evaluasi Model"
PAGE_FORECASTING = "Forecasting"
PAGE_COMPARISON = "Perbandingan Dataset"
PAGE_CONCLUSION = "Kesimpulan"

# Urutan halaman untuk menentukan alur navigasi (tombol "Lanjutkan")
PAGE_ORDER = [
    PAGE_HOME,
    PAGE_UPLOAD,
    PAGE_VALIDATION,
    PAGE_PREPROCESSING,
    PAGE_TRANSFORMATION,
    PAGE_ANALYSIS,
    PAGE_MODELING,
    PAGE_EVALUATION,
    PAGE_FORECASTING,
    PAGE_COMPARISON,
    PAGE_CONCLUSION,
]

# Pemetaan (mapping) icon emoji untuk setiap nama halaman di menu sidebar
PAGE_ICONS = {
    PAGE_HOME:           "🏠",
    PAGE_UPLOAD:         "📤",
    PAGE_VALIDATION:     "✅",
    PAGE_PREPROCESSING:  "🔧",
    PAGE_TRANSFORMATION: "🔄",
    PAGE_ANALYSIS:       "📊",
    PAGE_MODELING:       "🤖",
    PAGE_EVALUATION:     "📏",
    PAGE_FORECASTING:    "🔮",
    PAGE_COMPARISON:     "⚖️",
    PAGE_CONCLUSION:     "📋",
}

# ── Session State Keys ───────────────────────────────────────
# Definisi kunci (keys) untuk dictionary st.session_state agar mencegah 
# kesalahan ketik (typo) saat memanggil state di berbagai file.
SS_RAW_DATA          = "raw_data"
SS_CLEAN_DATA        = "clean_data"
SS_VALIDATION_RESULT = "validation_result"
SS_TIME_SERIES       = "time_series_data"
SS_SELECTED_CATEGORY = "selected_category"
SS_SARIMA_PARAMS     = "sarima_params"
SS_MODEL_RESULT      = "model_result"
SS_EVAL_METRICS      = "evaluation_metrics"
SS_FORECAST_RESULT   = "forecast_result"
SS_WORKFLOW_STATUS   = "workflow_status"
SS_COL_MAPPING       = "col_mapping"
SS_DATA_FREQUENCY    = "data_frequency"
SS_FILE_NAME         = "file_name"

# ── Observasi: Kategori Kelayakan (PRD §19.4) ───────────────
# Threshold (batas minimal) jumlah baris data agar model SARIMA bisa berjalan stabil
OBS_VERY_LIMITED = 10   # < 10 baris = error (terlalu sedikit)
OBS_LIMITED      = 30   # 10 - 30 baris = peringatan (terbatas)
OBS_ADEQUATE     = 60   # 31 - 60 baris = cukup, > 60 = baik

# ── SARIMA Auto-Search Batas (PRD §20.3) ────────────────────
# Batas pencarian grid (grid search) untuk parameter otomatis SARIMA.
# Diseting cukup rendah agar tidak terlalu lama waktu loading komputasinya.
AUTO_P_RANGE = range(0, 3)   # autoregressive order (0, 1, 2)
AUTO_D_RANGE = range(0, 2)   # differencing order (0, 1)
AUTO_Q_RANGE = range(0, 3)   # moving average order (0, 1, 2)
AUTO_P_SEASONAL = range(0, 2) # seasonal AR
AUTO_D_SEASONAL = range(0, 2) # seasonal diff
AUTO_Q_SEASONAL = range(0, 2) # seasonal MA

# ── Warna Tema ───────────────────────────────────────────────
# Variabel hex color untuk konsistensi di theme CSS
COLOR_PRIMARY    = "#0D3B66"   # Biru tua — sidebar, header
COLOR_SECONDARY  = "#0066CC"   # Biru muda — highlight, aksen
COLOR_SUCCESS    = "#2ECC71"   # Hijau
COLOR_WARNING    = "#F39C12"   # Oranye/kuning
COLOR_DANGER     = "#E74C3C"   # Merah
COLOR_BG         = "#F5F7FA"   # Background abu-abu muda
COLOR_CARD       = "#FAFAFA"   # Card putih
COLOR_TEXT_MAIN  = "#1A202C"   # Teks utama
COLOR_TEXT_MUTED = "#718096"   # Teks sekunder

# ── Grafik ───────────────────────────────────────────────────
# Variabel hex color khusus untuk garis-garis di grafik (charts.py)
CHART_ACTUAL_COLOR    = "#2196F3"
CHART_FITTED_COLOR    = "#FF9800"
CHART_FORECAST_COLOR  = "#4CAF50"
CHART_CI_COLOR        = "rgba(76, 175, 80, 0.15)"
CHART_RESIDUAL_COLOR  = "#9C27B0"

# ── Path Data Sample ─────────────────────────────────────────
# Path dinamis untuk membaca data sampel bawaan di folder `data/raw`
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

SAMPLE_TAHUNAN = os.path.join(DATA_RAW_DIR, "data_tahunan_per_prodi.csv")
SAMPLE_BULANAN_5 = os.path.join(DATA_RAW_DIR, "Data_Optimal_SARIMA_Bulanan_5Tahun.csv")
SAMPLE_BULANAN_10 = os.path.join(DATA_RAW_DIR, "Data_Optimal_SARIMA_Bulanan_10Tahun.csv")
