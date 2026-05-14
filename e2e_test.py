import os
from playwright.sync_api import sync_playwright
import time

def run_test():
    reports_dir = os.path.abspath("reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Path dataset
    data_path = os.path.abspath("data/Data_Optimal_SARIMA_Bulanan_10Tahun.csv")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            page.goto("http://localhost:8502", timeout=30000)
            page.wait_for_selector('button:has-text("Mulai")', timeout=15000)
            time.sleep(2)
            page.screenshot(path=os.path.join(reports_dir, "01_Home.png"))
            
            # Click Mulai
            print("2. Ke Halaman Upload...")
            page.get_by_text("Mulai — Upload Dataset").click()
            time.sleep(2)
            page.screenshot(path=os.path.join(reports_dir, "02_Upload_Before.png"))
            
            # Upload File
            print(f"3. Uploading file: {data_path}")
            page.locator('input[type="file"]').set_input_files(data_path)
            time.sleep(4)
            page.screenshot(path=os.path.join(reports_dir, "03_Upload_After.png"))
            
            # Ke Validasi
            print("4. Ke Validasi Data...")
            page.get_by_text("Lanjut ke Validasi").click()
            time.sleep(4)
            page.screenshot(path=os.path.join(reports_dir, "04_Validation.png"))
            
            # Ke Preprocessing
            print("5. Ke Preprocessing...")
            page.get_by_text("Lanjut ke Preprocessing").click()
            time.sleep(3)
            page.screenshot(path=os.path.join(reports_dir, "05_Preprocessing.png"))
            
            # Ke Transformasi
            print("6. Ke Transformasi...")
            page.get_by_text("Lanjut ke Transformasi").click()
            time.sleep(3)
            page.screenshot(path=os.path.join(reports_dir, "06_Transformation.png"))
            
            # Ke Analisis
            print("7. Ke Analisis...")
            page.get_by_text("Lanjut ke Analisis").click()
            time.sleep(4)
            page.screenshot(path=os.path.join(reports_dir, "07_Analysis.png"))
            
            # Ke Pemodelan
            print("8. Ke Pemodelan SARIMA...")
            page.get_by_text("Lanjut ke Pemodelan").click()
            time.sleep(2)
            
            # Jalankan Model Manual
            print("9. Menjalankan Model SARIMA...")
            time.sleep(2)
            page.locator('button:has-text("Jalankan Model SARIMA")').click()
            print("   (Menunggu model selesai fitting...)")
            time.sleep(20)
            page.screenshot(path=os.path.join(reports_dir, "08_Modeling.png"))
            
            # Ke Evaluasi
            print("10. Ke Evaluasi...")
            page.get_by_text("Lanjut ke Evaluasi").click()
            time.sleep(3)
            page.screenshot(path=os.path.join(reports_dir, "09_Evaluation.png"))
            
            # Ke Forecasting
            print("11. Ke Forecasting...")
            page.get_by_text("Lanjut ke Forecasting").click()
            time.sleep(2)
            
            # Generate Forecast
            print("12. Generate Forecast...")
            page.get_by_text("Generate Forecast").click()
            time.sleep(5)
            page.screenshot(path=os.path.join(reports_dir, "10_Forecasting.png"))
            
            # Ke Perbandingan Dataset
            print("13. Ke Perbandingan Dataset...")
            page.get_by_text("Lanjut ke Perbandingan").click()
            time.sleep(6)
            page.screenshot(path=os.path.join(reports_dir, "11_Comparison.png"))
            
            # Ke Kesimpulan
            print("14. Ke Kesimpulan...")
            page.get_by_text("Lanjut ke Kesimpulan").click()
            time.sleep(3)
            page.screenshot(path=os.path.join(reports_dir, "12_Conclusion.png"))
            
            print("Berhasil mengambil semua screenshot!")
            
        except Exception as e:
            err_msg = str(e).encode('ascii', 'ignore').decode('ascii')
            print(f"Terjadi error saat E2E testing: {err_msg}")
            page.screenshot(path=os.path.join(reports_dir, "error_state.png"))
            print("Screenshot error tersimpan di error_state.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()
