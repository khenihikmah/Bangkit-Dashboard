import streamlit as st
import altair as alt
import pandas as pd

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
data = pd.read_csv('https://raw.githubusercontent.com/khenihikmah/Bangkit-Dashboard/master/Data/day.csv')

## PT Kheni Mandiri merupakan suatu PT yang menyediakan jasa sewa sepeda untuk masyarakat di sekitar kampus IPB University. PT Kheni Mandiri ingin mengetahui season apa yang total sewa sepeda miliknya paling banyak dan paling sedikit. Hal ini dapat digunakan untuk evaluasi PT kedepannya. Dan memberikan strategi pengembangan bisnisnya agar lebih sukses.
data['season'] = data['season'].replace({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
def rental_by_season():
    season_cnt = data.groupby('season')['cnt'].sum().reset_index()
    max_season = season_cnt.loc[season_cnt['cnt'].idxmax()]
    min_season = season_cnt.loc[season_cnt['cnt'].idxmin()]

    text_font_size = 20

    chart = alt.Chart(season_cnt).mark_bar().encode(
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
            "text": "Total Sewa Sepeda PT Kheni Mandiri berdasarkan Season",
            "fontSize": text_font_size + 9  
        }
    
    )
    st.altair_chart(chart, use_container_width=True)
    st.write(f"Total Sewa Paling Banyak Musim: {max_season['season']}")
    st.write(f"Total Sewa Paling Sedikit Musim: {min_season['season']}")


## Setelah mengetahui season yang memiliki total paling banyak, PT Kheni Mandiri ingin mengetahui bagaimana total sewa sepeda pada saat holiday/weekend serta pada hari kerja? Apakah ada perbedaan? Apakah Lebih banyak penyewaan sepeda pada saat holiday atau pada saat weekend.
data['workingday'] = data['workingday'].replace({1: 'Weekend/Holiday', 0: 'Lainnya'})

def rental_by_workingday():
    workingday_cnt = data.groupby('workingday')['cnt'].sum().reset_index()
    max_workingday = workingday_cnt.loc[workingday_cnt['cnt'].idxmax()]
    min_workingday = workingday_cnt.loc[workingday_cnt['cnt'].idxmin()]

    text_font_size = 20

    chart = alt.Chart(workingday_cnt).mark_bar().encode(
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
            "fontSize": text_font_size + 9  
        }
    
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Total sewa sepeda pada hari kerja:", workingday_cnt.loc[workingday_cnt['workingday'] == 'Lainnya', 'cnt'].iloc[0])
    st.write("Total sewa sepeda pada weekend/holiday:", workingday_cnt.loc[workingday_cnt['workingday'] == 'Weekend/Holiday', 'cnt'].iloc[0])


# Rata-rata temp, hum, dan windspeed 
def calculate_seasonal_avrg():
    seasonal_avrg = data.groupby('season').agg({
    "temp": lambda x: x.mean() * 41,
    "hum": lambda x: x.mean() * 100,
    "windspeed": lambda x: x.mean() * 67
    }).reset_index()
    seasonal_avrg['temp'] = seasonal_avrg['temp'].round(2)  
    seasonal_avrg['hum'] = seasonal_avrg['hum'].round(2)   
    seasonal_avrg['windspeed'] = seasonal_avrg['windspeed'].round(2)  
    return seasonal_avrg

def display_seasonal_avrg():
    st.subheader('Rata-Rata Temperatur, Humidity dan Windspeed')
    seasonal_avrg = calculate_seasonal_avrg()
    st.dataframe(seasonal_avrg, width=800)  

# Main
def main():
    st.title('Dashboard Sewa Sepeda PT Kheni Mandiri')
    
    # Berdasakan musim
    rental_by_season()
    st.write("\n")
    st.write("\n")
    st.write("\n")

    # Berdasarkan Workingday
    rental_by_workingday()
    st.write("\n")
    st.write("\n")
    st.write("\n")

    # Season, rata-rata temp, rata-rata hum, rata-rata windspeed 
    display_seasonal_avrg()
    st.write("\n")
    st.write("\n")
    st.write("\n")
    
    # Conclution
    st.header("Conclution")
    st.write("Jumlah total sepeda sewaan termasuk casual dan registered paling banyak terjadi ***season fall***, dan paling sedikit terjadi ***season springer***. Season fall menjadi musim dengan pengguna sepeda paling tinggi diantaean season springer karena masyarakat IPB University merasa nyaman untuk bersepeda dengan suhu udara yang sejuk disertai dengan cuaca yang lebih stabil untuk menikmati alam sekitar. PT Kheni Mandiri diharapkan mampu menyediakan sepeda yang banyak untuk antisipasi adanya kenaikan penyewa sepeda. ")
    st.write("Jumlah pengguna biasa (casual), jumlah pengguna terdaftar (registered), dan jumlah total sepeda sewaan termasuk casual dan registered paling banyak terjadi saat weekend/holiday. Hal ini terjadi karena weekeen/holiday masyarakat lebih suka menikmati harinya dengan berkeliling di area Kampus. Baik itu mahasiswa ataupun masyarakat setempat. Hampir 2 kali lipat perbandingan penyewa sepeda saat weekend dan saat jam kerja. Karena mungkin saat jam kerja masyarakat lebih memilih menggunakan sepeda motor atau ojek online untuk mengantarnya ke tempat tujuan daripada bersepeda. PT Kheni Mandiri dapat menyusun strategi yang bagus untuk mendapatkan hasil yang optimal dari penyewaan sepeda pada saat weekend/holiday.")
if __name__ == "__main__":
    main()
