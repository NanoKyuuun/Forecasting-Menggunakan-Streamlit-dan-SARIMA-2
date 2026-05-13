# Dashboard Forecasting SARIMA

Dashboard forecasting berbasis Streamlit menggunakan metode SARIMA untuk prediksi data runtun waktu.

## Cara Menjalankan

```bash
cd sarima-project
pip install -r requirements.txt
streamlit run app.py
```

## Struktur Project

```
sarima-project/
├── app.py                    # Entry point
├── requirements.txt
├── data/raw/                 # Dataset sampel
├── outputs/forecasts/        # Hasil forecast
└── src/
    ├── core/                 # Logika inti (data, model, evaluasi)
    ├── ui/                   # Komponen tampilan
    ├── pages/                # Halaman dashboard
    └── utils/                # Helper & konstanta
```

## Modul Utama

| Halaman | Fungsi |
|---|---|
| Beranda | Penjelasan sistem |
| Upload Dataset | Unggah CSV/Excel |
| Validasi Data | Cek kualitas data |
| Preprocessing | Bersihkan data |
| Transformasi | Buat time series |
| Analisis | Visualisasi historis |
| Pemodelan SARIMA | Fitting model |
| Evaluasi Model | MAE, RMSE, MAPE |
| Forecasting | Prediksi & export |
| Perbandingan | Data tahunan vs bulanan |
| Kesimpulan | Ringkasan akhir |
