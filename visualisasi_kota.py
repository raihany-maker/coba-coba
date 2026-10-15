import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Fiskal", layout="wide")

# --- Custom CSS Tema Warna Pastel / Lucu ---
st.markdown("""
<style>
    /* Warna background utama & sidebar */
    .stApp {
        background-color: #FAF5FF;
    }
    [data-testid="stSidebar"] {
        background-color: #FFF0F5;
        border-right: 2px solid #FFD1DC;
    }

    /* Warna judul & teks header */
    h1, h2, h3, h4, h5, h6, label {
        color: #5E4B8B !important;
        font-family: 'Poppins', sans-serif;
    }

    /* Styling Tab Navigasi */
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

    /* Warna tag/pills pada multiselect */
    span[data-baseweb="tag"] {
        background-color: #FF8FA3 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Filter & Panel ---
st.sidebar.title("⚙️ Filter & Panel")
st.sidebar.caption("Atur filter di bawah untuk menyesuaikan data pada visualisasi.")

# 1. Rentang Tahun
rentang_tahun = st.sidebar.slider("📅 Rentang Tahun", 2014, 2024, (2014, 2024))

# 2. Pilih Kota
pilih_kota = st.sidebar.multiselect(
    "🏙️ Pilih Kota untuk Tren",
    options=["Kota Makassar", "Kota Salatiga", "Kota Bandung", "Kota Medan", "Kota Banda Aceh"],
    default=["Kota Makassar", "Kota Salatiga", "Kota Bandung", "Kota Medan"]
)

# 3. Opsi Jumlah Top Kota (Menggantikan Slider)
opsi_top_kota = [5, 10, 12, 15, 20]
jumlah_top_kota = st.sidebar.selectbox(
    "📊 Jumlah Top Kota (BM Ekonomi vs Sosial)",
    options=opsi_top_kota,
    index=2  # Default ke angka 12
)

# --- Main Area (Hanya 2 Tab, Tab Preview Dataset Dihapus) ---
tab1, tab2 = st.tabs([
    "📌 Analisis Hubungan & Kategori", 
    "🏛️ Perbandingan Antar Kota"
])

with tab1:
    st.subheader("Analisis Hubungan & Kategori")
    # Tempelkan kode grafik/visualisasi kamu untuk Tab 1 di sini

with tab2:
    st.subheader("Perbandingan Antar Kota")
    # Tempelkan kode grafik/visualisasi kamu untuk Tab 2 di sini
