# Forecasting Menggunakan Streamlit dan SARIMA

Project ini adalah dashboard forecasting berbasis Streamlit menggunakan metode SARIMA untuk analisis data runtun waktu.

## Fitur Utama
- Upload dataset CSV/Excel.
- Validasi dan Preprocessing data.
- Transformasi Time Series.
- Pemodelan SARIMA (Manual & Auto-search).
- Evaluasi Model (MAE, MSE, RMSE, MAPE).
- Forecasting periode mendatang.
- Perbandingan dataset (Tahunan vs Bulanan).

## Struktur Project
- `data/`: Dataset historis.
- `referensi/`: Gambar referensi tampilan dashboard.
- `PRD_Aplikasi_Forecasting_Streamlit_SARIMA.md`: Dokumen kebutuhan produk.

## Cara Menjalankan
1. Install dependencies: `pip install -r requirements.txt`
2. Jalankan aplikasi: `streamlit run app.py`
