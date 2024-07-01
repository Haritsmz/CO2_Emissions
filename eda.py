import streamlit as st
import pandas as pd
from PIL import Image
import requests
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import f_oneway
import joblib

def run():
    st.markdown("<h1 style='text-align: center;'>Pengaruh Jenis Bahan Bakar Terhadap Emisi CO2</h1>", unsafe_allow_html=True)
    st.header('\n')
    st.subheader('Analisis Perbandingan Bahan Bakar Regular Gasoline, Premium Gasoline, Diesel and Ethanol')
    st.write('by :  Harits Mughni Zakinu')
    st.caption('E-mail : haritsmzakinu@gmail.com')
    # Load Data
    with open('CO2_Emissions_clean.pkl', 'rb') as file_1:
        CO2_Emissions_clean= joblib.load(file_1)

    
    image = Image.open(requests.get('https://www.frost.com/wp-content/uploads/2022/06/GettyImages-1294597903-1.jpg', stream=True).raw)
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(image)    
 
    st.write('''Perubahan iklim global dan masalah lingkungan semakin menjadi perhatian utama di seluruh dunia. Salah satu kontributor utama 
                terhadap perubahan iklim adalah emisi gas rumah kaca, termasuk emisi karbon dioksida (CO2) yang dihasilkan oleh sektor transportasi. 
                Transportasi adalah sektor yang memiliki ketergantungan paling tinggi pada bahan bakar fosil yang mengakibatkan emisi karbon dioksida (CO2) dibandingkan sektor lainnya,
                pada tahun 2021 menurut **_International Energy Agency_** (_IEA_) sektor transportasi menyumbang sekitar **37%** dari total emisi CO2.
                Sebuah studi terbaru dari **_International Energy Agency_** (_IEA_) menunjukkan bahwa Kanada merupakan salah satu negara yang paling banyak menyumbang Emisi karbon dioksida yang berasal dari transportasi dengan total **206 g/km** pada tahun 2021 ([National Observer](https://www.nationalobserver.com/2019/09/04/analysis/canadian-cars-are-worlds-dirtiest-ev-age-essential)).
                Seiring dengan peningkatan jumlah kendaraan, menjadi sebuah tantangan bagi generasi saat ini terutama di Kanada agar dapat menurunkan tingkat emisi CO2. selain itu penting untuk memahami dampak jenis bahan bakar yang digunakan terhadap emisi CO2. Dalam industri otomotif,terdapat beberapa jenis bahan bakar yang umum digunakan, 
                termasuk reguler gasoline, premium gasoline, diesel, dan ethanol. Setiap jenis bahan bakar memiliki karakteristik yang berbeda dan dapat mempengaruhi tingkat emisi CO2 yang dihasilkan oleh kendaraan. 
                Dalam konteks ini, perlu analisis perbandingan antara jenis bahan bakar ini dapat memberikan wawasan yang berharga tentang dampak lingkungan yang dihasilkan oleh masing-masing jenis bahan bakar.''')
    st.header('\n')

    st.header('Dataset CO2 Emissions')
    st.dataframe(CO2_Emissions_clean)
    st.caption("Data Source: The data has been taken and compiled from the [Canada Goverment](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64#wb-auto-6) official link ")
    st.header('\n')

    total,year= st.columns(2)

    # Visualisasi brand
    table_brand1, table_brand2 = st.columns([1,1])
    st.header('\n')
   
    with table_brand1: 
        st.subheader('Top 10 Brand Mobil yang paling banyak digunakan')
        make_count = CO2_Emissions_clean['Make'].value_counts().head(10)
        label_brand = make_count.index.tolist()
        values_brand = make_count.values.tolist()
        fig_make = px.pie(names=label_brand,
                          values= values_brand,
                          color_discrete_sequence=px.colors.sequential.RdBu,
                          title='Brand Mobil',)
        fig_make.update_traces(textposition='inside', texttemplate='%{label} (%{value}) ')
    
        st.plotly_chart(fig_make)
        st.write('''Data menampilkan jumlah kendaraan berdasarkan Brand dan kuantitasnya. Dalam gambar diatas, terdapat beberapa merek kendaraan populer.
                    **Chevrolet** menjadi Brand mobil yang paling populer dengan jumlah pemakaian sebanyak 61 diikuti dengan **Porsche** 59, **Toyota** 54, **Ford** dan lain-lain''')
    

    with table_brand2: 
        st.subheader('Bahan bakar yang paling banyak digunakan')
        fuel_count = CO2_Emissions_clean['Fuel type'].value_counts()
        label_fuel = fuel_count.index.tolist()
        values_fuel = fuel_count.values.tolist()
        fig_fuel = px.pie(names=label_fuel,
                          values= values_fuel,
                          color_discrete_sequence=px.colors.sequential.Oranges,
                          title='Jenis Bahan Bakar',)
        fig_fuel.update_traces(textposition='inside', texttemplate='%{label} (%{value}) ')

        st.plotly_chart(fig_fuel)
        st.write('''Jika kita lihat dari jumlah pemakaian jenis bahan. Pemakaian jenis Gasoline sangat mendominasi seperti **Premium Gasoline** sebanyak 409 dan **Regular Gasoline** 331
        diikuti dengan **Diesel** 18 pemakaian dan **Ethanol** yang hanya 6 pemakaian''')
    
    
    st.header('Hubungan antara Jenis Bahan bakar, Banyaknya Konsumsi Bahan Bakar dan Kapasitas Mesin Terhadap Emisi CO2')
    table_fuel1, table_fuel2 = st.columns([1,1])
    st.header('\n')
   
    
    with table_fuel1: 
        st.subheader('Top 5 brand mobil yang menghasilkan Emisi CO2 paling banyak')
        top5_brand = CO2_Emissions_clean.groupby(CO2_Emissions_clean['Make'])[['CO2 emissions (g/km)']].mean().sort_values(by='CO2 emissions (g/km)', ascending=False).head(5)

        fig = px.bar(top5_brand, x=top5_brand.index, 
                    y='CO2 emissions (g/km)', 
                    color='CO2 emissions (g/km)', 
                    labels={'CO2 emissions (g/km)': 'Emisi CO2'},
                    title='Rata-Rata Emisi CO2 per Brand',
                    color_continuous_scale='oranges')
    
        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')
    
        st.plotly_chart(fig)
        st.write('''Diatas merupakan gambar dari 5 brand yang paling banyak menghasilkan emisi karbon dioksida.
                    **Bugatti** merupakan brand mobil yang paling banyak menyumbang emisi gas karbon dioksida dengan rataan sebesar **608 g/km**
                    diikuti dengan **Rolls-Royce, Ferrari, Lamborghini dan Bentley**''')
    
    with table_fuel2: 
        st.subheader('Bahan bakar yang menghasilkan Emisi CO2 paling banyak')
        fuel = CO2_Emissions_clean.groupby(CO2_Emissions_clean['Fuel type'])[['CO2 emissions (g/km)']].mean().sort_values(by='CO2 emissions (g/km)', ascending=False)

        fig = px.bar(fuel, x=fuel.index, 
                    y='CO2 emissions (g/km)', 
                    color='CO2 emissions (g/km)', 
                    labels={'CO2 emissions (g/km)': 'Emisi CO2'}, 
                    title='Rata-Rata Emisi CO2 dari setiap Bahan Bakar',
                    color_continuous_scale='oranges')
    
        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')
    
        st.plotly_chart(fig)
        st.write('''Jika kita lihat dari jenis bahan bakar, mobil dengan bahan bakar **Ethanol** menjadi yang paling banyak menyumbang gas emisi karbon dioksida (CO2)
        dan yang bahan bakar yang paling sedikit adalah Regular Gasoline''')



 #--------------------------------------------------------
    left, central,right = st.columns([1,2,1])
    with central:

        fig1 = px.scatter(CO2_Emissions_clean, x='Combined (L/100 km)', y='CO2 emissions (g/km)')
        fig2 = px.scatter(CO2_Emissions_clean, x='Combined (L/100 km)', y='Engine size (L)', color='Cylinders', color_continuous_scale='blues')

        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(fig1['data'][0], row=1, col=1)
        fig.add_trace(fig2['data'][0], row=1, col=2)

        # Atur rentang sumbu x dan y
        fig.update_xaxes(range=[CO2_Emissions_clean['Combined (L/100 km)'].min(), CO2_Emissions_clean['Combined (L/100 km)'].max()], row=1, col=1)
        fig.update_yaxes(range=[CO2_Emissions_clean['CO2 emissions (g/km)'].min(), CO2_Emissions_clean['CO2 emissions (g/km)'].max()], row=1, col=1)
        fig.update_xaxes(range=[CO2_Emissions_clean['Combined (L/100 km)'].min(), CO2_Emissions_clean['Combined (L/100 km)'].max()], row=1, col=2)
        fig.update_yaxes(range=[CO2_Emissions_clean['Engine size (L)'].min(), CO2_Emissions_clean['Engine size (L)'].max()], row=1, col=2)
        st.subheader('Dampak konsumsi bahan bakar dan Kapasitas Mesin terhadap Emisi CO2')
        fig.update_layout(
            height=500,  # Atur tinggi gambar
            width=800,  # Atur lebar gambar
            xaxis=dict(title='Fuel Consumption (L/100 km)'),  # Label sumbu x untuk gambar pertama
            yaxis=dict(title='CO2 Emissions(g/km)'),  # Label sumbu y untuk gambar pertama
            xaxis2=dict(title='Fuel Consumption (L/100 km)'),  # Label sumbu x untuk gambar kedua
            yaxis2=dict(title='Engine Size(L)')  # Label sumbu y untuk gambar kedua
        )
        st.plotly_chart(fig)
        st.write('''Jika dilihat korelasi antara konsumsi bahan bakar dengan Emisi gas karbon dioksida maka korelasinya berbanding lurus, semakin besarnya konsumsi bahan bakar maka akan menghasilkan emisi karbon dioksida (CO2)
        yang lebih tinggi. Selain itu tingkat konsumsi bahan bakar juga dipengaruhi oleh besarnya kapasitas mesin mobil yang digunakan. maka dapat disimpulkan bahwa emisi gas karbon dioksida (CO2) sangat dipengaruhi oleh 
        besarnya kapasitas mesin mobil dan juga banyaknya konsumsi bahan bakar yang digunakan''')

        correlations = CO2_Emissions_clean['Engine size (L)', 'Cylinders', 'Combined (L/100 km)', 'Combined (mpg)', 'CO2 rating', 'Smog rating'].corr()
        fig3, ax = plt.subplots(figsize = (6,4))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', cbar=True, ax=ax, fmt=".2g")
        
    c1,c2 = st.columns((7,3))
    with c1:
        st.markdown('### Heatmap Korelasi')
        st.pyplot(fig3)
    with c2:
        st.subheader('Hasilnya:')
        st.write('1. Konsumsi bahan bakar Liter per 100 km (Combined (L/100 km)): Memiliki korelasi positif kuat dengan Emisi CO2, menunjukkan bahwa semakin tinggi konsumsi bahan bakar dalam Liter per 100 km(L/100 km), maka semakin tinggi juga jumlah Emisi CO2 yang dihasilkan')
        st.write('2. Peringkat CO2 (CO2 rating): Memiliki korelasi negatif kuat dengan Emisi CO2, menunjukkan bahwa semakin kecil nilai CO2 rating, maka semakin tinggi Emisi CO2 yang dihasilkan')
        st.write('3. Konsumsi bahan bakar Miles per Gallon (Combined (mpg)): Memiliki korelasi negatif kuat dengan Emisi CO2, walaupun tidak sekuat faktor-faktor ekonomi dan sosial.')
        st.write('4. Kapasitas mesin (Engine size (L)) & Silinder (Cylinders): Memiliki korelasi positif kuat dengan Emisi CO2, menunjukkan semakin besar kapasitas mesin & semakin banyak jumlah silinder, maka semakin tinggi Emisi CO2 yang dihasilkan')
        st.write('5. Peringkat kabut asap (Smog rating): Memiliki korelasi negatif kuat dengan Emisi CO2, menunjukkan bahwa Semakin kecil nilai Smog rating, maka semakin tinggi Emisi CO2 yang dihasilkan')

        st.markdown('Hasil korelasi ini menunjukkan bahwa enam faktor yaitu Kapasitas mesin (Engine size (L)), Silinder (Cylinders), Konsumsi bahan bakar Liter per 100 km (Combined (L/100 km), Konsumsi bahan bakar Miles per Gallon (combined (mpg)), Peringkat CO2 (CO2 rating), dan Peringkat Kabut asap (Smog rating) semuanya berkorelasi kuat dengan Emisi CO2 gram per km (CO2 emissions (g/km)). Faktor-faktor tersebut penting dalam mempengaruhi Emisi CO2. Namun, Konsumsi bahan bakar Liter per 100 km, Peringkat CO2, dan Konsumsi bahan bakar Miles per Gallon memiliki peran yang lebih dominan dalam menentukan Emisi CO2 suatu kendaraan.')

    with st.expander('Apakah Jenis bahan bakar memiliki pengaruh yang Signifikan terhadap Emmisi gas CO2?'):
        st.subheader('Uji Hipotesis Testing (ANOVA)')
        st.write('''Untuk melihat apakah jenis bahan bakar berpengaruh terhadap emisi gas CO2 maka perlu dilakukan tes uji Hipotesis testing agar kita tahu
        apakah memiliki pengaruh yang signifikan atau tidak, pada pengujian kali ini methode yang dilakukan adalah ANOVA.
        Tes ANOVA menjadi metode yang paling cocok dalam konteks ini, karena ANOVA dapat melakukan uji untuk membandingkan 3 atau lebih variabel data''')
        st.write('Hipotesis Nol (H0): Tidak ada perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar.')
        st.write('Hipotesis Alternatif (H1): Terdapat perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar.')
        st.subheader('\n')

        regular_gasoline = CO2_Emissions_clean[CO2_Emissions_clean['Fuel type'] == 'Regular Gasoline']['CO2 emissions (g/km)']
        premium_gasoline = CO2_Emissions_clean[CO2_Emissions_clean['Fuel type'] == 'Premium Gasoline']['CO2 emissions (g/km)']
        diesel = CO2_Emissions_clean[CO2_Emissions_clean['Fuel type'] == 'Diesel']['CO2 emissions (g/km)']
        ethanol = CO2_Emissions_clean[CO2_Emissions_clean['Fuel type'] == 'Ethanol']['CO2 emissions (g/km)']

        stat, p_value = f_oneway(regular_gasoline, premium_gasoline, diesel, ethanol)

        # Menampilkan hasil
        st.write('Hasil Uji ANOVA:')
        from decimal import Decimal

        p_value_formatted = format(Decimal(p_value), '0.2e')
        st.write('P-value:', p_value_formatted)

        st.write(r'''Telah dilakukan Hipotesis Testing dengan menggunakan pengujian statistik ANOVA, untuk melihat apakah terdapat perbedaan yang signifikan Emisi karbon dioksida (CO2) yang dihasilkan pada setiap jenis bahan bakar (regular\_gasoline, premium\_gasoline, diesel dan ethanol).
        Hasil dari uji ANOVA menunjukkan bahwa nilai p-value yang diperoleh sangat kecil ($8.66 \times 10^{-19}$). Karena nilai p-value lebih kecil dari tingkat signifikansi yang telah ditentukan (biasanya $\alpha = 0.05$),
        kita dapat menolak hipotesis nol (tidak ada perbedaan signifikan) sehingga dapat disimpulkan bahwa terdapat perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar yang diuji dan Ethanol merupakan bahan bakar yang paling banyak menyumbang emisi gas karbon dioksida(CO2).''')


    one,two,three = st.columns([1,2,1])
    with two:
        st.header('\n')
        st.markdown("<h1 style='text-align: center;'>Recommendation</h1>", unsafe_allow_html=True)
        st.write('''Untuk menjawab tantangan mengurangi tingkat emisi karbon dioksida (CO2), salah satu cara paling efektif adalah mengganti kendaraan konvensional dengan kendaraan listrik. Namun, tidak semua orang mampu membeli kendaraan listrik karena harganya yang lebih mahal dibandingkan dengan kendaraan konvensional. 
                 Berdasarkan data emisi karbon dioksida (CO2) di Kanada, jenis bahan bakar yang digunakan ternyata memiliki dampak signifikan terhadap emisi CO2. Oleh karena itu, sebagai alternatif untuk mengurangi emisi karbon dioksida, pengguna kendaraan sebaiknya lebih bijak dalam memilih jenis bahan bakar.
                 Mobil yang menggunakan bahan bakar **Regular Gasoline** menghasilkan emisi CO2 yang lebih rendah yaitu sebesar 234.7 g/km, dibandingkan dengan Ethanol yang menghasilkan emisi CO2 sebesar 309.67 g/km. Berikut adalah beberapa alasan yang mendukung rekomendasi ini:''')
        st.write('1. Emisi CO2 yang Lebih Rendah: Mobil yang menggunakan Regular Gasoline cenderung memiliki emisi CO2 yang lebih rendah dibandingkan dengan jenis bahan bakar lainnya, sehingga dapat membantu mengurangi jejak karbon dan dampak lingkungan.')
        st.write('2. Ketersediaan dan Infrastruktur: Regular gasoline adalah jenis bahan bakar yang umum dan mudah ditemukan di stasiun pengisian bahan bakar. Infrastruktur yang mendukung penggunaan bahan bakar ini juga lebih luas dan tersedia secara luas di berbagai wilayah.')
        st.write('3. Efisiensi Konsumsi Bahan Bakar: Mobil yang menggunakan regular gasoline umumnya memiliki efisiensi konsumsi bahan bakar yang baik. Hal ini dapat menghasilkan penggunaan bahan bakar yang lebih efisien dan mengurangi ketergantungan terhadap bahan bakar.')
        st.write('4. Pilihan Kendaraan yang Tersedia: Sebagian besar produsen mobil menawarkan berbagai pilihan kendaraan yang menggunakan regular gasoline. Hal ini memberikan fleksibilitas bagi konsumen untuk memilih kendaraan yang sesuai dengan kebutuhan dan preferensi mereka.')
        
        fuel_types = ['All'] +['Regular Gasoline', 'Diesel','Premium Gasoline','Ethanol']

        # Kolom filter
        selected_fuel = st.selectbox('Jenis Bahan Bakar', fuel_types)

        if selected_fuel == 'All':
            filtered_data = CO2_Emissions_clean.groupby(CO2_Emissions_clean['Fuel type'])[['CO2 emissions (g/km)']].mean().sort_values(by='CO2 emissions (g/km)', ascending=False)
        else:
            filtered_data = CO2_Emissions_clean[CO2_Emissions_clean['Fuel type'] == selected_fuel]

        # Hitung rata-rata emisi CO2 berdasarkan jenis bahan bakar
        fuel = filtered_data.groupby('Fuel type')['CO2 emissions (g/km)'].mean().sort_values(ascending=False).head(5)

        # Buat bar chart
        fig = px.bar(fuel, x=fuel.index, y='CO2 emissions (g/km)', 
                    color='CO2 emissions (g/km)', 
                    labels={'CO2 emissions (g/km)': 'Emisi CO2'},
                    title='Rata-Rata Emisi CO2 dari Setiap Bahan Bakar',
                    color_continuous_scale='oranges')

        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')

        # Tampilkan chart
        st.plotly_chart(fig)
                
        st.write('Sebelum melakukan pembelian mobil, juga penting untuk mempertimbangkan faktor lain seperti efisiensi bahan bakar secara keseluruhan, biaya perawatan, ketersediaan suku cadang, dan juga pertimbangan pribadi seperti preferensi lingkungan dan kenyamanan penggunaan.')


        data_lower = pd.DataFrame(CO2_Emissions_clean.groupby('Make')[['CO2 emissions (g/km)']].mean().sort_values(by=('CO2 emissions (g/km)')))
        st.write(data_lower)
        st.write('''Jika kita lihat berdasarkan Brand mobil, akan lebih baik pengguna mobil membeli mobil yang menghasilkan emisi CO2 yang rendah. dari data diatas dapat kita lihat bahwa Top 5 mobil dengan emisi CO2 terendah adalah
        **MINI, Kia, Honda, Hyundai, dan Toyota**''')


if __name__ == '__main__':
    run()
