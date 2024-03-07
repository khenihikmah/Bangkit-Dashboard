import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import streamlit as st

## df Wrangling

st.title("Air Quality in Tiantan")
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
st.write(
    """"
    Air Quality mengacu pada tingkat kebersihan dan kemurnian udara di suatu wilayah atau lokasi tertentu. 
    Kualitas udara dipengaruhi oleh sejumlah parameter dan polutan udara, seperti partikulat matter (PM), 
    nitrogen dioksida (NO2), sulfur dioksida (SO2), karbon monoksida (CO), ozon (O3), dan lainnya. Pengukuran
    kualitas udara umumnya dilakukan untuk memantau tingkat polusi dan memastikan keamanan serta kesehatan masyarakat.
    """
)
st.write(
    """"
    Dashboard Air Quality dapat menyajikan informasi ini dalam format visual yang mudah dimengerti. Hal ini dapat 
    mencakup pemantauan terhadap tingkat polutan tertentu, perubahan seiring waktu, dan pembandingan dengan standar 
    kebersihan udara yang ditetapkan oleh lembaga pemerintah atau organisasi lingkungan. Dashboard semacam itu membantu
    masyarakat dan pemangku kepentingan lainnya untuk memahami dan mengambil tindakan terkait kualitas udara di suatu daerah.
    """
)
st.header('Gathering df')
df_1 = pd.read_csv(r"https://raw.githubusercontent.com/khenihikmah/Bangkit-Dashboard/master/dashboard/DataTiantan.csv")
df_1
df = df_1.dropna()

st.header("Air Quality Dashboard in Tiantan")
tahun = st.selectbox(        
    label = 'Choose The Year',
    options = (2013,2014,2015,2016,2017)
    )
st.write('Pilih: ', tahun)

st.header('Create_PM10_Tabel')
def create_PM10_tabel(df):
    PM10_per_tahun = df[df['year'] == tahun]
    PM10_tabel = PM10_per_tahun.groupby(by=['month']).agg({
        "PM10":'median'
    })
    return PM10_tabel
st.table(create_PM10_tabel(df))

st.header('Create_O3_Tabel')
def create_O3_tabel(df):
    O3_per_tahun = df[df['year'] == tahun]
    O3_tabel = O3_per_tahun[['O3','hour']].groupby(['hour']).median()
    return O3_tabel

# Create three columns
st.table(create_PM10_tabel(df))
st.table(create_O3_tabel(df).sort_values(by="O3"))


#create_O3_tabel
def create_O3_tabel(df):
    O3_per_tahun = df[df['year'] == tahun]
    O3_tabel = O3_per_tahun[['O3','hour']].groupby(['hour']).median()
    return O3_tabel

st.header('Melihat O3 di tiap Bulannya')
fig, ax = plt.subplots(figsize=(12, 6))
plt.style.use('ggplot')
ax.plot(
    create_PM10_tabel(df_1),
    marker='o', 
    linewidth=4,
    color="#D37676"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title(("O3 per Month in " + str(tahun)))
ax.set_xlabel("Months")
ax.set_ylabel("O3")
ax.set_ylim(0,1000)
st.pyplot(fig)


st.header('Melihat Median Jumlah O3 per Jam pada tahun tertentu')
col1, col2= st.columns(2)

with col1:
    st.table(create_O3_tabel(df))

with col2:
    st.table(create_O3_tabel(df).sort_values(by="O3"))

#membuat chart informasi O3 per hour
fig, ax = plt.subplots(figsize=(12, 6))
plt.style.use('ggplot')
ax.plot(
    create_O3_tabel(df),
    marker='o', 
    linewidth=4,
    color="#D37676"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title(("Median " + str(tahun)))
ax.set_xlabel("Jam")
ax.set_ylabel("O3")
ax.set_xlim(0,100)
ax.set_ylim(10, 100)

st.pyplot(fig)
