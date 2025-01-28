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

# Pemetaan nilai numerik ke label
day['season'] = day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day['weathersit'] = day['weathersit'].map({
    1: 'Clear or Partly Cloudy',
    2: 'Mist or Cloudy',
    3: 'Light Snow or Rain',
    4: 'Heavy Rain or Snow'
})
day['workingday'] = day['workingday'].map({0: 'Weekend', 1: 'Working Day'})
day['yr'] = day['yr'].map({0: '2011', 1: '2012'})

# Menambahkan kolom 'yr_season'
day['yr_season'] = day['yr'].astype(str) + '-' + day['season']

# Fungsi untuk menghitung rata-rata penyewaan sepeda berdasarkan kondisi tertentu
def calculate_average_rentals(df, group_by_col):
    return df.groupby(group_by_col)['cnt'].mean().reset_index()

# Layout Streamlit
st.sidebar.image('logo.png', use_column_width=True)

# Navigasi menggunakan selectbox
page = st.sidebar.selectbox("Pilih Halaman", ["Home", "Lihat Dataset", "Pengaruh Musim", "Hari Kerja vs Akhir Pekan", "Pengaruh Cuaca", "Pengaruh Suhu", "Tren Musiman"])

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
    selected_season = st.sidebar.multiselect("Pilih Musim", options=day['season'].unique(), default=day['season'].unique())
    filtered_day = day[day['season'].isin(selected_season)]
    season_counts = calculate_average_rentals(filtered_day, 'season')
    st.bar_chart(season_counts.set_index('season'))
    st.markdown("""
    **Kesimpulan:**  
    Dari analisis data, musim memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda harian. Musim gugur memiliki rata-rata jumlah penyewaan sepeda harian tertinggi sekitar 5644.3 penyewaan per hari, diikuti oleh musim panas dengan rata-rata sekitar 4992.33 penyewaan per hari, kemudian musim dingin dengan rata-rata sekitar 4728.16 penyewaan per hari, dan yang terendah adalah musim semi dengan rata-rata sekitar 2604.13 penyewaan per hari. Untuk meningkatkan sistem penyewaan sepeda, disarankan untuk meningkatkan ketersediaan sepeda dan layanan selama musim gugur dan panas, serta melakukan promosi atau diskon selama musim semi untuk meningkatkan jumlah penyewaan.
    """)

elif page == "Hari Kerja vs Akhir Pekan":
    st.title('Perbedaan Jumlah Penyewaan Sepeda Antara Hari Kerja dan Akhir Pekan')
    selected_workingday = st.sidebar.multiselect("Pilih Hari", options=day['workingday'].unique(), default=day['workingday'].unique())
    filtered_day = day[day['workingday'].isin(selected_workingday)]
    workingday_counts = calculate_average_rentals(filtered_day, 'workingday')
    st.bar_chart(workingday_counts.set_index('workingday'))
    st.markdown("""
    **Kesimpulan:**  
    Berdasarkan analisis data, terdapat perbedaan dalam jumlah penyewaan sepeda antara hari kerja dan akhir pekan. Pada akhir pekan, rata-rata jumlah penyewaan sepeda harian adalah sekitar 4330.17 penyewaan per hari, sementara pada hari kerja rata-rata jumlah penyewaan sepeda harian adalah sekitar 4584.82 penyewaan per hari. Meski perbedaannya tidak signifikan, jumlah penyewaan sedikit lebih tinggi pada hari kerja. Untuk meningkatkan sistem penyewaan sepeda, penyedia layanan dapat menawarkan promosi spesial di akhir pekan guna meningkatkan jumlah penyewaan dan memastikan ketersediaan serta perawatan sepeda yang memadai pada hari kerja. Program loyalitas dan analisis waktu sewa puncak juga dapat membantu dalam meningkatkan efisiensi operasional, kepuasan pelanggan, dan potensi peningkatan pendapatan.
    """)

elif page == "Pengaruh Cuaca":
    st.title('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
    selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=day['weathersit'].unique(), default=day['weathersit'].unique())
    filtered_day = day[day['weathersit'].isin(selected_weather)]
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='weathersit', y='cnt', data=filtered_day)
    plt.title('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan:**  
    Berdasarkan analisis data, kondisi cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda setiap hari. Visualisasi menunjukkan bahwa jumlah penyewaan sepeda tertinggi terjadi pada kondisi cuaca yang cerah atau sebagian berawan dengan rata-rata penyewaan sepeda harian tertinggi, diikuti oleh kondisi cuaca berkabut atau berawan, dan terendah pada kondisi cuaca dengan salju atau hujan ringan. Dalam konteks ini, untuk meningkatkan sistem penyewaan sepeda, disarankan agar penyedia layanan meningkatkan promosi dan penawaran khusus pada hari-hari dengan cuaca baik untuk memaksimalkan jumlah penyewaan. Selain itu, penyedia juga dapat menawarkan perlengkapan cuaca seperti jas hujan atau penutup sepeda pada hari-hari dengan cuaca kurang mendukung untuk menjaga kenyamanan dan keamanan pengguna, yang pada gilirannya dapat meningkatkan kepuasan pelanggan dan potensi pendapatan.
    """)


elif page == "Pengaruh Suhu":
    st.title('Pengaruh Suhu Harian Terhadap Jumlah Penyewaan Sepeda')
    selected_temp_range = st.sidebar.slider('Pilih Rentang Suhu (Celsius)', min_value=float(day['temp_celsius'].min()), max_value=float(day['temp_celsius'].max()), value=(float(day['temp_celsius'].min()), float(day['temp_celsius'].max())))
    filtered_day = day[(day['temp_celsius'] >= selected_temp_range[0]) & (day['temp_celsius'] <= selected_temp_range[1])]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp_celsius', y='cnt', data=filtered_day)
    plt.title('Pengaruh Suhu Harian Terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Suhu (Celsius)')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan:**  
    Berdasarkan analisis data, perbedaan rata-rata suhu harian memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Pada suhu antara 2.391 dan 5.715 derajat Celsius, rata-rata jumlah penyewaan sepeda harian sekitar 1386.71 penyewaan per hari. Ketika suhu meningkat ke rentang 5.715 hingga 9.005 derajat Celsius, rata-rata jumlah penyewaan juga meningkat menjadi sekitar 1607.03 penyewaan per hari. Tren ini terus naik hingga mencapai puncaknya pada rentang suhu 22.167 hingga 25.457 derajat Celsius dengan rata-rata 5823.84 penyewaan per hari. Namun, setelah suhu melebihi 25.457 derajat Celsius, jumlah penyewaan mulai sedikit menurun, meski tetap berada di angka tinggi, seperti pada suhu antara 28.748 dan 32.038 derajat Celsius yang memiliki rata-rata 5773.91 penyewaan per hari. Dari hasil ini, disarankan agar penyedia layanan meningkatkan ketersediaan sepeda pada hari-hari dengan suhu tinggi untuk memaksimalkan pendapatan. Selain itu, promosi atau diskon pada hari-hari dengan suhu rendah dapat membantu mendorong lebih banyak orang menyewa sepeda. Implementasi strategi operasional dan pemasaran yang lebih efektif berdasarkan suhu harian akan meningkatkan efisiensi operasional, kepuasan pelanggan, dan potensi peningkatan pendapatan.
    """)

elif page == "Tren Musiman":
    st.title('Tren Musiman Penyewaan Sepeda Selama Dua Tahun Terakhir')
    selected_year = st.sidebar.multiselect("Pilih Tahun", options=day['yr'].unique(), default=day['yr'].unique())
    filtered_day = day[day['yr'].isin(selected_year)]
    season_trend = calculate_average_rentals(filtered_day, 'yr_season')
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='yr_season', y='cnt', data=season_trend)
    plt.title('Tren Musiman Penyewaan Sepeda (2011-2012)')
    plt.xlabel('Tahun-Musim')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    st.markdown("""
    **Kesimpulan:**  
    Berdasarkan analisis data, terdapat tren musiman dalam penyewaan sepeda selama dua tahun terakhir. Pada tahun pertama, rata-rata jumlah penyewaan sepeda harian tertinggi terjadi pada musim gugur (Fall) dengan sekitar 4464.36 penyewaan per hari, sedangkan terendah terjadi pada musim semi (Spring) dengan sekitar 1666.67 penyewaan per hari. Pada tahun kedua, tren yang sama terlihat dengan musim gugur mencapai puncaknya pada sekitar 6824.24 penyewaan per hari, sementara musim semi tetap yang terendah dengan sekitar 3531.3 penyewaan per hari. Selain itu, musim panas (Summer) menunjukkan peningkatan signifikan dengan rata-rata 3775.17 penyewaan per hari pada tahun pertama dan 6209.49 pada tahun kedua, sementara musim dingin (Winter) juga mengalami peningkatan dari 3664.46 menjadi 5791.87 penyewaan per hari. Berdasarkan analisis ini, disarankan untuk meningkatkan ketersediaan sepeda dan melakukan promosi khusus pada musim gugur dan musim panas untuk memaksimalkan pendapatan, serta meningkatkan efisiensi operasional dengan penjadwalan perawatan sepeda pada musim semi yang memiliki permintaan lebih rendah. Implementasi strategi ini dapat membantu meningkatkan kepuasan pelanggan dan potensi peningkatan pendapatan bagi sistem penyewaan sepeda.
    """)
