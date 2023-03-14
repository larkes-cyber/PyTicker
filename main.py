import pandas as pd
from pandas_datareader import data as web
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yt
import plotly.io as pio
import plotly.graph_objects as go


def get_candlestick_chart(df: pd.DataFrame, ticker):
    layout = go.Layout(
        title=f'График {ticker}',
        xaxis={'title': 'Дата'},
        yaxis={'title': 'Цена'},
    )

    fig = go.Figure(
        layout=layout,
        data=[
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Candlestick chart'
            ),
        ]
    )

    fig.update_xaxes(rangebreaks=[{'bounds': ['sat', 'mon']}])

    return fig


pio.renderers.default = 'browser'


plt.style.use('seaborn-whitegrid')
st.set_option('deprecation.showPyplotGlobalUse', False)

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
        df = yt.download(f'{ticker}')
        print(df)
        df.to_csv(f'{ticker}.csv')

        st.plotly_chart(get_candlestick_chart(df, ticker), use_container_width=True)
    except:
        st.error('Error while loading ticker')




