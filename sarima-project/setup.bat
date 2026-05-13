@echo off
title Setup Dashboard SARIMA
echo ===================================================
echo SETUP DASHBOARD FORECASTING SARIMA
echo ===================================================
echo.

echo [1/3] Memeriksa instalasi Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ditemukan! 
    echo Pastikan Python sudah terinstal dan opsi "Add Python to PATH" dicentang saat instalasi.
    pause
    exit /b
)

echo [2/3] Membuat Virtual Environment (venv)...
if not exist "venv\" (
    python -m venv venv
    echo Virtual Environment berhasil dibuat.
) else (
    echo Virtual Environment sudah ada. Melewati langkah ini.
)

echo.
echo [3/3] Menginstal Library yang dibutuhkan (requirements.txt)...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ===================================================
echo SETUP SELESAI DENGAN SUKSES!
echo ===================================================
echo Anda sekarang bisa langsung menjalankan program dengan mengklik dua kali file "run.bat"
echo.
pause
