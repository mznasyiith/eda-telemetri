from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'raw' / 'telemetri.csv'

st.set_page_config(page_title='EDA Telemetri', layout='wide')
st.title('Dashboard EDA — Telemetri Operasional')
st.warning('Analisis akademik atas satu cuplikan transkripsi screenshot; bukan dashboard resmi KNKT atau alat keselamatan operasional.')

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, na_values=['--', ''])
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=True, errors='coerce')
    numeric = ['km', 'm', 'speed_kmh', 'acceleration_m_s2', 'load_amps', 'eab_bp_psi', 'eab_bc_psi']
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df, numeric

if not DATA.exists():
    st.error(f'File dataset tidak ditemukan: {DATA}')
    st.stop()

df, numeric = load_data()
c1, c2, c3, c4 = st.columns(4)
c1.metric('Jumlah observasi', f'{len(df)}')
c2.metric('Jumlah kolom', f'{len(df.columns)}')
c3.metric('Kecepatan minimum', f"{df.speed_kmh.min():.0f} km/jam")
c4.metric('Kecepatan maksimum', f"{df.speed_kmh.max():.0f} km/jam")

st.subheader('Kecepatan terhadap waktu')
st.line_chart(df.set_index('timestamp')['speed_kmh'], y_label='km/jam')

st.subheader('Tekanan EAB terhadap waktu')
st.line_chart(df.set_index('timestamp')[['eab_bp_psi', 'eab_bc_psi']], y_label='psi')

left, right = st.columns(2)
with left:
    st.subheader('Missing values')
    missing = df.isna().sum().sort_values(ascending=False)
    st.dataframe(pd.DataFrame({'missing_count': missing, 'missing_pct': 100 * missing / len(df)}), use_container_width=True)
with right:
    st.subheader('Statistik fitur numerik')
    st.dataframe(df[numeric].describe().T, use_container_width=True)

st.subheader('Korelasi Spearman')
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(df[numeric].corr(method='spearman', min_periods=3), annot=True, fmt='.2f', cmap='vlag', center=0, ax=ax)
st.pyplot(fig)
plt.close(fig)

st.subheader('Kandidat pencilan IQR')
rows = []
for col in numeric:
    s = df[col].dropna()
    if s.empty:
        continue
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    mask = df[col].notna() & ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr))
    for idx in df.index[mask]:
        rows.append({'timestamp': df.loc[idx, 'timestamp'], 'feature': col, 'value': df.loc[idx, col]})
st.dataframe(pd.DataFrame(rows), use_container_width=True)
st.caption('IQR menandai kandidat statistik saja. Tidak ada nilai yang dihapus atau dikoreksi. Konfirmasi seluruh interpretasi terhadap log asli dan dokumentasi sistem.')
