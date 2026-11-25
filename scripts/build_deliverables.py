from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from pptx import Presentation
from pptx.util import Inches as PptInches, Pt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'raw' / 'telemetri.csv'
REPORTS = ROOT / 'reports'; PRESENTATION = ROOT / 'presentation'; IMAGES = ROOT / 'images'
REPORTS.mkdir(exist_ok=True); PRESENTATION.mkdir(exist_ok=True)
df = pd.read_csv(DATA, na_values=['--', ''])
df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=True, errors='coerce')
df['speed_kmh'] = pd.to_numeric(df['speed_kmh'], errors='coerce')
df['acceleration_m_s2'] = pd.to_numeric(df['acceleration_m_s2'], errors='coerce')
missing_acc = int(df['acceleration_m_s2'].isna().sum())
start, end = df.timestamp.min(), df.timestamp.max()

sections = [
('Abstrak', f'EDA deskriptif dilakukan pada {len(df)} baris dan {len(df.columns)-1} kolom sumber, dari {start} hingga {end}. Kecepatan teramati {df.speed_kmh.min():.0f}–{df.speed_kmh.max():.0f} km/jam. Terdapat {missing_acc} nilai akselerasi missing ({missing_acc/len(df):.2%}); tidak dilakukan imputasi. Data merupakan transkripsi screenshot, sehingga hasil memerlukan validasi sumber.'),
('Bab 1 — Pendahuluan dan pemahaman masalah', 'Tujuan proyek adalah mendeskripsikan satu cuplikan telemetri dan memeriksa kualitas data. Tipe masalah adalah EDA deskriptif deret waktu, bukan klasifikasi/regresi/klasterisasi. Keberhasilan dinilai dari transparansi, reproduksibilitas, dan validasi domain; metrik prediksi belum relevan.'),
('Bab 2 — Memahami data', 'Sumber adalah screenshot tabel yang ditranskripsikan ke CSV, bukan ekstraksi logger terverifikasi. Dataset memiliki timestamp, fitur numerik, dan status kategorikal. Definisi singkatan, satuan serta perubahan kolom km/m memerlukan konfirmasi. Satu cuplikan belum cukup untuk mengukur performa umum.'),
('Bab 3 — Memuat dan memeriksa data', 'Data dimuat dengan Pandas. Tanggal dan waktu digabung menjadi timestamp, string -- dibaca sebagai missing, dan fitur angka dikonversi numerik. Pemeriksaan meliputi dimensi, tipe kolom, duplikasi timestamp, rentang waktu, serta statistik deskriptif.'),
('Bab 4 — Missing data', f'{missing_acc} dari {len(df)} nilai akselerasi ({missing_acc/len(df):.2%}) tidak tersedia. Mekanisme MCAR/MAR/MNAR tidak dapat ditentukan dari sampel ini. Baris tidak dihapus dan nilai tidak diimputasi karena urutan waktu penting dan alasan missing belum diketahui.'),
('Bab 5 — Karakteristik data', f'Kecepatan memiliki rentang {df.speed_kmh.min():.0f}–{df.speed_kmh.max():.0f} km/jam. Ringkasan numerik lengkap dihitung di notebook. Nilai minimum akselerasi teramati {df.acceleration_m_s2.min():.2f} m/s²; nilai ekstrem hanya kandidat pemeriksaan, bukan otomatis kesalahan.'),
('Bab 6 — Transformasi data', 'Tidak ada transformasi statistik, scaling, atau encoding pada EDA. Timestamp dibuat untuk visualisasi waktu. Bila kelak membangun model, transformasi harus dipelajari pada data latih saja.'),
('Bab 7 — Visualisasi hubungan', 'Notebook menghasilkan histogram, boxplot, heatmap Spearman, dan grafik deret waktu. Korelasi menggambarkan asosiasi sampel, bukan sebab-akibat; tren waktu dan autokorelasi membatasi inferensi.'),
('Bab 8 — Pencilan', 'Kandidat pencilan diidentifikasi dengan aturan IQR di notebook. Tidak ada nilai yang dihapus atau dicapping otomatis. Periksa sumber asli, kalibrasi, satuan, dan konteks domain sebelum treatment.'),
('Bab 9 — Kesimpulan dan langkah lanjut', 'Cuplikan terdiri dari observasi satu detik selama sekitar satu menit, dengan kecepatan 0–109 km/jam dan tujuh nilai akselerasi missing. Keterbatasan utama adalah transkripsi screenshot, satu cuplikan pendek, dan kamus data yang belum terverifikasi. Langkah berikutnya: validasi log asli, konfirmasi definisi kolom, kumpulkan perjalanan tambahan yang diizinkan, lalu tentukan target bila pemodelan memang diperlukan.'),
]

# DOCX
D = Document(); D.add_heading('Laporan UTS EDA: Analisis Telemetri Perlambatan', 0)
D.add_paragraph('Nama: [Isi nama] | Kelas: [Isi kelas] | Mata kuliah: [Isi mata kuliah]')
D.add_paragraph('Catatan: laporan akademik atas transkripsi screenshot; bukan publikasi resmi/afiliasi KNKT dan bukan evaluasi keselamatan.')
for title, text in sections:
    D.add_heading(title, level=1); D.add_paragraph(text)
for name in ['speed_time_series.png', 'heatmap.png', 'dashboard.png']:
    p = IMAGES / name
    if p.exists():
        D.add_heading(name.replace('_', ' ').replace('.png', '').title(), level=2)
        D.add_picture(str(p), width=Inches(6.2))
D.add_heading('Daftar tabel dan gambar', level=1)
D.add_paragraph('Tabel statistik, missing, dan kandidat IQR tersedia pada output notebook. Gambar PNG dibuat oleh scripts/generate_figures.py.')
D.add_heading('Referensi', level=1)
D.add_paragraph('Pandas documentation: https://pandas.pydata.org/docs/ | Seaborn documentation: https://seaborn.pydata.org/')
D.save(REPORTS / 'Laporan_UTS_EDA.docx')

# PDF
styles = getSampleStyleSheet(); story = [Paragraph('Laporan UTS EDA: Analisis Telemetri Perlambatan', styles['Title']), Spacer(1, 12)]
story.append(Paragraph('Nama: [Isi nama] | Kelas: [Isi kelas] | Mata kuliah: [Isi mata kuliah]', styles['Normal']))
story.append(Paragraph('Catatan: analisis akademik atas transkripsi screenshot; bukan publikasi resmi/afiliasi KNKT dan bukan evaluasi keselamatan.', styles['Italic']))
for title, text in sections:
    story += [Spacer(1, 10), Paragraph(title, styles['Heading2']), Paragraph(text.replace('&','&amp;'), styles['BodyText'])]
    if title.startswith('Bab 7'):
        for name in ['speed_time_series.png', 'heatmap.png']:
            p = IMAGES / name
            if p.exists(): story += [Spacer(1, 6), Image(str(p), width=440, height=230)]
SimpleDocTemplate(str(REPORTS / 'Laporan_UTS_EDA.pdf'), pagesize=A4, title='Laporan UTS EDA').build(story)

# PPTX, 12 slides
slides = [
('Analisis Eksploratori Telemetri Perlambatan', 'Nama: [Isi nama]\nKelas: [Isi kelas]\nSatu cuplikan operasional — EDA akademik'),
('Ruang lingkup', 'Transkripsi screenshot; satu interval sekitar 63 detik.\nBukan publikasi resmi KNKT atau penilaian keselamatan.'),
('Pertanyaan analisis', 'Bagaimana sinyal numerik dan status berubah selama cuplikan?\nIsu kualitas data apa yang harus divalidasi?'),
('Dataset', f"{len(df)} observasi\n{len(df.columns)-1} kolom sumber + timestamp turunan\n{start} sampai {end}"),
('Metode', 'Pandas untuk inspeksi dan statistik\nHistogram, boxplot, deret waktu\nSpearman dan IQR bersifat eksploratif'),
('Kualitas data', f'{missing_acc} nilai akselerasi missing ({missing_acc/len(df):.2%})\nTidak diimputasi\nDefinisi km/m dan singkatan perlu konfirmasi'),
('Kecepatan', f"Rentang teramati {df.speed_kmh.min():.0f}–{df.speed_kmh.max():.0f} km/jam.\nLihat grafik deret waktu."),
('Distribusi dan pencilan', 'Histogram/boxplot membantu menandai bentuk dan kandidat nilai ekstrem.\nPencilan statistik tidak otomatis salah.'),
('Hubungan antar fitur', 'Heatmap Spearman menunjukkan asosiasi sampel.\nKorelasi bukan kausalitas; tren waktu/autokorelasi membatasi inferensi.'),
('Keterbatasan', 'Satu cuplikan pendek; data ditranskripsikan; kamus data dan konteks operasi belum lengkap.\nTidak untuk generalisasi atau keputusan keselamatan.'),
('Kesimpulan', 'EDA mendokumentasikan pola dan isu kualitas data.\nTujuh pembacaan akselerasi missing.\nValidasi sumber sebelum menafsirkan sinyal.'),
('Langkah selanjutnya', 'Validasi terhadap log asli dan manual.\nKumpulkan data tambahan yang diizinkan.\nTentukan pertanyaan/target sebelum pemodelan.'),
]
prs = Presentation(); prs.slide_width = PptInches(13.333); prs.slide_height = PptInches(7.5)
for title, body in slides:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    slide.placeholders[1].text = body
    for p in slide.placeholders[1].text_frame.paragraphs:
        p.font.size = Pt(24)
    slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(32)
    if title == 'Kecepatan' and (IMAGES / 'speed_time_series.png').exists():
        slide.shapes.add_picture(str(IMAGES / 'speed_time_series.png'), PptInches(6.7), PptInches(2.1), width=PptInches(5.8))
    if title == 'Hubungan antar fitur' and (IMAGES / 'heatmap.png').exists():
        slide.shapes.add_picture(str(IMAGES / 'heatmap.png'), PptInches(6.7), PptInches(2.1), width=PptInches(5.8))
prs.save(PRESENTATION / 'Presentasi_UTS.pptx')
print('Selesai: DOCX, PDF, PPTX dibuat. Jalankan scripts/generate_figures.py terlebih dahulu untuk menyertakan grafik.')
