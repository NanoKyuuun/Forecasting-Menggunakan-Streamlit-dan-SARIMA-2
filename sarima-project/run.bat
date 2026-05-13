@echo off
title Menjalankan Dashboard SARIMA
echo ===================================================
echo MENJALANKAN DASHBOARD FORECASTING SARIMA
echo ===================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment tidak ditemukan!
    echo Silakan jalankan "setup.bat" terlebih dahulu untuk menginstal dependensi.
    pause
    exit /b
)

echo Mengaktifkan Virtual Environment...
call venv\Scripts\activate

echo.
echo Membuka aplikasi di browser... (Jangan tutup jendela ini selama aplikasi berjalan)
echo.
streamlit run app.py

pause
