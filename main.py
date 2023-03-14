import pandas as pd
from pandas_datareader import data as web
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
import requests
from service import Service
import asyncio

serv = Service()


#check auth state 
st.session_state['auth'] = serv.checkUserSession()




plt.style.use('seaborn-whitegrid')
st.set_option('deprecation.showPyplotGlobalUse', False)


#send user data
async def sendUserData(login, password):
    res  = await serv.sendUserData(login, password) 
    st.session_state['auth'] = res
    st.experimental_rerun()



#auth part
if st.session_state['auth']:
    with st.sidebar:
        st.title("АВТОРИЗИРОВАН!!")
else:
    with st.sidebar:
        if st.checkbox('регистрация', False):
            st.title("Регистрация:")
        else:
            st.title("Войти:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button('Войти'): 
            asyncio.run(  sendUserData(username, password)  )
            

# Title
st.write("""# PuTickers""")

# Invest Size Slider
investment = st.number_input('Размер инвестиций', 5000, 1000000, step=1000)
st.write(f'Инвестируемая сумма денег: ₽{investment} РУБ')

# Auto portfolio Configurator
if not st.checkbox('Автоподбор тикеров', True):
    examples = pd.read_csv('stocks.csv')
    symbols = examples['Symbol'].values.tolist()
    chosen_symbols = st.multiselect('Введите тикеры, из которых хотите состваить портфель', symbols, [])
    if st.button('Submit'):
        st.success(f'Ваш портфель состоит из: {" ".join(chosen_symbols)}')


# Risks/Profit Layout
choice = st.radio("Что вам важно?", ['Риски', 'Доходность'])
if choice == 'Риски':
    # Risks Layout
    risks = st.slider('Размер рисков %', 0, 100, step=1)
    st.metric(f'Риск', f'{risks} %')

    # Profit Layout
    st.metric(f'Профит', f'{int((100+risks)*investment/100)} ₽', f'{risks} %')
    profit = int((100+risks)*investment/100)
else:
    # Profit Layout
    profit = st.slider('Профит', 0, investment, step=1)
    st.metric(f'Доходность', f'{profit} ₽', f'{int(profit/investment*100)} %')

    # Risks Layout
    st.metric(f'Риск', f'{int(profit/investment*100)} %')

st.write()

