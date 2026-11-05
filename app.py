import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. Fungsi Load & Preprocessing Data
@st.cache_data
def load_data():
    # Membaca dataset train.csv
    df = pd.read_csv("train.csv")
    
    # Penanganan data kosong (Missing Value Handling)
    df['Postal Code'] = df['Postal Code'].fillna(0).astype(int)
    
    # Pengubahan tipe data Tanggal
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
    
    # Ekstraksi Tahun dan Bulan-Tahun
    df['Year'] = df['Order Date'].dt.year
    df['Year_Month'] = df['Order Date'].dt.to_period('M').astype(str)
    
    return df

df = load_data()

# 3. Sidebar Filter Interaktif (Elemen 3 Rubrik UTS)
st.sidebar.header("🔍 Filter Data Dashboard")

# Filter 1: Rentang Tahun
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Pilih Tahun Order:",
    options=years,
    default=years
)

# Filter 2: Region (Wilayah)
regions = df['Region'].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "Pilih Region Wilayah:",
    options=regions,
    default=regions
)

# Filter 3: Kategori Produk
categories = df['Category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=categories,
    default=categories
)

# Terapkan Filter pada Dataframe
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories))
]

# 4. Header & Judul Dashboard
st.title("📊 Superstore Sales & Performance Dashboard")
st.markdown("### Executive Summary Analysis | Retail E-Commerce Data")
st.markdown("---")

# Validasi jika data hasil filter kosong
if filtered_df.empty:
    st.warning("⚠️ Data tidak ditemukan untuk kombinasi filter ini. Silakan sesuaikan filter Anda.")
    st.stop()

# 5. Ringkasan Utama / KPI Cards (Elemen 1 Rubrik UTS)
total_sales = filtered_df['Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()
total_customers = filtered_df['Customer ID'].nunique()
avg_sales_per_order = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="💰 Total Penjualan (Sales)", value=f"${total_sales:,.2f}")

with col2:
    st.metric(label="📦 Total Pesanan (Orders)", value=f"{total_orders:,}")

with col3:
    st.metric(label="👥 Pelanggan Unik", value=f"{total_customers:,}")

with col4:
    st.metric(label="📈 Rata-rata Penjualan/Pesanan", value=f"${avg_sales_per_order:,.2f}")

st.markdown("---")

# 6. Variasi Bagan / Charts (Elemen 2 Rubrik UTS - Minimal 4 Bagan)

# Baris 1: Line Chart & Donut Chart
row1_col1, row1_col2 = st.columns([6, 4])

with row1_col1:
    st.subheader("📈 Chart 1: Tren Penjualan Bulanan (Line Chart)")
    monthly_sales = filtered_df.groupby('Year_Month')['Sales'].sum().reset_index()
    fig_line = px.line(
        monthly_sales, 
        x='Year_Month', 
        y='Sales', 
        labels={'Year_Month': 'Bulan-Tahun', 'Sales': 'Total Sales ($)'},
        markers=True,
        color_discrete_sequence=['#1f77b4']
    )
    fig_line.update_layout(xaxis_tickangle=-45, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_line, use_container_width=True)

with row1_col2:
    st.subheader("🍩 Chart 2: Proporsi Segmen Pelanggan (Donut Chart)")
    segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    fig_donut = px.pie(
        segment_sales, 
        names='Segment', 
        values='Sales', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_donut, use_container_width=True)

# Baris 2: Bar Chart & Horizontal Bar Chart
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("📊 Chart 3: Top 10 Sub-Kategori Penjualan (Bar Chart)")
    subcat_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
    fig_bar = px.bar(
        subcat_sales, 
        x='Sub-Category', 
        y='Sales', 
        color='Sales',
        color_continuous_scale='Viridis',
        labels={'Sub-Category': 'Sub-Kategori', 'Sales': 'Total Sales ($)'}
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_col2:
    st.subheader("🗺️ Chart 4: Penjualan berdasarkan Region (Horizontal Bar Chart)")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=True)
    fig_region = px.bar(
        region_sales, 
        y='Region', 
        x='Sales', 
        orientation='h',
        color='Region',
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={'Region': 'Region', 'Sales': 'Total Sales ($)'}
    )
    fig_region.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_region, use_container_width=True)

st.markdown("---")

# 7. Analisis & Wawasan / Storytelling (Elemen 5 Rubrik UTS)
st.subheader("💡 Analisis & Wawasan Utama (Key Business Insights)")
st.info("""
 Berdasarkan hasil olah data visualisasi pada dataset Superstore Sales:
1. **Dominasi Kategori & Sub-Kategori**: Kategori **Technology** dan sub-kategori **Phones** serta **Chairs** menjadi kontributor penjualan terbesar. Hal ini menunjukkan permintaan tinggi pada produk perlengkapan kantor modern.
2. **Segmen Pasar Konsumen Utama**: Segmen **Consumer** menyumbang lebih dari **50%** dari total nilai penjualan dibanding segmen Corporate dan Home Office.
3. **Performa Wilayah (Region)**: Region **West** menduduki peringkat pertama dalam menghasilkan akumulasi pendapatan penjualan, diikuti oleh region East.
4. **Tren Pertumbuhan**: Tren penjualan menunjukkan pola musiman (*seasonality*) dengan lonjakan transaksi yang signifikan pada kuartal akhir (Q4) di setiap tahunnya.
""")