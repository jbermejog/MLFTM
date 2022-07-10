import streamlit as st
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

features_list=[
    'mes',
    'dia',
    'presMax',
    'presMin',
    'sol',
    'tmin',
    'prec',
    'velmedia',
    'racha']

features = pd.DataFrame(columns=features_list)
path_model = '../models/'

st.set_page_config(page_title='Temperatura máxima',layout='wide')
st.title("Predicción de la temperatura máxima")


with st.sidebar:
    st.title('Rellenar parámetros')
    with st.form(key='formulario clima'):
        clima = {}
        err = 0
        start_date = dt.date.today()
        start_date = st.date_input('Date', value=start_date)
        date = str(start_date)
        list_date = date.split('-')
        if start_date < dt.date.today():
            st.error('Error: La fecha ha de ser superior o igual a hoy')
            err = 1

        clima['mes'] = float(list_date[1])
        clima['dia'] = float(list_date[2])
        
        clima['presMax'] = st.slider('Presión Máxima (hPa):', min_value=850.0, max_value=1100.0, step=0.1, value=1000.0)
        clima['presMin'] = st.slider('Presión Mínima (hPa):', min_value=850.0, max_value=1100.0, step=0.1, value=950.0)
        if clima['presMax'] <= clima['presMin']:
            st.error('Error: La presión Máxima ha de ser superior a la presión mínima')
            err = 1
        
        clima['sol'] = st.slider('Horas de sol (en horas):', min_value=-0.0, max_value=15.0, step=1.0, value=8.0)
        clima['tmin'] = st.slider('Temperatura Mínima (ºC):', min_value=-30.0, max_value=50.0, step=0.1, value=10.0)
        clima['prec'] = st.slider('Precipitaciones (mm):', min_value=0.0, max_value=200.0, step=0.01, value=0.0)
        clima['velmedia'] = st.slider('Velocidad media del viento (m/s):', min_value=0.0, max_value=30.0, step=0.01, value=4.0)
        clima['racha'] = st.slider('Velocidad máxima del viento (m/s):', min_value=0.0, max_value=60.0, step=0.01, value=10.0)
            
        submit_button_predict = st.form_submit_button(label='Predecir')

if submit_button_predict and err == 0:
    features = features.append(clima, ignore_index=True)

    reg_clima = joblib.load(path_model+'modelo_mejor.sav')
    prediccion_clima = reg_clima.predict(features[features_list])
        
    
    valor_tmax = prediccion_clima
    

    st.write('---------------------------------------------')

    st.header('Temperatura Máxima')
    st.write('\n')
    st.write('\n')

    c1, c2 = st.columns((4, 5))
    with c1:
        st.subheader('Estación Getafe')
        st.write('\n')
        st.write('Para la fecha '+str(start_date))
        st.write('Se espera una máxima de '+str(round(valor_tmax[0],1))+' ºC.')
        st.write('\n')

    with c2:
        st.write('Identificador 3200')
        st.write('\n')
        st.write('Latitud 40.299444')
        st.write('Longitud -3.722222')
        st.write('Altitud 620m')
