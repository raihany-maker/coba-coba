import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Fiskal & Pengangguran",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS TEMA PASTEL / LUCU ---
st.markdown("""
<style>
    /* Background utama & sidebar */
    .stApp {
        background-color: #FAF5FF;
    }
    [data-testid="stSidebar"] {
        background-color: #FFF0F5;
        border-right: 2px solid #FFD1DC;
    }

    /* Kartu Metric / KPI */
    .stMetric {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #FFE5EC;
        box-shadow: 0px 4px 10px rgba(255, 182, 193, 0.2);
    }

    /* Warna judul & teks */
    h1, h2, h3, h4, h5, h6, label {
        color: #5E4B8B !important;
        font-family: 'Poppins', sans-serif;
    }

    /* Tab Navigasi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFE5EC;
        border-radius: 12px 12px 0px 0px;
        padding: 8px 16px;
        color: #5E4B8B;
        font-weight: 600;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFB3C1 !important;
        color: #2B2D42 !important;
    }

    /* Tag multiselect */
    span[data-baseweb="tag"] {
        background-color: #FF8FA3 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. LOAD & CACHE DATASET
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Alam-A99/DATAAKSI/refs/heads/main/dataset_fiskal_97_hipoFull.csv'
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()


# ---------------------------------------------------------
# 3. SIDEBAR / FILTER INTERAKTIF
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/analytics.png", width=70)
st.sidebar.title("⚙️ Filter & Panel")
st.sidebar.markdown("Atur filter di bawah untuk menyesuaikan data pada visualisasi.")

# Filter Tahun
min_tahun = int(df['Tahun'].min()) if 'Tahun' in df.columns else 2000
max_tahun = int(df['Tahun'].max()) if 'Tahun' in df.columns else 2024

selected_years = st.sidebar.slider(
    "🗓️ Rentang Tahun",
    min_value=min_tahun,
    max_value=max_tahun,
    value=(min_tahun, max_tahun)
)

# Filter Kota untuk Chart Tren
semua_kota = sorted(df['Kota'].dropna().unique().tolist())
default_kota = [k for k in ['Kota Makassar', 'Kota Salatiga', 'Kota Bandung', 'Kota Medan'] if k in semua_kota]

selected_kota = st.sidebar.multiselect(
    "🏙️ Pilih Kota untuk Tren",
    options=semua_kota,
    default=default_kota if default_kota else semua_kota[:4]
)

# --- UBAH SLIDER MENJADI SELECTBOX (OPSI) ---
top_n = st.sidebar.selectbox(
    "📊 Jumlah Top Kota (BM Ekonomi vs Sosial)",
    options=[5, 10, 12, 15, 20, 25],
    index=3  # Default 15
)

# Apply Filter Data
df_filtered = df[(df['Tahun'] >= selected_years[0]) & (df['Tahun'] <= selected_years[1])].copy()


# ---------------------------------------------------------
# 4. HEADER & METRIK RINGKASAN (KPI)
# ---------------------------------------------------------
st.title("📊 Dashboard Analisis Kebijakan Fiskal & Pengangguran Kota")
st.markdown("Visualisasi interaktif hubungan Belanja Modal (BM) Ekonomi, BM Perlindungan Sosial, dan Tingkat Pengangguran.")

st.markdown("---")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric("📋 Total Data Digunakan", f"{len(df_filtered):,} baris")

with col_kpi2:
    avg_unemp = df_filtered['PENGANGGURAN'].mean() if not df_filtered.empty else 0
    st.metric("📉 Rata-rata Pengangguran", f"{avg_unemp:.2f}%")

with col_kpi3:
    avg_bm_eko = df_filtered['bm_ekonomi'].mean() if not df_filtered.empty else 0
    st.metric("💰 Rata-rata BM Ekonomi", f"{avg_bm_eko:,.0f}")

with col_kpi4:
    avg_bm_sos = df_filtered['bm_perlindungan_sosial'].mean() if not df_filtered.empty else 0
    st.metric("🛡️ Rata-rata BM Sosial", f"{avg_bm_sos:,.0f}")

st.markdown("---")


# ---------------------------------------------------------
# 5. GRAFIK DENGAN LAYOUT TABS (TAB PREVIEW DIHAPUS)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📌 Analisis Hubungan & Kategori", "🏛️ Perbandingan Antar Kota"])

with tab1:
    col1, col2 = st.columns(2)

    # --- CHART 1: BM EKONOMI VS PENGANGGURAN ---
    with col1:
        st.subheader("1. BM Ekonomi vs Pengangguran")
        if not df_filtered.empty and len(df_filtered) > 1:
            X1 = sm.add_constant(df_filtered['bm_ekonomi'])
            model1 = sm.OLS(df_filtered['PENGANGGURAN'], X1).fit()

            x_line1 = np.linspace(df_filtered['bm_ekonomi'].min(), df_filtered['bm_ekonomi'].max(), 100)
            y_line1 = model1.params['const'] + model1.params['bm_ekonomi'] * x_line1

            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_filtered['bm_ekonomi'], y=df_filtered['PENGANGGURAN'],
                mode='markers', name='Data Titik',
                text=df_filtered['Kota'],
                marker=dict(size=8, color='#FF6B6B', opacity=0.7)
            ))
            fig1.add_trace(go.Scatter(
                x=x_line1, y=y_line1,
                mode='lines', name=f'Regresi (R²={model1.rsquared:.2f})',
                line=dict(color='#4ECDC4', width=3)
            ))
            fig1.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='BM Ekonomi',
                yaxis_title='Pengangguran (%)',
                margin=dict(l=20, r=20, b=30, t=40),
                height=450
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Data tidak cukup untuk menghitung regresi.")

    # --- CHART 2: BM SOSIAL KATEGORIAL ---
    with col2:
        st.subheader("2. Pengangguran per Kategori BM Sosial")
        if not df_filtered.empty and df_filtered['bm_perlindungan_sosial'].nunique() >= 3:
            df_filtered['Kategori_BM_Sosial'] = pd.qcut(
                df_filtered['bm_perlindungan_sosial'],
                q=3,
                labels=['Sosial Rendah', 'Sosial Sedang', 'Sosial Tinggi'],
                duplicates='drop'
            )
            df_bar2 = df_filtered.groupby('Kategori_BM_Sosial', observed=False)['PENGANGGURAN'].mean().reset_index()

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df_bar2['Kategori_BM_Sosial'],
                y=df_bar2['PENGANGGURAN'],
                text=df_bar2['PENGANGGURAN'].round(2),
                textposition='auto',
                marker_color=['#B5E2FA', '#EDA2C0', '#C7CEEA']
            ))
            fig2.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Kelompok BM Perlindungan Sosial',
                yaxis_title='Rata-Rata Pengangguran (%)',
                margin=dict(l=20, r=20, b=30, t=40),
                height=450
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Variasi data BM Perlindungan Sosial tidak mencukupi.")


with tab2:
    col3, col4 = st.columns(2)

    # --- CHART 3: HORIZONTAL BAR TOP N KOTA ---
    with col3:
        st.subheader(f"3. BM Ekonomi vs BM Sosial (Top {top_n} Kota)")
        df_top = (
            df_filtered.groupby('Kota')[['bm_ekonomi', 'bm_perlindungan_sosial']]
            .mean()
            .nlargest(top_n, 'bm_ekonomi')
            .sort_values('bm_ekonomi', ascending=True)
            .reset_index()
        )

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=df_top['Kota'], x=df_top['bm_ekonomi'],
            name='Rata-Rata BM Ekonomi', orientation='h', marker_color='#957FEF'
        ))
        fig3.add_trace(go.Bar(
            y=df_top['Kota'], x=df_top['bm_perlindungan_sosial'],
            name='Rata-Rata BM Sosial', orientation='h', marker_color='#FF8FA3'
        ))
        fig3.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            xaxis_title='Rata-Rata Anggaran',
            yaxis_title='Kota',
            margin=dict(l=100, r=20, b=30, t=40),
            height=500
        )
        st.plotly_chart(fig3, use_container_width=True)

    # --- CHART 4: TREN TAHUNAN ANTAR KOTA ---
    with col4:
        st.subheader("4. Tren Pengangguran Tahunan Antar Kota")
        if selected_kota:
            df_line = df_filtered[df_filtered['Kota'].isin(selected_kota)].sort_values('Tahun')

            fig4 = go.Figure()
            for kota in selected_kota:
                df_k = df_line[df_line['Kota'] == kota]
                if not df_k.empty:
                    fig4.add_trace(go.Scatter(
                        x=df_k['Tahun'], y=df_k['PENGANGGURAN'],
                        mode='lines+markers', name=kota,
                        marker=dict(size=7),
                        line=dict(width=2.5)
                    ))

            fig4.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Tahun',
                yaxis_title='Tingkat Pengangguran (%)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, b=30, t=50),
                height=500
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Pilih minimal satu kota di sidebar untuk menampilkan tren.")
