## Membuat laporan, slide, dan grafik

Jalankan dari root repository setelah memasang `requirements.txt`:

```bash
python scripts/generate_figures.py
python scripts/build_deliverables.py
```

Skrip menghasilkan `Laporan_UTS_EDA.docx`, `Laporan_UTS_EDA.pdf`, `Presentasi_UTS.pptx`, dan grafik di `images/`. Lengkapi identitas mahasiswa dan validasi data/kamus kolom sebelum pengumpulan. File biner hasil dibuat secara lokal oleh skrip, bukan otomatis di-commit oleh perintah tersebut.
