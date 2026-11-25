# Dataset Mentah — Telemetri

Dataset ini berisi rekaman telemetri operasional dari tanggal 27 April 2026, pukul 20:51:18–20:52:21.

## Sumber

Data ditranskripsikan dari screenshot tabel asli untuk keperluan proyek EDA.

## File

- `telemetri.csv`: data mentah, satu baris mewakili satu pembacaan waktu.

## Catatan kualitas

- Kolom `acceleration_m_s2` menggunakan nilai `--` untuk 7 baris ketika pembacaan tidak tersedia.
- Kolom dipertahankan tanpa imputasi agar perbedaan data mentah dan data olahan tetap jelas.
- Arti, satuan, dan perilaku kolom operasional perlu dikonfirmasi dari manual sistem.
