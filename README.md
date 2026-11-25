# KNKT Railway Risk Analysis — EDA

Proyek Exploratory Data Analysis (EDA) untuk memeriksa pola telemetri operasional pada satu cuplikan perlambatan kendaraan/kereta. Analisis mencakup kualitas data, missing values, statistik deskriptif, distribusi, pencilan, korelasi, dan visualisasi deret waktu.

> **Penting:** Nama proyek ini hanya label akademik. Repository ini bukan publikasi resmi KNKT dan tidak berafiliasi dengan KNKT. Data yang tersedia merupakan transkripsi screenshot, bukan ekspor sistem tervalidasi. Hasilnya tidak boleh digunakan untuk mengambil keputusan operasional atau keselamatan.

## Struktur proyek

```text
KNKT-Railway-Risk-Analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                 # data sumber; jangan ditimpa
│   └── processed/           # hasil pembersihan dari notebook
├── notebooks/
│   └── KNKT_EDA.ipynb
├── reports/                 # laporan DOCX/PDF (belum dibuat)
├── presentation/            # slide PPTX (belum dibuat)
├── dashboard/               # dashboard Power BI (belum dibuat)
└── images/                  # grafik hasil notebook
```

Repository GitHub saat ini bernama [`eda-telemetri`](https://github.com/mznasyiith/eda-telemetri). Direktori root lokal dapat dinamai `KNKT-Railway-Risk-Analysis` saat clone.

## Dataset

File sumber: [`data/raw/telemetri.csv`](data/raw/telemetri.csv). Dataset berisi 64 catatan per detik untuk 16 kolom, dari 27 April 2026 20:51:18 sampai 20:52:21. Nilai `--` pada akselerasi dipertahankan sebagai missing value saat dibaca.

Beberapa definisi kolom dan satuan perlu dikonfirmasi terhadap dokumentasi sistem. Khususnya, transisi nilai `km`/`m`, status kontrol, dan nilai sensor harus diverifikasi dengan sumber asli. Jangan menarik kesimpulan keselamatan dari cuplikan tunggal ini.

## Menjalankan notebook

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/KNKT_EDA.ipynb
```

Jalankan notebook dari direktori root repository. Notebook menyimpan data hasil parsing ke `data/processed/` dan grafik ke `images/`.

## Analisis yang tersedia

- Inspeksi dimensi, tipe kolom, rentang waktu, dan duplikasi timestamp.
- Ringkasan missing values dan statistik deskriptif.
- Distribusi dan boxplot fitur numerik.
- Korelasi Pearson/Spearman sebagai eksplorasi, bukan bukti sebab-akibat.
- Grafik deret waktu kecepatan dan tekanan rem.
- Deteksi kandidat outlier menggunakan IQR; kandidat perlu pemeriksaan domain, tidak otomatis dihapus.

## Artefak yang belum tersedia

Laporan `DOCX/PDF`, presentasi `PPTX`, dan dashboard `PBIX` belum dibuat. Foldernya disiapkan untuk artefak tersebut. Grafik PNG dibuat dengan menjalankan notebook.

## Etika, privasi, dan batasan

Repository ini publik. Pastikan Anda berwenang membagikan data telemetri. Jika data termasuk informasi operasional terbatas, segera hapus dari repository publik dan gunakan data sintetis/tersamarkan. Analisis hanya bersifat akademik dan deskriptif; satu cuplikan pendek tidak mewakili operasi keseluruhan.
