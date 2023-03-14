import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import requests
from service import Service
import asyncio

import yfinance as yt
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


#send user data
async def sendUserData(login, password):
    res  = await serv.sendUserData(login, password) 
    st.session_state['auth'] = res
    st.experimental_rerun()


def get_candlestick_chart(df: pd.DataFrame, ticker, ma1, ma2):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'График {ticker}', 'Объемы'),
        row_width=[0.3, 0.7]
    )

    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick chart'
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'{ma1}_ma'], name=f'{ma1} SMA'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'{ma2}_ma'], name=f'{ma2} SMA'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df['Date'], y=df['Volume'], name='Volume'),
        row=2,
        col=1,
    )

    fig['layout']['xaxis2']['title'] = 'Дата'
    fig['layout']['yaxis']['title'] = 'Цена'
    fig['layout']['yaxis2']['title'] = 'Объем'

    fig.update_xaxes(
        rangebreaks=[{'bounds': ['sat', 'mon']}],
        rangeslider_visible=False,
    )

    return fig


pio.renderers.default = 'browser'



plt.style.use('seaborn-whitegrid')
st.set_option('deprecation.showPyplotGlobalUse', False)


serv = Service()
#check auth state 
st.session_state['auth'] = serv.checkUserSession()

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
            

examples = pd.read_csv('stocks.csv')
symbols = examples['Symbol'].values.tolist()


# Title
st.write("""# PuTickers""")

choice = st.radio('', ['Просмотр тикеров', 'Создание портфеля'])
if choice == 'Создание портфеля':
    # Invest Size Slider
    investment = st.number_input('Размер инвестиций', 5000, 1000000, step=1000)
    st.write(f'Инвестируемая сумма денег: ₽{investment} РУБ')

    # Auto portfolio Configurator
    if not st.checkbox('Автоподбор тикеров', True):
        chosen_symbols = st.multiselect('Введите тикеры, из которых хотите состваить портфель', symbols, [])
        if st.button('Submit'):
            st.success(f'Ваш портфель состоит из: {" ".join(chosen_symbols)}')


    # Risks/Profit Layout
    choice_risks = st.radio("Что вам важно?", ['Риски', 'Доходность'])
    if choice_risks == 'Риски':
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
else:
    # ticker search
    ticker = st.selectbox('Введите тикер', symbols)
    try:
        if f'{ticker}.csv' not in os.listdir():
            df = yt.download(f'{ticker}')
            df.to_csv(f'{ticker}.csv')
        df = pd.read_csv(f'{ticker}.csv')
        df['10_ma'] = df['Close'].rolling(10).mean()
        df['20_ma'] = df['Close'].rolling(20).mean()

        st.plotly_chart(get_candlestick_chart(df, ticker, 10, 20), use_container_width=True)
    except:
        st.error('Error while loading ticker')



