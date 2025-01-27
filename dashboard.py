# Import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset dari folder 'Bike Sharing Dataset'
day = pd.read_csv('day.csv')

# Data Wrangling
# Menambahkan kolom 'temp_celsius'
day['temp_celsius'] = day['temp'] * 41

# Fungsi untuk menghitung rata-rata penyewaan sepeda berdasarkan kondisi tertentu
def calculate_average_rentals(df, group_by_col):
    return df.groupby(group_by_col)['cnt'].mean().reset_index()

# Layout Streamlit
# Menghapus parameter yang menyebabkan error
st.sidebar.image('logo.png')

home = st.sidebar.button("Home")
lihat_dataset = st.sidebar.button("Lihat Dataset")
pengaruh_musim = st.sidebar.button("Pengaruh Musim")
hari_kerja_vs_akhir_pekan = st.sidebar.button("Hari Kerja vs Akhir Pekan")
pengaruh_cuaca = st.sidebar.button("Pengaruh Cuaca")
pengaruh_suhu = st.sidebar.button("Pengaruh Suhu")
tren_musiman = st.sidebar.button("Tren Musiman")

# Menambahkan styling untuk tombol dan kartu metrik menggunakan CSS
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #00588E !important;
        color: white !important;
    }
    
    .metric {
        background-color: #00588E !important;
        border-left-color: #00588E !important;
        padding: 20px !important;
        border-radius: 8px !important;
        text-align: center !important;
        color: white !important;
        font-size: 18px !important;
        height: 100px !important;  /* Mengurangi tinggi card */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .metric h3 {
        font-size: 12px !important;
        margin-bottom: 2px !important;
        color: white !important;
    }

    .metric p {
        font-size: 24px !important;
        margin: 0 !important;
        font-weight: bold !important;
        line-height: 1.2;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Menentukan halaman mana yang harus ditampilkan
page = "Home"
if 'page' not in st.session_state:
    st.session_state.page = page

if home:
    st.session_state.page = "Home"
elif lihat_dataset:
    st.session_state.page = "Lihat Dataset"
elif pengaruh_musim:
    st.session_state.page = "Pengaruh Musim"
elif hari_kerja_vs_akhir_pekan:
    st.session_state.page = "Hari Kerja vs Akhir Pekan"
elif pengaruh_cuaca:
    st.session_state.page = "Pengaruh Cuaca"
elif pengaruh_suhu:
    st.session_state.page = "Pengaruh Suhu"
elif tren_musiman:
    st.session_state.page = "Tren Musiman"

page = st.session_state.page

if page == "Home":
    st.title('Dashboard Analisis Data Bike Sharing')
    st.markdown("""
    Proyek Analisis Data: Bike Sharing Dataset  
    **Nama:** Dea Reigina  
    **Email:** deareigina05@gmail.com  
    **ID Dicoding:** deareignn  
    """)

    # Menghitung beberapa metrik utama
    total_rentals = day['cnt'].sum()
    avg_rentals = day['cnt'].mean()
    median_rentals = day['cnt'].median()
    mode_rentals = day['cnt'].mode()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="metric"><h3>Total Rentals</h3><p>{total_rentals:,}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric"><h3>Average Rentals</h3><p>{avg_rentals:,.2f}</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric"><h3>Median Rentals</h3><p>{median_rentals:,.2f}</p></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric"><h3>Mode Rentals</h3><p>{mode_rentals:,}</p></div>', unsafe_allow_html=True)

    # Visualisasi tren penyewaan sepeda harian
    st.subheader('Tren Penyewaan Sepeda Harian')
    daily_trend = day.set_index('dteday')['cnt']
    st.line_chart(daily_trend)

elif page == "Lihat Dataset":
    st.title('Lihat Dataset')
    st.markdown('### Dataset day.csv')
    st.write(day.head())
    st.markdown('### Statistik Deskriptif day.csv')
    st.write(day.describe())

elif page == "Pengaruh Musim":
    st.title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
    season_counts = calculate_average_rentals(day, 'season')
    st.bar_chart(season_counts.set_index('season'))
    st.markdown("""
    **Kesimpulan:**  
    Dari visualisasi bar plot, kita dapat melihat bahwa jumlah penyewaan sepeda bervariasi tergantung musim. Musim ketiga memiliki rata-rata jumlah penyewaan tertinggi, diikuti oleh musim kedua, musim keempat, dan musim pertama. Ini menunjukkan bahwa pola sewa sepeda sangat dipengaruhi oleh musim.
    """)

elif page == "Hari Kerja vs Akhir Pekan":
    st.title('Perbedaan Jumlah Penyewaan Sepeda Antara Hari Kerja dan Akhir Pekan')
    workingday_counts = calculate_average_rentals(day, 'workingday')
    st.bar_chart(workingday_counts.set_index('workingday'))
    st.markdown("""
    **Kesimpulan:**  
    Visualisasi menunjukkan bahwa ada perbedaan jumlah penyewaan sepeda antara hari kerja dan akhir pekan. Pada hari kerja, jumlah penyewaan sepeda cenderung sedikit lebih rendah dibandingkan dengan akhir pekan. Ini mungkin disebabkan oleh aktivitas rekreasi yang lebih banyak dilakukan pada akhir pekan.
    """)

elif page == "Pengaruh Cuaca":
    st.title('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='weathersit', y='cnt', data=day)
    plt.title('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan:**  
    Dari box plot yang menunjukkan pengaruh cuaca terhadap jumlah penyewaan sepeda, kita dapat melihat bahwa kondisi cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Kondisi cuaca yang lebih baik (seperti langit cerah) cenderung meningkatkan jumlah penyewaan sepeda, sementara cuaca buruk (seperti hujan) dapat menurunkan jumlah penyewaan sepeda. Ini menunjukkan bahwa penyewa lebih cenderung menggunakan sepeda pada hari-hari dengan kondisi cuaca yang baik.
    """)

elif page == "Pengaruh Suhu":
    st.title('Pengaruh Suhu Harian Terhadap Jumlah Penyewaan Sepeda')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp_celsius', y='cnt', data=day)
    plt.title('Pengaruh Suhu Harian Terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Suhu (Celsius)')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan:**  
    Dari scatter plot dan visualisasi lainnya, kita dapat melihat bahwa suhu harian memiliki hubungan dengan jumlah penyewaan sepeda. Suhu yang lebih nyaman cenderung meningkatkan jumlah penyewaan sepeda. Terlalu panas atau terlalu dingin dapat mengurangi jumlah penyewaan sepeda.
    """)

elif page == "Tren Musiman":
    st.title('Tren Musiman Penyewaan Sepeda Selama Dua Tahun Terakhir')
    day['yr_season'] = day['yr'].astype(str) + '-' + day['season'].astype(str)
    season_trend = calculate_average_rentals(day, 'yr_season')
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='yr_season', y='cnt', data=season_trend)
    plt.title('Tren Musiman Penyewaan Sepeda (2011-2012)')
    plt.xlabel('Tahun-Musim')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    st.markdown("""

   **Kesimpulan:**  
    Berdasarkan gambar, jumlah penyewaan sepeda meningkat secara signifikan pada musim ketiga tahun 2011 (0-3) dan musim kedua tahun 2012 (1-2), mencapai puncaknya pada musim ketiga tahun 2012 (1-3). Ini menunjukkan bahwa ada pola musiman yang konsisten dalam penyewaan sepeda, dengan puncak penyewaan terjadi pada musim-musim tersebut.
    """)
