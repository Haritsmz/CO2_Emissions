import streamlit as st
import eda
import model

st.set_page_config(
    page_title = "Home Page",
    layout='wide'
)

navigation = st.sidebar.selectbox('Pilih Halaman : ',('Insight Analysis', 'Web Apps'))

if navigation =='Insight Analysis':
    eda.run()
else:
    model.run()