# Naskah Presentasi UTS (12 slide)

## Slide 1 — Judul
**Analisis Eksploratori Telemetri Perlambatan**  
Nama, kelas, mata kuliah, tanggal.  
Narasi: “Presentasi ini membahas EDA satu cuplikan telemetri. Hasilnya deskriptif dan bukan penilaian keselamatan.”

## Slide 2 — Konteks
- Data telemetri berinterval satu detik
- Screenshot ditranskripsikan ke CSV
- Satu interval, 27 April 2026
Narasi: “Sumber belum berupa ekspor logger; validasi dengan data asli menjadi batas utama.”

## Slide 3 — Pertanyaan dan tujuan
- Bagaimana variabel berubah selama cuplikan?
- Apa isu kualitas data yang perlu ditinjau?
- Tidak membangun model prediksi pada tahap ini

## Slide 4 — Dataset
- 64 baris, 16 kolom
- Rentang waktu sekitar 63 detik
- Fitur kecepatan, akselerasi, arus, tekanan, dan status

## Slide 5 — Metode
- Pandas untuk inspeksi dan statistik
- Matplotlib/Seaborn untuk visualisasi
- IQR untuk kandidat pencilan; Spearman untuk asosiasi monotonic
- Tidak mengimputasi atau menghapus data

## Slide 6 — Kualitas data
- 7/64 nilai akselerasi missing (10,94%)
- Tidak terlihat timestamp duplikat pada transkripsi
- Definisi km/m dan singkatan status perlu konfirmasi

## Slide 7 — Perubahan kecepatan
Tampilkan `images/speed_time_series.png`.  
Narasi: “Kecepatan teramati dari 0 sampai 109 km/jam dan berubah sepanjang interval. Satu cuplikan tidak mewakili perjalanan lain.”

## Slide 8 — Distribusi dan pencilan
Tampilkan histogram dan boxplot.  
Narasi: “Grafik membantu mengidentifikasi nilai untuk diperiksa; aturan statistik tidak otomatis menjadikan nilai sebagai kesalahan.”

## Slide 9 — Tekanan dan status
Tampilkan `images/brake_pressure_time_series.png`.  
Narasi: “Perubahan sinyal terlihat bersamaan dengan waktu. Arti hubungan sistem memerlukan manual dan pengetahuan domain.”

## Slide 10 — Korelasi
Tampilkan `images/heatmap.png`.  
Narasi: “Korelasi Spearman hanya asosiasi pada sampel ini, bukan kausalitas. Tren waktu bersama dapat memengaruhi korelasi.”

## Slide 11 — Keterbatasan
- Satu sampel pendek dan hasil transkripsi screenshot
- Metadata/definisi fitur belum lengkap
- Tidak cukup untuk generalisasi atau kesimpulan keselamatan

## Slide 12 — Kesimpulan dan langkah lanjut
- Pertahankan missing dan data mentah
- Validasi dengan log asli dan manual sistem
- Kumpulkan perjalanan tambahan yang diizinkan
- Tentukan pertanyaan bisnis sebelum pemodelan
Narasi penutup: “Kontribusi utama proyek ini adalah profil data yang transparan dan daftar validasi berikutnya, bukan klaim diagnosis.”
