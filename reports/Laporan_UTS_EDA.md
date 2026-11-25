# Laporan UTS EDA: Analisis Telemetri Perlambatan

**Judul:** Analisis Eksploratori Telemetri Kecepatan dan Sistem Pengereman pada Satu Cuplikan Operasional  
**Nama:** [Isi nama]  
**Program/Kelas:** [Isi program dan kelas]  
**Mata kuliah:** [Isi mata kuliah]  
**Tanggal:** [Isi tanggal]

> **Pernyataan ruang lingkup:** Dataset adalah transkripsi 64 baris dari screenshot, bukan ekspor sistem tervalidasi. Nama proyek/repository bukan publikasi resmi atau afiliasi KNKT. Analisis ini untuk tujuan akademik, bukan evaluasi keselamatan maupun rekomendasi operasional.

## Abstrak

Laporan ini mengeksplorasi satu cuplikan telemetri bertimestamp per detik pada 27 April 2026 pukul 20:51:18–20:52:21. Dataset memuat 16 kolom yang meliputi waktu, kecepatan, akselerasi, arus beban, tekanan EAB, serta status kontrol. Fokus analisis adalah pemeriksaan struktur dan kualitas data serta deskripsi perubahan sinyal selama cuplikan. Kecepatan teramati dari 0 sampai 109 km/jam; tujuh dari 64 nilai akselerasi tercatat sebagai `--` dan diperlakukan sebagai missing, bukan nol. Karena hanya ada satu cuplikan pendek dan definisi sejumlah kolom belum dikonfirmasi, hasil tidak dapat digeneralisasi ke perjalanan lain atau digunakan untuk menyimpulkan kondisi keselamatan.

**Kata kunci:** EDA, telemetri, deret waktu, missing value, pengereman.

## Bab 1 — Pendahuluan dan Pemahaman Masalah

### 1.1 Latar belakang dan tujuan

Data telemetri dapat membantu menggambarkan perubahan kecepatan dan sinyal kendali dalam suatu interval operasi. Tujuan proyek adalah mendeskripsikan pola variabel numerik dan status kategorikal, memeriksa kualitas data, serta menyiapkan pertanyaan lanjutan untuk validasi domain. Proyek tidak menetapkan adanya kerusakan atau risiko operasional.

### 1.2 Tipe masalah

Tahap ini merupakan **EDA deskriptif deret waktu**, bukan klasifikasi, regresi, atau klasterisasi. Tidak ada label target yang terdefinisi dan jumlah pengamatan hanya mencakup satu cuplikan.

### 1.3 Metrik keberhasilan

Keberhasilan dinilai dari kelengkapan profil data, transparansi penanganan missing value, grafik yang dapat direproduksi, dan kesesuaian interpretasi terhadap definisi sistem. Metrik prediksi seperti akurasi, F1, atau MAE belum relevan.

## Bab 2 — Memahami Data

### 2.1 Pengumpulan data

Sumber yang diberikan adalah screenshot tabel telemetri yang ditranskripsikan menjadi `data/raw/telemetri.csv`. Ini bukan ekstraksi langsung dari basis data atau logger. Reproduksi dan validasi harus dilakukan terhadap ekspor asli.

### 2.2 Deskripsi awal

File memuat 64 observasi per detik dan 16 kolom: `date`, `time`, `km`, `m`, `speed_kmh`, `acceleration_m_s2`, `load_amps`, `eab_bp_psi`, `eab_bc_psi`, `db_exit`, `throttle`, `pcs_open`, `dir_call`, `db_set`, `db_start`, dan `ibs`. Rentang timestamp sekitar 63 detik.

### 2.3 Kualitas data

Tujuh nilai `--` pada akselerasi diperlakukan sebagai missing (7/64 = 10,94%). Timestamp pada cuplikan tidak tampak berulang. Nilai minimum akselerasi tercatat -0,84 m/s²; ini hanya kandidat pemeriksaan, bukan bukti kesalahan. Transisi kolom `km`/`m` dan singkatan status perlu dikonfirmasi. Tidak dilakukan penghapusan, imputasi, atau koreksi data mentah.

### 2.4 Eksplorasi visual awal

Notebook menghasilkan histogram, boxplot, heatmap korelasi Spearman, serta plot kecepatan dan tekanan terhadap waktu. Grafik merupakan deskripsi sampel dan korelasi bukan bukti sebab-akibat.

### 2.5 Kesesuaian bisnis-data

Data relevan untuk menggambarkan satu episode perubahan operasi, tetapi belum cukup untuk menilai kinerja umum, membandingkan perjalanan, atau membuat keputusan keselamatan. Diperlukan definisi fitur dari manual dan beberapa perjalanan dengan identitas perjalanan yang aman.

## Bab 3 — Memuat dan Memeriksa Data

Dataset dibaca menggunakan Pandas dari `data/raw/telemetri.csv`; `--` dikonversi menjadi nilai missing. Kolom numerik diparsing sebagai numerik dan `date` + `time` digabungkan menjadi timestamp. Notebook memeriksa `shape`, tipe data, rentang waktu, duplikasi timestamp, dan `describe()`. Data mentah tetap dipertahankan; hasil parsing disimpan terpisah di `data/processed/`.

## Bab 4 — Penanganan Data Hilang

### 4.1 Identifikasi

Missing terdapat pada `acceleration_m_s2`: 7 baris atau 10,94% dari total. Notebook menampilkan ringkasan dan grafik jumlah missing.

### 4.2 Mekanisme

Mekanisme MCAR/MAR/MNAR tidak dapat ditentukan hanya dari cuplikan. Missing yang berurutan di bagian akhir mungkin terkait kondisi pencatatan atau proses sistem; penyebab perlu diklarifikasi dengan pemilik data.

### 4.3 Eliminasi

Tidak menghapus baris atau kolom pada tahap EDA karena jumlah sampel kecil dan kehilangan observasi berurutan dapat mengaburkan urutan waktu.

### 4.4 Imputasi

Tidak dilakukan imputasi. `--` tetap missing. Imputasi statistik atau model baru dipertimbangkan jika ada kebutuhan pemodelan, setelah mekanisme missing dan validasi domain dipahami.

## Bab 5 — Karakteristik Data

Ringkasan numerik disediakan oleh notebook, termasuk mean, median, simpangan baku, kuartil, minimum, dan maksimum. Rentang kecepatan pada sampel adalah 0–109 km/jam. Pembacaan akselerasi mencakup nilai dari -0,84 hingga 0,05 m/s²; nilai ekstrem perlu ditinjau terhadap resolusi sensor, definisi tanda, dan konteks pengukuran. Bentuk distribusi dan skewness dihitung dari nilai yang tersedia, dengan catatan sampel berurutan bukan observasi independen.

## Bab 6 — Transformasi Data

Tidak ada transformasi nilai pada analisis deskriptif. Timestamp dibuat untuk analisis waktu; label `--` dikonversi menjadi missing. Scaling, encoding, log transform, dan rekayasa fitur tidak diperlukan untuk EDA ini. Jika kelak membangun model, semua transformasi harus dipelajari dari data latih saja untuk mencegah kebocoran data.

## Bab 7 — Hubungan Data

Analisis univariat ditampilkan melalui histogram dan boxplot. Plot deret waktu mengilustrasikan perubahan kecepatan serta tekanan. Korelasi Spearman dihitung untuk fitur numerik sebagai eksplorasi monotonic association. Sampel kecil, tren waktu bersama, serta kemungkinan autokorelasi membatasi inferensi; tidak ditafsirkan sebagai hubungan kausal.

## Bab 8 — Pencilan

Notebook menandai kandidat pencilan numerik menggunakan aturan IQR. Kandidat tidak dihapus atau dicapping otomatis. Nilai -0,84 m/s² patut diverifikasi pada sumber asli dan dokumentasi sensor. Keputusan treatment ditunda sampai diketahui apakah nilai tersebut valid, artefak transkripsi, atau kesalahan alat.

## Bab 9 — Kesimpulan dan Temuan Utama

### 9.1 Temuan

- Cuplikan memuat 64 catatan berinterval satu detik dan kecepatan teramati 0–109 km/jam.
- Terdapat tujuh nilai akselerasi yang tidak tersedia; nilai tersebut tidak diganti nol.
- Berbagai status kontrol berubah selama interval, namun arti teknisnya belum diverifikasi.
- Analisis hanya mendeskripsikan cuplikan yang diberikan dan tidak membuktikan penyebab atau kondisi keselamatan.

### 9.2 Keterbatasan

Satu episode berdurasi sekitar satu menit, data ditranskripsikan dari gambar, kemungkinan kesalahan transkripsi, definisi kolom/satuan yang belum tersedia, tidak ada identitas perjalanan atau konteks operasi, serta sampel terlalu kecil untuk generalisasi dan pemodelan prediktif.

### 9.3 Langkah selanjutnya

Validasi CSV terhadap log asli; konfirmasi arti/satuan kolom dan aturan penandaan missing; kumpulkan sejumlah perjalanan dengan metadata yang aman; tentukan pertanyaan operasional bersama ahli domain; baru pertimbangkan model. Jangan merekomendasikan algoritma prediksi sebelum target, ukuran sampel, dan skema validasi ditetapkan.

## Daftar gambar

Dibuat otomatis oleh notebook di `images/`: histogram fitur numerik, boxplot fitur numerik, heatmap Spearman, grafik kecepatan-waktu, grafik tekanan-waktu, dan ringkasan dashboard.

## Daftar tabel

Tabel 1. Kamus kolom; Tabel 2. Ringkasan kualitas data; Tabel 3. Statistik deskriptif; Tabel 4. Kandidat outlier IQR. Output tabel tersedia saat notebook dijalankan.

## Referensi

1. Dokumentasi Pandas, *User Guide*. https://pandas.pydata.org/docs/user_guide/
2. Dokumentasi Seaborn, *Statistical Data Visualization*. https://seaborn.pydata.org/
3. Dokumentasi KNMI, *Exploratory Data Analysis* (rujukan metodologis dapat ditambahkan sesuai pedoman mata kuliah).
