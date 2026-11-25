from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'raw' / 'telemetri.csv'
OUT = ROOT / 'images'
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA, na_values=['--', ''])
df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=True, errors='coerce')
cols = ['km', 'm', 'speed_kmh', 'acceleration_m_s2', 'load_amps', 'eab_bp_psi', 'eab_bc_psi']
for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Histograms and boxplots
for col in ['speed_kmh', 'acceleration_m_s2', 'load_amps', 'eab_bp_psi', 'eab_bc_psi']:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df[col].dropna(), kde=df[col].nunique() > 2, ax=ax, color='#2563eb')
    ax.set(title=f'Distribusi {col}', xlabel=col)
    fig.tight_layout(); fig.savefig(OUT / f'histogram_{col}.png', dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 2.5))
    sns.boxplot(x=df[col], ax=ax, color='#93c5fd')
    ax.set_title(f'Boxplot {col}')
    fig.tight_layout(); fig.savefig(OUT / f'boxplot_{col}.png', dpi=160); plt.close(fig)

# Spearman heatmap / correlation chart
corr = df[cols].corr(method='spearman', min_periods=3)
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='vlag', center=0, ax=ax)
ax.set_title('Korelasi Spearman — fitur numerik')
fig.tight_layout(); fig.savefig(OUT / 'heatmap.png', dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8, 5))
corr['speed_kmh'].drop('speed_kmh').sort_values().plot.barh(ax=ax, color='#0f766e')
ax.set_title('Asosiasi Spearman dengan kecepatan'); ax.set_xlabel('Koefisien Spearman')
fig.tight_layout(); fig.savefig(OUT / 'correlation.png', dpi=160); plt.close(fig)

# Time series charts
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(df.timestamp, df.speed_kmh, marker='.', color='#1d4ed8')
ax.set(title='Kecepatan terhadap waktu', ylabel='km/jam', xlabel='Waktu'); ax.grid(alpha=.25)
fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(OUT / 'speed_time_series.png', dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(df.timestamp, df.eab_bp_psi, marker='.', label='EAB BP (psi)')
ax.plot(df.timestamp, df.eab_bc_psi, marker='.', label='EAB BC (psi)')
ax.set(title='Tekanan EAB terhadap waktu', ylabel='psi', xlabel='Waktu'); ax.legend(); ax.grid(alpha=.25)
fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(OUT / 'brake_pressure_time_series.png', dpi=160); plt.close(fig)

# Dashboard summary image
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(df.timestamp, df.speed_kmh, color='#1d4ed8'); axes[0, 0].set_title('Kecepatan (km/jam)'); axes[0, 0].grid(alpha=.2)
axes[0, 1].plot(df.timestamp, df.eab_bp_psi, label='BP'); axes[0, 1].plot(df.timestamp, df.eab_bc_psi, label='BC'); axes[0, 1].set_title('Tekanan EAB (psi)'); axes[0, 1].legend(); axes[0, 1].grid(alpha=.2)
missing = df.isna().sum(); missing = missing[missing > 0]
if len(missing):
    missing.plot.bar(ax=axes[1, 0], color='#d97706', title='Missing values')
else:
    axes[1, 0].text(.5, .5, 'Tidak ada missing', ha='center'); axes[1, 0].set_title('Missing values')
sns.heatmap(corr, cmap='vlag', center=0, ax=axes[1, 1], cbar=False); axes[1, 1].set_title('Korelasi Spearman')
fig.suptitle('Ringkasan EDA Telemetri — satu cuplikan')
fig.tight_layout(); fig.savefig(OUT / 'dashboard.png', dpi=160); plt.close(fig)
print(f'Grafik disimpan ke {OUT}')
