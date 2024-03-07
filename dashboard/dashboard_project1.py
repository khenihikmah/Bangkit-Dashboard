import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import streamlit as st

## df Wrangling

st.title("Bike Sharing Dataset (Day)")
st.write(
    """
    Nama: [Kheni Hikmah Lestari]
    """
    )
st.write(
    """
    Email: [m001d4kx1593@bangkit.academy]
    """
    )
st.write(
    """
    ID Dicoding: [khenihikmah130303]
    """
    )
st.header('Gathering df')
data = pd.read_csv(r"https://raw.githubusercontent.com/khenihikmah/Bangkit-Dashboard/master/dashboard/day.csv")


## Pada musim apa total sewa sepeda paling banyak dan paling sedikit
# Mengganti nilai dalam kolom 'season' dengan label yang sesuai
data['season'] = data['season'].replace({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
# Visualisasi dengan Altair
def rental_by_season():
    season_counts = data.groupby('season')['cnt'].sum().reset_index()
    max_season = season_counts.loc[season_counts['cnt'].idxmax()]
    min_season = season_counts.loc[season_counts['cnt'].idxmin()]

# Konfigurasi ukuran font
    text_font_size = 20

    chart = alt.Chart(season_counts).mark_bar().encode(
        x=alt.X('season:N', axis=alt.Axis(labelFontSize=text_font_size)),  
        y=alt.Y('cnt:Q', axis=alt.Axis(labelFontSize=text_font_size)),     
        color=alt.condition(
            alt.datum.season == max_season['season'],
            alt.value('steelblue'),
            alt.value('lightsteelblue')
        ),
        tooltip=['season', 'cnt']
    ).properties(
        width=1000,
        height=800,
        title={
            "text": "Total Sewa Sepeda berdasarkan Musim",
            "fontSize": text_font_size + 9  # Atur ukuran font untuk judul  
        }
    
    )

    # Tampilkan gambar di Streamlit
    st.altair_chart(chart, use_container_width=True)
    st.write(f"Musim dengan total sewa sepeda paling banyak: {max_season['season']}")
    st.write(f"Musim dengan total sewa sepeda paling sedikit: {min_season['season']}")


## Bagaimana total sewa sepeda pada saat holiday/weekend serta pada hari kerja  
# Mengganti nilai dalam kolom 'season' dengan label yang sesuai
data['workingday'] = data['workingday'].replace({1: 'Weekend/Holiday', 0: 'Lainnya'})

def rental_by_workingday():
    workingday_counts = data.groupby('workingday')['cnt'].sum().reset_index()
    max_workingday = workingday_counts.loc[workingday_counts['cnt'].idxmax()]
    min_workingday = workingday_counts.loc[workingday_counts['cnt'].idxmin()]

# Konfigurasi ukuran font
    text_font_size = 20

    chart = alt.Chart(workingday_counts).mark_bar().encode(
        x=alt.X('workingday:N', axis=alt.Axis(labelFontSize=text_font_size)),  
        y=alt.Y('cnt:Q', axis=alt.Axis(labelFontSize=text_font_size)),     
        color=alt.condition(
            alt.datum.season == max_workingday['workingday'],
            alt.value('steelblue'),
            alt.value('powderblue')
        ),
        tooltip=['workingday', 'cnt']
    ).properties(
        width=1000,
        height=800,
        title={
            "text": "Total Sewa Sepeda berdasarkan Workingday",
            "fontSize": text_font_size + 9  # Atur ukuran font untuk judul  
        }
    
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Total sewa sepeda pada hari kerja:", workingday_counts.loc[workingday_counts['workingday'] == 'Lainnya', 'cnt'].iloc[0])
    st.write("Total sewa sepeda pada weekend/holiday:", workingday_counts.loc[workingday_counts['workingday'] == 'Weekend/Holiday', 'cnt'].iloc[0])



# Menghitung rata-rata temp, hum, dan windspeed berdasarkan musim
def calculate_seasonal_averages():
    seasonal_averages = data.groupby('season').agg({
    "temp": lambda x: x.mean() * 41,
    "hum": lambda x: x.mean() * 100,
    "windspeed": lambda x: x.mean() * 67
    }).reset_index()
    seasonal_averages['temp'] = seasonal_averages['temp'].round(2)  # Pembulatan nilai rata-rata
    seasonal_averages['hum'] = seasonal_averages['hum'].round(2)    # Pembulatan nilai rata-rata
    seasonal_averages['windspeed'] = seasonal_averages['windspeed'].round(2)  # Pembulatan nilai rata-rata
    return seasonal_averages

def display_seasonal_averages():
    st.subheader('Informasi Rata-Rata Temperatur, Humidity dan Windspeed')
    seasonal_averages = calculate_seasonal_averages()
    st.dataframe(seasonal_averages, width=800)  # Mengatur lebar tabel menjadi 800 piksel


# Main
def main():
    st.title('🚲Dashboard Sewa Sepeda🚲')
    st.write("Dashboard ini menampilkan informasi tentang sewa sepeda berdasarkan season dan workingday serta rata-rata temperatur, humidity dan windspeed pada setiap musim")

    # Total rental berdasakan musim
    rental_by_season()
    st.write("\n")
    st.write("\n")
    st.write("\n")

    # Total rental berdasarkan workingday
    rental_by_workingday()
    st.write("\n")
    st.write("\n")
    st.write("\n")

    # Menampilkan tabel antara season, rata-rata temp, rata-rata hum, rata-rata windspeed di dashboard
    display_seasonal_averages()
    st.write("\n")
    st.write("\n")
    st.write("\n")
    
    # Kesimpulan
    st.header("Kesimpulan")
    st.write("Pada season fall orang paling banyak menyewa sepeda, hal ini dapat disebabkan karena beberapa faktor diantaranya yaitu suhu yang sejuk (tidak terlalu panas atau terlalu dingin) rata-rata berkisar sekitar 28.9°C, lalu kelembapan udara yang nyaman dengan rata-rata berkisar 63.3, serta kecepatan angin yang menyegarkan (tidak terlalu kencang) dengan rata-rata berkisar 11.53 km/jam.")
    st.write("Jumlah total sepeda sewaan termasuk casual dan registered paling banyak terdapat pada saat weekend/holiday, hal ini mungkin dikarenakan pada saat weekend/holiday seringkali menjadi waktu luang bagi banyak orang. Orang-orang cenderung memiliki lebih banyak waktu untuk melakukan aktivitas rekreasi atau bersantai, termasuk bersepeda.")
if __name__ == "__main__":
    main()
