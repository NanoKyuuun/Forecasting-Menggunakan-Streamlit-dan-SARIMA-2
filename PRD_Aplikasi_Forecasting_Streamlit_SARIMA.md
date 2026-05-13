# Product Requirements Document (PRD)
# Aplikasi Forecasting Menggunakan Streamlit dan SARIMA

**Nama produk:** Dashboard Forecasting SARIMA  
**Platform:** Web dashboard berbasis Streamlit  
**Metode utama:** SARIMA  
**Target pengguna:** Mahasiswa, dosen pembimbing, penguji, dan pengguna akademik  
**Status dokumen:** Draft pengembangan  
**Versi:** 1.0  

---

## 1. Ringkasan Produk

Aplikasi ini merupakan dashboard forecasting berbasis Streamlit yang digunakan untuk melakukan prediksi data runtun waktu menggunakan model SARIMA. Aplikasi dirancang untuk membantu pengguna mengunggah dataset, melakukan validasi data, melihat pola historis, membangun model SARIMA, mengevaluasi performa model, dan menampilkan hasil prediksi dalam bentuk grafik, tabel, serta ringkasan interpretatif.

Aplikasi ini dikembangkan untuk kebutuhan Tugas Akhir dengan judul **Forecasting Menggunakan Streamlit dan SARIMA**. Fokus utama aplikasi bukan hanya menjalankan model, tetapi juga menampilkan alur analisis secara jelas agar mudah dipahami oleh dosen dan pengguna non-teknis.

Sistem akan mendukung dua skenario data. Pertama, data tahunan lima tahun sebagai contoh data historis yang belum optimal untuk pemodelan SARIMA. Kedua, data bulanan dengan jumlah observasi lebih banyak sebagai data pembanding yang lebih sesuai untuk pengujian pola musiman. Dengan dua skenario ini, pengguna dapat memahami bahwa kualitas dan struktur data sangat memengaruhi hasil forecasting.

---

## 2. Latar Belakang

Forecasting dibutuhkan untuk memperkirakan nilai masa depan berdasarkan pola data historis. Dalam konteks penelitian ini, forecasting digunakan untuk memprediksi perkembangan data berdasarkan periode waktu tertentu. SARIMA dipilih karena model ini mampu menangani data runtun waktu yang memiliki pola tren dan musiman.

Permasalahan utama pada project awal adalah data yang tersedia hanya mencakup lima tahun. Data seperti ini tetap dapat digunakan untuk demonstrasi sistem, tetapi belum ideal untuk menangkap pola musiman secara kuat. Oleh karena itu, aplikasi perlu menyediakan mekanisme pembanding antara data belum optimal dan data optimal. Tujuannya agar pengguna dapat melihat perbedaan hasil ketika model dijalankan pada data dengan struktur yang berbeda.

Selain aspek metodologis, tampilan dashboard juga perlu dibuat lebih modern, rapi, dan informatif. Tampilan yang baik akan membantu pengguna memahami proses analisis dari awal sampai akhir. Aplikasi tidak boleh hanya menampilkan hasil angka, tetapi juga harus menjelaskan arti dari hasil tersebut.

---

## 3. Tujuan Produk

Tujuan utama aplikasi ini adalah membangun dashboard forecasting SARIMA yang informatif, interaktif, dan mudah digunakan.

Secara rinci, aplikasi bertujuan untuk:

1. Memudahkan pengguna mengunggah dan memeriksa dataset runtun waktu.
2. Menampilkan validasi data sebelum proses pemodelan dilakukan.
3. Mengubah data mentah menjadi format time series yang siap dianalisis.
4. Menampilkan grafik tren historis agar pola data mudah dipahami.
5. Menjalankan pemodelan SARIMA berdasarkan parameter yang ditentukan.
6. Menampilkan evaluasi model menggunakan metrik kesalahan.
7. Menampilkan hasil forecasting dalam bentuk grafik dan tabel.
8. Memberikan catatan interpretasi agar hasil prediksi tidak dibaca secara keliru.
9. Menyediakan fitur unduh hasil forecast dalam format CSV.
10. Menyediakan perbandingan antara data belum optimal dan data optimal.

---

## 4. Sasaran Pengguna

### 4.1 Mahasiswa

Mahasiswa menggunakan aplikasi ini untuk menyelesaikan project Tugas Akhir, menjelaskan alur sistem, menampilkan hasil pemodelan, dan menunjukkan pemahaman terhadap metode SARIMA.

### 4.2 Dosen Pembimbing

Dosen pembimbing menggunakan aplikasi ini untuk menilai kelayakan metode, struktur sistem, tampilan dashboard, kejelasan alur analisis, serta ketepatan interpretasi hasil forecasting.

### 4.3 Dosen Penguji

Dosen penguji menggunakan aplikasi ini untuk mengevaluasi apakah sistem mampu menjalankan proses forecasting secara sistematis, apakah data divalidasi dengan baik, dan apakah hasil model dijelaskan secara hati-hati.

### 4.4 Pengguna Akademik

Pengguna akademik dapat memakai aplikasi ini sebagai alat bantu eksplorasi forecasting berbasis SARIMA, terutama untuk memahami pengaruh jumlah data terhadap kualitas hasil model.

---

## 5. Ruang Lingkup Produk

### 5.1 Dalam Ruang Lingkup

Fitur yang termasuk dalam ruang lingkup aplikasi:

1. Upload dataset CSV dan Excel.
2. Preview dataset.
3. Validasi kolom wajib.
4. Validasi missing value.
5. Validasi duplikasi data.
6. Validasi format tanggal atau periode.
7. Transformasi data menjadi time series.
8. Visualisasi tren historis.
9. Pemodelan SARIMA.
10. Evaluasi model.
11. Forecasting periode berikutnya.
12. Perbandingan data belum optimal dan data optimal.
13. Ringkasan kesimpulan otomatis.
14. Export hasil forecast ke CSV.
15. Tampilan dashboard modern berbasis card, chart, dan tabel.

### 5.2 Di Luar Ruang Lingkup

Fitur berikut tidak menjadi prioritas versi awal:

1. Sistem login pengguna.
2. Database server permanen.
3. Multi-user collaboration.
4. Integrasi API eksternal.
5. Deployment enterprise.
6. Export PDF dan DOCX otomatis.
7. Model pembanding selain SARIMA.
8. Aplikasi mobile.
9. Backend terpisah menggunakan framework API.
10. Frontend terpisah menggunakan React atau framework sejenis.

Fitur-fitur tersebut dapat dikembangkan pada versi lanjutan jika fitur utama sudah stabil.

---

## 6. Pernyataan Masalah

Project awal sudah dapat menjalankan forecasting, tetapi masih memiliki beberapa keterbatasan. Keterbatasan tersebut perlu diperbaiki agar aplikasi lebih layak ditampilkan sebagai project Tugas Akhir.

Masalah utama yang perlu diselesaikan:

1. Tampilan dashboard masih perlu dibuat lebih modern dan informatif.
2. Alur analisis perlu ditampilkan secara lebih jelas.
3. Data tahunan lima tahun belum optimal untuk menangkap pola musiman.
4. Sistem perlu membedakan data belum optimal dan data optimal secara eksplisit.
5. Validasi data perlu diperkuat agar pengguna mengetahui kualitas dataset.
6. Hasil model perlu disertai evaluasi dan interpretasi.
7. Halaman kesimpulan perlu dibuat lebih kuat sebagai output akhir sistem.
8. Struktur project perlu dirapikan agar mudah dijelaskan saat bimbingan.

---

## 7. Nilai Produk

Aplikasi ini memiliki nilai utama sebagai alat bantu akademik untuk memahami proses forecasting menggunakan SARIMA. Nilai produk tidak hanya terletak pada hasil prediksi, tetapi juga pada kemampuan sistem menjelaskan proses analisis.

Nilai yang diberikan aplikasi:

1. Membantu pengguna memahami proses pemodelan SARIMA dari awal sampai akhir.
2. Menunjukkan pentingnya struktur data dalam analisis time series.
3. Menyediakan dashboard visual yang lebih mudah dipahami dibanding output kode mentah.
4. Membantu mahasiswa menjelaskan project secara sistematis di depan dosen.
5. Menyediakan hasil forecast yang dapat diunduh dan digunakan dalam laporan.
6. Menampilkan catatan metodologis agar interpretasi hasil tetap hati-hati.

---

## 8. Prinsip Desain Produk

Aplikasi harus mengikuti prinsip berikut:

1. **Jelas**  
   Setiap halaman harus memiliki tujuan yang mudah dipahami.

2. **Sistematis**  
   Alur aplikasi harus mengikuti proses analisis time series, mulai dari upload data sampai kesimpulan.

3. **Konsisten**  
   Istilah, warna, ikon, dan format tampilan harus konsisten di seluruh halaman.

4. **Informatif**  
   Dashboard tidak hanya menampilkan angka, tetapi juga memberikan penjelasan singkat.

5. **Akademik**  
   Aplikasi harus menjaga kehati-hatian dalam menjelaskan hasil prediksi.

6. **Mudah diuji**  
   Setiap modul harus dapat diperiksa secara terpisah.

7. **Tidak berlebihan**  
   Fitur harus relevan dengan tujuan Tugas Akhir. Sistem tidak perlu terlalu kompleks.

---

## 9. Konsep Utama Aplikasi

Aplikasi akan dibuat dengan konsep dashboard modern. Pengguna dapat berpindah antar halaman melalui sidebar. Setiap halaman mewakili satu tahapan analisis.

Alur utama aplikasi:

1. Pengguna membuka halaman beranda.
2. Pengguna mengunggah dataset.
3. Sistem memvalidasi struktur dan isi data.
4. Sistem menampilkan data bersih.
5. Pengguna memilih jenis dataset atau skenario data.
6. Sistem mengubah data menjadi time series.
7. Sistem menampilkan tren historis.
8. Pengguna menjalankan model SARIMA.
9. Sistem menampilkan evaluasi model.
10. Sistem menghasilkan forecast.
11. Sistem menampilkan kesimpulan dan rekomendasi.
12. Pengguna dapat mengunduh hasil forecast.

---

## 10. Modul Aplikasi

### 10.1 Modul Beranda

Modul ini menjadi halaman pembuka aplikasi. Halaman ini menjelaskan identitas project, tujuan aplikasi, metode yang digunakan, dan ringkasan alur kerja.

Konten yang ditampilkan:

1. Judul aplikasi.
2. Deskripsi singkat project.
3. Ringkasan metode SARIMA.
4. Alur kerja aplikasi.
5. Kartu informasi utama.
6. Tombol menuju upload dataset.

Komponen visual:

1. Hero section.
2. Card ringkasan.
3. Ikon tahapan analisis.
4. Progress flow sederhana.

### 10.2 Modul Upload Dataset

Modul ini digunakan untuk mengunggah dataset yang akan dianalisis.

Konten yang ditampilkan:

1. Upload file CSV atau Excel.
2. Preview data awal.
3. Informasi nama file.
4. Jumlah baris dan kolom.
5. Status file berhasil dibaca.
6. Pesan error jika file tidak valid.

Kebutuhan validasi:

1. File tidak boleh kosong.
2. Format file harus CSV atau Excel.
3. File harus memiliki kolom periode.
4. File harus memiliki kolom nilai yang akan diprediksi.
5. File harus memiliki kolom kategori jika data berisi beberapa program studi atau kelompok.

### 10.3 Modul Validasi Data

Modul ini memeriksa kelayakan data sebelum diproses lebih lanjut.

Validasi yang dilakukan:

1. Cek kolom wajib.
2. Cek nilai kosong.
3. Cek duplikasi data.
4. Cek format periode.
5. Cek tipe data numerik.
6. Cek jumlah observasi.
7. Cek rentang periode.
8. Cek konsistensi kategori.

Output validasi:

1. Status validasi berhasil atau gagal.
2. Daftar masalah yang ditemukan.
3. Rekomendasi perbaikan data.
4. Data yang siap diproses.

### 10.4 Modul Preprocessing

Modul ini membersihkan data agar siap dianalisis.

Proses yang dilakukan:

1. Menghapus baris kosong.
2. Mengubah nama kolom ke format standar.
3. Mengubah tipe data periode.
4. Mengubah nilai target menjadi numerik.
5. Menangani missing value.
6. Menghapus duplikasi jika diperlukan.
7. Mengurutkan data berdasarkan periode.

Output preprocessing:

1. Dataset bersih.
2. Ringkasan jumlah data sebelum dan sesudah preprocessing.
3. Tabel data siap transformasi.

### 10.5 Modul Transformasi Time Series

Modul ini mengubah data bersih menjadi format time series.

Proses yang dilakukan:

1. Memilih kategori atau program studi.
2. Mengelompokkan data berdasarkan periode.
3. Membentuk indeks waktu.
4. Menentukan frekuensi data.
5. Menampilkan tabel time series.
6. Menampilkan grafik tren awal.

Jenis frekuensi data:

1. Tahunan.
2. Bulanan.
3. Kuartalan jika tersedia.

Catatan sistem:

Jika data hanya memiliki lima observasi tahunan, sistem tetap dapat menjalankan SARIMA sesuai fokus project, tetapi harus menampilkan catatan bahwa hasil prediksi merupakan estimasi awal berbasis data terbatas.

### 10.6 Modul Analisis Time Series

Modul ini digunakan untuk memahami pola awal pada data.

Konten yang ditampilkan:

1. Grafik tren historis.
2. Statistik deskriptif.
3. Nilai minimum.
4. Nilai maksimum.
5. Rata-rata.
6. Perubahan antar periode.
7. Indikasi pola tren.
8. Indikasi pola musiman jika data mendukung.

Visualisasi yang digunakan:

1. Line chart.
2. Area chart opsional.
3. Bar chart perubahan per periode.
4. Tabel ringkasan statistik.

### 10.7 Modul Pemodelan SARIMA

Modul ini menjadi inti aplikasi. Modul ini menjalankan model SARIMA berdasarkan data yang telah diproses.

Fitur utama:

1. Pemilihan kategori atau program studi.
2. Pemilihan parameter SARIMA.
3. Opsi auto-search parameter terbatas.
4. Proses fitting model.
5. Penampilan parameter model.
6. Penampilan model terbaik.
7. Penampilan actual vs fitted.
8. Status keberhasilan pemodelan.

Parameter yang digunakan:

1. p: komponen autoregressive.
2. d: differencing.
3. q: moving average.
4. P: seasonal autoregressive.
5. D: seasonal differencing.
6. Q: seasonal moving average.
7. s: panjang periode musiman.

Catatan tampilan:

Seluruh tampilan aplikasi harus menggunakan istilah SARIMA. Istilah lain yang dapat membingungkan pengguna tidak perlu ditampilkan di dashboard.

### 10.8 Modul Evaluasi Model

Modul ini digunakan untuk menilai performa model SARIMA terhadap data historis.

Metrik evaluasi:

1. MAE.
2. MSE.
3. RMSE.
4. MAPE.

Visualisasi evaluasi:

1. Grafik actual vs fitted.
2. Grafik residual.
3. Distribusi residual jika diperlukan.
4. Tabel metrik evaluasi.

Interpretasi evaluasi:

Sistem harus menampilkan penjelasan singkat tentang arti metrik. Contohnya, RMSE digunakan untuk melihat rata-rata kesalahan model dalam satuan data target. MAPE digunakan untuk melihat persentase kesalahan model.

### 10.9 Modul Forecasting

Modul ini menghasilkan prediksi untuk periode berikutnya.

Fitur utama:

1. Pemilihan jumlah periode forecast.
2. Penampilan hasil prediksi.
3. Penampilan grafik aktual dan forecast.
4. Penampilan confidence interval jika tersedia.
5. Penampilan tabel forecast.
6. Download hasil forecast dalam CSV.

Output utama:

1. Periode prediksi.
2. Nilai prediksi.
3. Batas bawah prediksi.
4. Batas atas prediksi.
5. Kategori atau program studi.

### 10.10 Modul Perbandingan Dataset

Modul ini digunakan untuk membandingkan dua jenis data.

Jenis data:

1. Data tahunan lima tahun.
2. Data bulanan optimal.

Tujuan modul:

1. Menunjukkan perbedaan jumlah observasi.
2. Menunjukkan perbedaan pola data.
3. Menunjukkan perbedaan hasil evaluasi model.
4. Menunjukkan perbedaan stabilitas forecasting.
5. Menjelaskan bahwa struktur data memengaruhi kualitas hasil model.

Output perbandingan:

1. Tabel perbandingan jumlah observasi.
2. Grafik tren masing-masing data.
3. Perbandingan nilai evaluasi.
4. Ringkasan interpretasi.

Catatan akademik:

Data bulanan optimal yang dibuat untuk pengujian harus disebut sebagai data simulasi atau data pembanding. Data tersebut tidak boleh diklaim sebagai data empiris resmi jika tidak berasal dari instansi terkait.

### 10.11 Modul Kesimpulan

Modul ini menjadi halaman akhir aplikasi. Halaman ini harus menampilkan ringkasan hasil model dan rekomendasi.

Konten yang ditampilkan:

1. Dataset yang digunakan.
2. Jumlah observasi.
3. Model SARIMA yang digunakan.
4. Nilai evaluasi model.
5. Hasil forecast utama.
6. Interpretasi tren.
7. Catatan keterbatasan.
8. Rekomendasi penggunaan hasil.
9. Tombol download forecast.

Format kesimpulan:

Kesimpulan harus ditulis dalam bahasa yang mudah dipahami. Sistem tidak boleh membuat klaim berlebihan. Jika data terbatas, sistem harus menampilkan catatan bahwa hasil forecast bersifat estimasi awal.

---

## 11. Kebutuhan Fungsional

### FR-01 Upload Dataset

Sistem harus memungkinkan pengguna mengunggah file CSV atau Excel.

Kriteria penerimaan:

1. Pengguna dapat memilih file dari perangkat.
2. Sistem dapat membaca file CSV.
3. Sistem dapat membaca file Excel.
4. Sistem menampilkan preview data.
5. Sistem menampilkan pesan error jika file tidak valid.

### FR-02 Validasi Struktur Data

Sistem harus memeriksa struktur dataset.

Kriteria penerimaan:

1. Sistem memeriksa keberadaan kolom periode.
2. Sistem memeriksa keberadaan kolom target.
3. Sistem memeriksa keberadaan kolom kategori jika diperlukan.
4. Sistem menampilkan daftar kolom yang ditemukan.
5. Sistem menampilkan status validasi.

### FR-03 Validasi Isi Data

Sistem harus memeriksa isi dataset.

Kriteria penerimaan:

1. Sistem mendeteksi missing value.
2. Sistem mendeteksi duplikasi.
3. Sistem mendeteksi nilai target non-numerik.
4. Sistem mendeteksi format periode yang tidak valid.
5. Sistem menampilkan rekomendasi perbaikan.

### FR-04 Preprocessing Data

Sistem harus membersihkan data sebelum pemodelan.

Kriteria penerimaan:

1. Sistem menghapus baris kosong.
2. Sistem mengubah tipe data sesuai kebutuhan.
3. Sistem mengurutkan data berdasarkan periode.
4. Sistem menghasilkan data bersih.
5. Sistem menampilkan ringkasan hasil preprocessing.

### FR-05 Transformasi Time Series

Sistem harus mengubah data menjadi format time series.

Kriteria penerimaan:

1. Pengguna dapat memilih kategori.
2. Sistem mengelompokkan data berdasarkan periode.
3. Sistem membentuk indeks waktu.
4. Sistem menampilkan grafik tren historis.
5. Sistem menyimpan time series ke session state.

### FR-06 Pemodelan SARIMA

Sistem harus menjalankan model SARIMA.

Kriteria penerimaan:

1. Pengguna dapat menentukan parameter SARIMA.
2. Sistem dapat menjalankan fitting model.
3. Sistem menampilkan parameter model.
4. Sistem menampilkan grafik actual vs fitted.
5. Sistem menampilkan status model berhasil atau gagal.

### FR-07 Evaluasi Model

Sistem harus menghitung metrik evaluasi.

Kriteria penerimaan:

1. Sistem menghitung MAE.
2. Sistem menghitung MSE.
3. Sistem menghitung RMSE.
4. Sistem menghitung MAPE.
5. Sistem menampilkan interpretasi singkat dari hasil evaluasi.

### FR-08 Forecasting

Sistem harus menghasilkan forecast untuk periode mendatang.

Kriteria penerimaan:

1. Pengguna dapat memilih jumlah periode forecast.
2. Sistem menghasilkan nilai prediksi.
3. Sistem menampilkan grafik forecast.
4. Sistem menampilkan tabel forecast.
5. Sistem dapat mengunduh hasil forecast dalam CSV.

### FR-09 Perbandingan Dataset

Sistem harus dapat membandingkan data belum optimal dan data optimal.

Kriteria penerimaan:

1. Sistem menampilkan jumlah observasi tiap dataset.
2. Sistem menampilkan grafik perbandingan.
3. Sistem menampilkan hasil evaluasi tiap dataset.
4. Sistem menampilkan interpretasi perbandingan.
5. Sistem memberi catatan bahwa data simulasi hanya digunakan untuk pengujian.

### FR-10 Kesimpulan Otomatis

Sistem harus menampilkan ringkasan hasil akhir.

Kriteria penerimaan:

1. Sistem menampilkan nama dataset.
2. Sistem menampilkan jumlah observasi.
3. Sistem menampilkan parameter SARIMA.
4. Sistem menampilkan metrik evaluasi.
5. Sistem menampilkan hasil forecast utama.
6. Sistem menampilkan catatan keterbatasan.

---

## 12. Kebutuhan Non-Fungsional

### 12.1 Kinerja

Aplikasi harus dapat berjalan lancar pada laptop standar mahasiswa. Proses pemodelan harus dibatasi agar tidak terlalu berat.

Target kinerja:

1. Aplikasi dapat terbuka dalam waktu wajar.
2. Upload dataset kecil sampai sedang dapat diproses tanpa error.
3. Pemodelan SARIMA tidak boleh membuat aplikasi berhenti terlalu lama.
4. Proses auto-search parameter harus dibatasi.

### 12.2 Kemudahan Penggunaan

Aplikasi harus mudah digunakan oleh pengguna non-teknis.

Kriteria:

1. Navigasi jelas.
2. Setiap halaman memiliki judul dan deskripsi.
3. Pesan error mudah dipahami.
4. Hasil analisis diberi interpretasi singkat.
5. Tombol aksi terlihat jelas.

### 12.3 Keandalan

Aplikasi harus tetap stabil ketika pengguna mengunggah data yang kurang baik.

Kriteria:

1. Sistem tidak crash saat data tidak valid.
2. Sistem menampilkan pesan error yang jelas.
3. Sistem memberi rekomendasi perbaikan data.
4. Sistem menyimpan status proses di session state.

### 12.4 Konsistensi Tampilan

Aplikasi harus menggunakan gaya visual yang konsisten.

Kriteria:

1. Warna utama konsisten.
2. Card memiliki format seragam.
3. Tabel memiliki tampilan rapi.
4. Grafik memakai label yang jelas.
5. Sidebar memiliki urutan halaman yang logis.

### 12.5 Maintainability

Kode aplikasi harus mudah dirawat dan dijelaskan.

Kriteria:

1. Fungsi analisis dipisah dari tampilan.
2. File tidak terlalu panjang.
3. Nama fungsi jelas.
4. Struktur folder mudah dipahami.
5. Komentar digunakan pada bagian penting.

---

## 13. Kebutuhan Data

### 13.1 Format Dataset Minimal

Dataset minimal harus memiliki kolom berikut:

| Kolom | Deskripsi | Contoh |
|---|---|---|
| periode | Tahun atau bulan data | 2021 atau 2021-01 |
| kategori | Nama program studi atau kelompok data | Teknik Informatika |
| nilai | Nilai yang akan diprediksi | 120 |

Nama kolom dapat disesuaikan, tetapi sistem perlu menyediakan mapping kolom agar pengguna dapat memilih kolom yang sesuai.

### 13.2 Data Tahunan Lima Tahun

Data ini digunakan sebagai contoh data belum optimal.

Karakteristik:

1. Periode 2021 sampai 2025.
2. Jumlah observasi kecil.
3. Tidak cukup kuat untuk membaca pola musiman.
4. Tetap dapat digunakan untuk demonstrasi sistem.
5. Hasil prediksi perlu dibaca secara hati-hati.

### 13.3 Data Bulanan Optimal

Data ini digunakan sebagai pembanding yang lebih sesuai untuk SARIMA.

Karakteristik:

1. Memiliki data bulanan.
2. Minimal 60 observasi untuk lima tahun.
3. Lebih baik jika tersedia 120 observasi untuk sepuluh tahun.
4. Dapat memperlihatkan pola musiman.
5. Lebih stabil untuk pengujian model.

### 13.4 Status Data Simulasi

Jika data optimal dibuat secara sintetis, sistem dan laporan harus menyebutnya sebagai data simulasi. Data simulasi digunakan untuk menguji kemampuan aplikasi, bukan untuk menggantikan data empiris resmi.

Kalimat yang dapat digunakan:

> Data bulanan digunakan sebagai data simulasi pembanding untuk menguji performa dashboard pada struktur data yang lebih sesuai dengan pemodelan SARIMA.

---

## 14. Desain Tampilan Dashboard

### 14.1 Gaya Visual

Dashboard menggunakan gaya modern, bersih, dan profesional. Tampilan mengacu pada dashboard analitik dengan sidebar, kartu informasi, grafik utama, dan tabel ringkasan.

Karakter tampilan:

1. Latar belakang abu-abu muda atau putih kebiruan.
2. Sidebar gelap atau biru tua.
3. Card putih dengan sudut membulat.
4. Grafik besar dengan label jelas.
5. Tabel rapi dengan header tegas.
6. Ikon sederhana untuk membantu navigasi.
7. Tombol aksi dengan warna kontras.

### 14.2 Warna Utama

Rekomendasi warna:

1. Biru tua untuk sidebar dan header utama.
2. Biru muda untuk highlight.
3. Putih untuk card.
4. Abu-abu muda untuk background.
5. Hijau untuk status berhasil.
6. Kuning atau oranye untuk peringatan.
7. Merah untuk error.

### 14.3 Layout Umum

Setiap halaman menggunakan struktur berikut:

1. Header halaman.
2. Deskripsi singkat halaman.
3. Card ringkasan di bagian atas.
4. Konten utama di tengah.
5. Grafik atau tabel pendukung.
6. Catatan interpretasi di bagian bawah.
7. Tombol aksi jika diperlukan.

### 14.4 Sidebar

Sidebar harus memuat menu berikut:

1. Beranda.
2. Upload Dataset.
3. Validasi Data.
4. Preprocessing.
5. Transformasi Time Series.
6. Analisis Time Series.
7. Pemodelan SARIMA.
8. Evaluasi Model.
9. Forecasting.
10. Perbandingan Dataset.
11. Kesimpulan.

Sidebar harus menampilkan status tahapan. Contohnya, halaman yang sudah selesai dapat diberi tanda centang.

### 14.5 Card Ringkasan

Card ringkasan digunakan untuk menampilkan informasi penting secara cepat.

Contoh card:

1. Total observasi.
2. Jumlah kategori.
3. Rentang periode.
4. Frekuensi data.
5. Model SARIMA.
6. Nilai MAPE.
7. Nilai RMSE.
8. Jumlah periode forecast.

### 14.6 Grafik

Grafik yang dibutuhkan:

1. Grafik tren historis.
2. Grafik actual vs fitted.
3. Grafik actual vs forecast.
4. Grafik residual.
5. Grafik perbandingan dataset.

Grafik harus memiliki:

1. Judul yang jelas.
2. Label sumbu X.
3. Label sumbu Y.
4. Legenda.
5. Tooltip jika menggunakan Plotly.

### 14.7 Tabel

Tabel yang dibutuhkan:

1. Preview dataset.
2. Data bersih.
3. Data time series.
4. Parameter model.
5. Metrik evaluasi.
6. Hasil forecast.
7. Perbandingan dataset.

Tabel harus mudah dibaca dan tidak terlalu penuh.

---

## 15. Alur Pengguna

### 15.1 Alur Utama

1. Pengguna membuka aplikasi.
2. Pengguna membaca ringkasan pada halaman beranda.
3. Pengguna masuk ke halaman upload dataset.
4. Pengguna mengunggah file.
5. Sistem membaca dan menampilkan preview data.
6. Pengguna masuk ke halaman validasi data.
7. Sistem menampilkan status validasi.
8. Pengguna masuk ke halaman preprocessing.
9. Sistem membersihkan data.
10. Pengguna memilih kategori data.
11. Sistem menampilkan time series.
12. Pengguna menjalankan model SARIMA.
13. Sistem menampilkan evaluasi model.
14. Pengguna menentukan horizon forecast.
15. Sistem menampilkan hasil prediksi.
16. Pengguna melihat halaman kesimpulan.
17. Pengguna mengunduh hasil forecast.

### 15.2 Alur Error

Jika file tidak valid:

1. Sistem menolak file.
2. Sistem menampilkan alasan penolakan.
3. Sistem memberi contoh format data yang benar.
4. Pengguna dapat mengunggah ulang file.

Jika data terlalu sedikit:

1. Sistem tetap menampilkan warning.
2. Sistem memberi catatan keterbatasan.
3. Sistem dapat tetap menjalankan model jika pengguna melanjutkan.
4. Sistem menampilkan hasil dengan interpretasi hati-hati.

Jika model gagal:

1. Sistem menampilkan pesan error.
2. Sistem menyarankan parameter yang lebih sederhana.
3. Sistem meminta pengguna mencoba parameter lain.
4. Sistem tidak menghentikan seluruh aplikasi.

---

## 16. Arsitektur Sistem

Aplikasi menggunakan arsitektur modular berbasis Streamlit. Streamlit tetap menjadi antarmuka utama sekaligus server aplikasi. Logika pemrosesan data dan model dipisahkan dalam file Python agar kode lebih rapi.

Arsitektur konseptual:

```text
Pengguna
  ↓
Streamlit UI
  ↓
Validasi Data
  ↓
Preprocessing
  ↓
Transformasi Time Series
  ↓
Model SARIMA
  ↓
Evaluasi Model
  ↓
Forecasting
  ↓
Visualisasi dan Export
```

Aplikasi tidak menggunakan backend terpisah pada versi awal. Hal ini dipilih agar sistem tetap sederhana, mudah dijelaskan, dan sesuai untuk kebutuhan Tugas Akhir.

---

## 17. Struktur Project

Struktur project yang direkomendasikan:

```text
forecasting-sarima-streamlit/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── outputs/
│   ├── forecasts/
│   └── reports/
│
├── src/
│   ├── core/
│   │   ├── data_loader.py
│   │   ├── validation.py
│   │   ├── preprocessing.py
│   │   ├── transformation.py
│   │   ├── sarima_model.py
│   │   ├── evaluation.py
│   │   └── forecasting.py
│   │
│   ├── ui/
│   │   ├── theme.py
│   │   ├── sidebar.py
│   │   ├── cards.py
│   │   ├── charts.py
│   │   ├── tables.py
│   │   └── messages.py
│   │
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── upload_page.py
│   │   ├── validation_page.py
│   │   ├── preprocessing_page.py
│   │   ├── transformation_page.py
│   │   ├── analysis_page.py
│   │   ├── modeling_page.py
│   │   ├── evaluation_page.py
│   │   ├── forecasting_page.py
│   │   ├── comparison_page.py
│   │   └── conclusion_page.py
│   │
│   └── utils/
│       ├── export.py
│       ├── helpers.py
│       └── constants.py
```

### 17.1 Penjelasan Folder

#### app.py

File utama untuk menjalankan aplikasi Streamlit. File ini memanggil konfigurasi tema, sidebar, dan halaman yang dipilih pengguna.

#### src/core

Folder untuk logika utama aplikasi. Folder ini berisi proses membaca data, validasi, preprocessing, transformasi, pemodelan SARIMA, evaluasi, dan forecasting.

#### src/ui

Folder untuk komponen tampilan. Folder ini berisi card, grafik, tabel, pesan, tema, dan sidebar.

#### src/pages

Folder untuk halaman dashboard. Setiap halaman dibuat dalam satu file agar mudah dijelaskan.

#### src/utils

Folder untuk fungsi pendukung, seperti export CSV, format angka, dan konstanta.

#### data

Folder untuk menyimpan data contoh, data mentah, dan data hasil proses.

#### outputs

Folder untuk menyimpan hasil forecast atau laporan yang dihasilkan aplikasi.

---

## 18. Desain Session State

Aplikasi perlu menggunakan session state agar data tidak hilang saat pengguna berpindah halaman.

Data yang disimpan di session state:

1. Dataset asli.
2. Dataset bersih.
3. Hasil validasi.
4. Data time series.
5. Kategori yang dipilih.
6. Parameter SARIMA.
7. Hasil model.
8. Metrik evaluasi.
9. Hasil forecast.
10. Status tahapan aplikasi.

Contoh key session state:

```text
raw_data
clean_data
validation_result
time_series_data
selected_category
sarima_params
model_result
evaluation_metrics
forecast_result
workflow_status
```

---

## 19. Aturan Validasi Data

### 19.1 Validasi Kolom

Sistem harus memastikan dataset memiliki kolom yang dibutuhkan.

Kolom wajib:

1. Kolom periode.
2. Kolom target.
3. Kolom kategori jika data berisi lebih dari satu kelompok.

Jika nama kolom berbeda, pengguna dapat memilih mapping kolom.

### 19.2 Validasi Periode

Sistem harus memastikan periode dapat dibaca sebagai waktu.

Format yang diterima:

1. Tahun, contoh 2021.
2. Bulan, contoh 2021-01.
3. Tanggal lengkap, contoh 2021-01-01.

### 19.3 Validasi Nilai Target

Sistem harus memastikan nilai target berupa angka.

Aturan:

1. Nilai tidak boleh kosong.
2. Nilai tidak boleh berupa teks.
3. Nilai negatif hanya diperbolehkan jika sesuai konteks data.
4. Nilai ekstrem harus ditandai sebagai outlier potensial.

### 19.4 Validasi Jumlah Observasi

Sistem harus menghitung jumlah observasi.

Kategori kelayakan:

| Jumlah Observasi | Status | Keterangan |
|---|---|---|
| Kurang dari 10 | Sangat terbatas | Hasil forecast harus dibaca sangat hati-hati |
| 10 sampai 30 | Terbatas | Model dapat diuji, tetapi interpretasi tetap hati-hati |
| 31 sampai 60 | Cukup | Lebih layak untuk pengujian awal |
| Lebih dari 60 | Baik | Lebih sesuai untuk analisis musiman |

### 19.5 Validasi Frekuensi Data

Sistem harus mendeteksi apakah data tahunan, bulanan, atau kuartalan.

Aturan:

1. Data tahunan memiliki satu observasi per tahun.
2. Data bulanan memiliki satu observasi per bulan.
3. Data kuartalan memiliki satu observasi per kuartal.
4. Jika periode tidak konsisten, sistem memberi warning.

---

## 20. Kebutuhan Model SARIMA

### 20.1 Input Model

Input model berupa data time series dengan indeks waktu dan nilai target numerik.

Input minimal:

1. Periode.
2. Nilai target.
3. Frekuensi data.
4. Parameter SARIMA.

### 20.2 Parameter SARIMA

Parameter yang harus didukung:

| Parameter | Fungsi |
|---|---|
| p | Mengatur komponen autoregressive |
| d | Mengatur differencing non-musiman |
| q | Mengatur komponen moving average |
| P | Mengatur komponen autoregressive musiman |
| D | Mengatur differencing musiman |
| Q | Mengatur komponen moving average musiman |
| s | Mengatur panjang periode musiman |

### 20.3 Mode Parameter

Aplikasi mendukung dua mode parameter:

1. Manual.
2. Auto-search terbatas.

#### Mode Manual

Pengguna menentukan parameter sendiri melalui input number atau dropdown.

#### Mode Auto-search Terbatas

Sistem mencoba beberapa kombinasi parameter dengan batas kecil agar proses tidak terlalu lama.

Contoh batas:

1. p: 0 sampai 2.
2. d: 0 sampai 1.
3. q: 0 sampai 2.
4. P: 0 sampai 1.
5. D: 0 sampai 1.
6. Q: 0 sampai 1.
7. s: mengikuti frekuensi data.

### 20.4 Output Model

Output model:

1. Parameter SARIMA.
2. Nilai AIC jika tersedia.
3. Nilai BIC jika tersedia.
4. Fitted value.
5. Residual.
6. Forecast.
7. Confidence interval jika tersedia.

### 20.5 Aturan Interpretasi Model

Sistem harus menampilkan interpretasi yang hati-hati.

Jika data terbatas:

> Data historis yang tersedia masih terbatas. Model SARIMA tetap digunakan sesuai fokus analisis, tetapi hasil prediksi perlu ditafsirkan sebagai estimasi awal.

Jika data bulanan cukup panjang:

> Data memiliki jumlah observasi yang lebih memadai untuk membaca pola runtun waktu dan pola musiman.

---

## 21. Export dan Output

### 21.1 Export CSV

Export CSV menjadi fitur wajib versi awal.

Isi file CSV:

1. Kategori.
2. Periode forecast.
3. Nilai prediksi.
4. Batas bawah prediksi.
5. Batas atas prediksi.
6. Parameter SARIMA.
7. Tanggal export.

### 21.2 Export Markdown

Export Markdown menjadi fitur tambahan.

Isi laporan Markdown:

1. Ringkasan dataset.
2. Ringkasan validasi.
3. Parameter SARIMA.
4. Metrik evaluasi.
5. Tabel forecast.
6. Kesimpulan.
7. Catatan keterbatasan.

### 21.3 Export PDF atau DOCX

Export PDF atau DOCX tidak menjadi prioritas awal. Fitur ini dapat dikembangkan jika fitur utama sudah stabil.

---

## 22. Halaman Kesimpulan yang Diharapkan

Halaman kesimpulan harus menjadi output utama yang mudah dibaca dosen.

Format halaman:

1. Judul kesimpulan.
2. Ringkasan dataset.
3. Ringkasan model SARIMA.
4. Ringkasan evaluasi.
5. Ringkasan forecast.
6. Interpretasi hasil.
7. Catatan keterbatasan.
8. Rekomendasi penggunaan.

Contoh narasi kesimpulan:

> Berdasarkan data historis yang digunakan, model SARIMA menghasilkan prediksi untuk periode mendatang dengan nilai evaluasi tertentu. Hasil ini menunjukkan arah perubahan data berdasarkan pola historis yang tersedia. Karena jumlah observasi pada dataset tahunan masih terbatas, hasil forecast perlu dipahami sebagai estimasi awal. Penggunaan data bulanan dengan jumlah observasi lebih banyak dapat memberikan dasar pemodelan yang lebih kuat.

---

## 23. Roadmap Pengembangan

### Tahap 1: Rebuild Tampilan Utama

Target:

1. Membuat layout dashboard baru.
2. Membuat sidebar modern.
3. Membuat card ringkasan.
4. Membuat tema warna konsisten.

Output:

1. Beranda baru.
2. Sidebar baru.
3. Komponen card dasar.

### Tahap 2: Rebuild Pipeline Data

Target:

1. Membuat upload dataset.
2. Membuat validasi data.
3. Membuat preprocessing.
4. Membuat transformasi time series.

Output:

1. Data dapat diunggah.
2. Data dapat divalidasi.
3. Data dapat dibersihkan.
4. Data dapat diubah menjadi time series.

### Tahap 3: Implementasi Model SARIMA

Target:

1. Membuat modul SARIMA.
2. Membuat parameter manual.
3. Membuat auto-search terbatas.
4. Menampilkan hasil model.

Output:

1. Model SARIMA dapat dijalankan.
2. Parameter tampil jelas.
3. Actual vs fitted tampil.

### Tahap 4: Evaluasi dan Forecasting

Target:

1. Menghitung metrik evaluasi.
2. Menampilkan residual.
3. Menghasilkan forecast.
4. Menampilkan tabel forecast.

Output:

1. MAE, MSE, RMSE, dan MAPE tampil.
2. Grafik forecast tampil.
3. Tabel forecast tampil.

### Tahap 5: Perbandingan Dataset

Target:

1. Menambahkan data tahunan lima tahun.
2. Menambahkan data bulanan optimal.
3. Menampilkan perbandingan hasil.
4. Menampilkan catatan interpretasi.

Output:

1. Perbandingan data tersedia.
2. Perbandingan evaluasi tersedia.
3. Perbandingan forecast tersedia.

### Tahap 6: Kesimpulan dan Export

Target:

1. Membuat halaman kesimpulan.
2. Membuat export CSV.
3. Membuat ringkasan otomatis.
4. Menyempurnakan pesan metodologis.

Output:

1. Halaman kesimpulan siap presentasi.
2. Hasil forecast dapat diunduh.
3. Sistem siap ditunjukkan saat bimbingan.

---

## 24. Prioritas Pengembangan

| Prioritas | Fitur | Status |
|---|---|---|
| P0 | Layout utama dan sidebar | Wajib |
| P0 | Upload dan validasi dataset | Wajib |
| P0 | Preprocessing dan transformasi time series | Wajib |
| P0 | Pemodelan SARIMA | Wajib |
| P0 | Evaluasi model | Wajib |
| P0 | Forecasting | Wajib |
| P0 | Halaman kesimpulan | Wajib |
| P1 | Perbandingan dataset | Penting |
| P1 | Export CSV | Penting |
| P1 | Catatan keterbatasan otomatis | Penting |
| P2 | Export Markdown | Tambahan |
| P2 | Export PDF atau DOCX | Tambahan |
| P2 | Unit test lengkap | Tambahan |

---

## 25. Risiko dan Mitigasi

### Risiko 1: Data Terlalu Pendek

Dampak:

Hasil forecasting dapat kurang stabil.

Mitigasi:

1. Tampilkan warning.
2. Sediakan data bulanan pembanding.
3. Batasi klaim hasil.
4. Jelaskan bahwa hasil adalah estimasi awal.

### Risiko 2: Model Gagal Fitting

Dampak:

Pengguna tidak mendapatkan hasil model.

Mitigasi:

1. Gunakan parameter sederhana sebagai default.
2. Batasi rentang auto-search.
3. Tampilkan pesan error yang jelas.
4. Berikan rekomendasi parameter alternatif.

### Risiko 3: Dashboard Terlalu Kompleks

Dampak:

Pengguna sulit memahami aplikasi.

Mitigasi:

1. Gunakan alur halaman bertahap.
2. Gunakan card ringkasan.
3. Batasi fitur yang tidak penting.
4. Fokus pada output utama.

### Risiko 4: Tampilan Tidak Konsisten

Dampak:

Dashboard terlihat kurang profesional.

Mitigasi:

1. Buat file tema khusus.
2. Gunakan komponen UI yang seragam.
3. Gunakan warna yang konsisten.
4. Hindari terlalu banyak variasi layout.

### Risiko 5: Data Simulasi Disalahpahami

Dampak:

Pengguna dapat mengira data simulasi sebagai data resmi.

Mitigasi:

1. Beri label data simulasi.
2. Jelaskan fungsi data sebagai pembanding.
3. Jangan klaim data simulasi sebagai data empiris.
4. Pisahkan dataset resmi dan simulasi.

---

## 26. Pengujian Sistem

### 26.1 Pengujian Upload

Kasus uji:

1. Upload CSV valid.
2. Upload Excel valid.
3. Upload file kosong.
4. Upload file dengan format salah.
5. Upload file tanpa kolom wajib.

### 26.2 Pengujian Validasi

Kasus uji:

1. Data tanpa missing value.
2. Data dengan missing value.
3. Data dengan duplikasi.
4. Data dengan periode tidak valid.
5. Data dengan nilai target non-numerik.

### 26.3 Pengujian Preprocessing

Kasus uji:

1. Data berhasil dibersihkan.
2. Data berhasil diurutkan.
3. Data berhasil dikonversi ke format time series.
4. Data hasil preprocessing tampil di dashboard.

### 26.4 Pengujian Model SARIMA

Kasus uji:

1. Model berjalan dengan parameter default.
2. Model berjalan dengan parameter manual.
3. Model gagal dengan parameter tertentu dan sistem memberi pesan error.
4. Model menghasilkan fitted value.
5. Model menghasilkan forecast.

### 26.5 Pengujian Evaluasi

Kasus uji:

1. Sistem menghitung MAE.
2. Sistem menghitung MSE.
3. Sistem menghitung RMSE.
4. Sistem menghitung MAPE.
5. Sistem menampilkan grafik residual.

### 26.6 Pengujian Export

Kasus uji:

1. Hasil forecast dapat diunduh dalam CSV.
2. File CSV berisi kolom yang sesuai.
3. File CSV dapat dibuka kembali.

---

## 27. Acceptance Criteria

Aplikasi dianggap memenuhi kebutuhan versi awal jika:

1. Pengguna dapat mengunggah dataset.
2. Sistem dapat memvalidasi dataset.
3. Sistem dapat melakukan preprocessing data.
4. Sistem dapat membentuk data time series.
5. Sistem dapat menjalankan model SARIMA.
6. Sistem dapat menampilkan evaluasi model.
7. Sistem dapat menghasilkan forecast.
8. Sistem dapat menampilkan grafik aktual dan forecast.
9. Sistem dapat menampilkan halaman kesimpulan.
10. Sistem dapat mengunduh hasil forecast dalam CSV.
11. Sistem dapat membandingkan data tahunan lima tahun dan data bulanan optimal.
12. Sistem menampilkan catatan keterbatasan jika data belum optimal.
13. Tampilan dashboard rapi, konsisten, dan mudah dipahami.
14. Kode tersusun dalam struktur folder yang jelas.
15. Aplikasi dapat dijalankan melalui perintah Streamlit tanpa error utama.

---

## 28. Batasan Produk

Batasan aplikasi:

1. Aplikasi berjalan lokal atau melalui server Streamlit.
2. Aplikasi belum menggunakan database permanen.
3. Aplikasi belum memiliki sistem login.
4. Aplikasi belum menggunakan backend terpisah.
5. Aplikasi masih bergantung pada kualitas dataset yang diunggah.
6. Aplikasi tidak menjamin hasil forecast selalu akurat.
7. Hasil forecast harus ditafsirkan berdasarkan konteks data.
8. Data simulasi hanya digunakan sebagai pembanding teknis.

---

## 29. Rekomendasi Narasi untuk Presentasi

Narasi yang disarankan:

> Aplikasi ini dikembangkan sebagai dashboard forecasting menggunakan metode SARIMA. Sistem tidak hanya menampilkan hasil prediksi, tetapi juga menampilkan proses validasi data, preprocessing, analisis time series, pemodelan, evaluasi, dan kesimpulan. Karena data historis tahunan lima tahun memiliki keterbatasan jumlah observasi, aplikasi juga menyediakan data bulanan pembanding untuk menunjukkan pengaruh struktur data terhadap hasil model. Dengan demikian, dashboard ini dapat digunakan sebagai alat bantu analisis sekaligus media pembelajaran mengenai pemodelan time series menggunakan SARIMA.

---

## 30. Definisi Selesai

Satu fitur dianggap selesai jika memenuhi syarat berikut:

1. Fitur dapat dijalankan tanpa error.
2. Fitur memiliki tampilan yang rapi.
3. Fitur memiliki pesan sukses atau error.
4. Fitur menyimpan output yang diperlukan ke session state.
5. Fitur dapat dijelaskan dalam laporan Tugas Akhir.
6. Fitur sudah diuji dengan dataset contoh.
7. Fitur tidak merusak halaman lain.

---

## 31. Kesimpulan PRD

Aplikasi Forecasting Menggunakan Streamlit dan SARIMA perlu dibangun ulang dengan fokus pada tampilan modern, struktur sistem yang jelas, validasi data yang kuat, serta output forecasting yang mudah dipahami. Rebuild tidak hanya dilakukan untuk memperbaiki tampilan, tetapi juga untuk memperkuat alur akademik dan teknis project.

Prioritas utama pengembangan adalah membuat aplikasi yang dapat menjelaskan proses forecasting secara lengkap. Aplikasi harus mampu menunjukkan perbedaan antara data tahunan lima tahun yang belum optimal dan data bulanan yang lebih sesuai untuk pengujian SARIMA. Dengan begitu, project memiliki nilai akademik yang lebih kuat karena tidak hanya menampilkan hasil prediksi, tetapi juga menjelaskan pentingnya kualitas data dalam pemodelan runtun waktu.

Versi awal aplikasi harus fokus pada fitur inti, yaitu upload data, validasi, preprocessing, transformasi time series, pemodelan SARIMA, evaluasi, forecasting, perbandingan dataset, kesimpulan, dan export CSV. Fitur tambahan seperti export PDF, DOCX, backend terpisah, atau frontend khusus dapat dikembangkan setelah fitur utama stabil.
