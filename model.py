import streamlit as st
import pandas as pd
import joblib


# Load files 
with open('pipeline_model_linearregression.pkl', 'rb') as file_2:
    pipeline_model_linearregression = joblib.load(file_2)


def run():
    st.markdown("<h1 style='text-align: center;'>CO2 Emission Predictor!</h1>", unsafe_allow_html=True)
    st.subheader('Track Your Carbon Footprint')
    st.write('by : Harits Mughni Zakinu')



    with st.form(key='form_parameters'):
        make = st.selectbox('Brand', ('Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW',
                                      'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge',
                                      'Ferrari', 'Ford', 'Genesis', 'GMC', 'Honda', 'Hyundai',
                                      'Infiniti', 'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Land Rover',
                                      'Lexus', 'Lincoln', 'Maserati', 'Mazda', 'Mercedes-Benz', 'MINI',
                                      'Mitsubishi', 'Nissan', 'Porsche', 'Ram', 'Rolls-Royce', 'Subaru',
                                      'Toyota', 'Volkswagen', 'Volvo'), index=1)
        Vehicle_Class = st.selectbox('Vehicle Class', ('Full-size', 'Sport utility vehicle: Small',
                                                       'Sport utility vehicle: Standard', 'Mid-size', 'Minicompact',
                                                       'Two-seater', 'Subcompact', 'Compact', 'Station wagon: Small',
                                                       'Station wagon: Mid-size', 'Pickup truck: Small',
                                                       'Pickup truck: Standard', 'Minivan'), index=1)
        Fuel_Type = st.selectbox('Fuel Type', ('Premium Gasoline', 'Regular Gasoline', 'Ethanol', 'Diesel'), index=1)
        Engine_Size = st.slider('Engine Size', min_value=1.2, max_value=8.0,value=1.2,step=0.1)
        Cylinders = st.number_input('Cylinders', min_value=3, max_value=16, value=3, step=1)
        Fuel_Consumption_Liter = st.number_input('Fuel Consumption (L/100 km)', min_value=4.4, max_value=26.1, value=4.4, step=0.1)
        Fuel_Consumption_mpg = st.number_input('Fuel Consumption (mpg)', min_value=11, max_value=64, value=11, step=1)
        CO2_rating = st.number_input('CO2 rating', min_value=1, max_value=8, value=1, step=1)
        Smog_rating = st.number_input('Smog rating', min_value=1, max_value=8, value=1, step=1)
        st.markdown('---')

        submitted = st.form_submit_button('Predict')


    data_inf={
            'Make'           : make,
            'Vehicle class'   : Vehicle_Class,
            'Fuel type'       : Fuel_Type,
            'Engine size (L)'     : Engine_Size,
            'Cylinders'       : Cylinders,
            'Combined (L/100 km)'  :Fuel_Consumption_Liter,
            'Combined (mpg)'    : Fuel_Consumption_mpg,
            'CO2 rating': CO2_rating,  
            'Smog rating': Smog_rating  
            }


    data_inf = pd.DataFrame([data_inf])

    if submitted:       
        y_pred = pipeline_model_linearregression.predict(data_inf)
        formatted_result = f"{y_pred:.2f}"

        st.write('The result is :')
        st.write(f'<p style="font-size:40px;">CO2 Emissions : {str(int(y_pred))} g/km</p>', unsafe_allow_html=True)
        

if __name__ == '__main__':
    run()
