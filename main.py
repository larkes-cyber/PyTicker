import random

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
import plotly.express as px
import os


# send user data
async def sendUserData(login, password):
    res = await serv.sendUserData(login, password)
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


def get_tickers_diagram(df):
    fig = px.pie(df, values='Количество', names='Тикер')
    fig.update_traces(hole=.8, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="Баланс портфеля",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=f'{df.shape[0]} компаний', font_size=20, showarrow=False)])
    return fig

pio.renderers.default = 'browser'

plt.style.use('seaborn-whitegrid')
st.set_option('deprecation.showPyplotGlobalUse', False)

serv = Service()
# check auth state
st.session_state['auth'] = serv.checkUserSession()

# auth part
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
            asyncio.run(sendUserData(username, password))

examples = pd.read_csv('stocks.csv')
symbols = examples['Symbol'].values.tolist()

# Title
title_cols = st.columns([1, 6])
title_cols[0].image("https://user-images.githubusercontent.com/60555372/225298739-6126a612-44f3-4ff1-a78d-df1e58922cf2.png", width=100)
title_cols[1].write("""# PuTickers""")

choice = st.radio('', ['Просмотр тикеров', 'Создание портфеля'])
if choice == 'Создание портфеля':
    # Invest Size Slider
    investment = st.number_input('Размер инвестиций', 5000, 1000000, step=1000)
    st.write(f'Инвестируемая сумма денег: ₽{investment} РУБ')

    # Auto portfolio Configurator
    if not st.checkbox('Автоподбор тикеров', True):
        chosen_symbols = st.multiselect('Введите тикеры, из которых хотите составить портфель', symbols, ['AAPL', 'AMZN', 'NKE', 'QCOM', 'CSCO'], disabled=False)
    else:
        chosen_symbols = st.multiselect('Введите тикеры, из которых хотите составить портфель', symbols, ['AAPL', 'AMZN', 'NKE', 'QCOM', 'CSCO'], disabled=True)
    # Risks/Profit Layout
    choice_risks = st.radio("Что вам важно?", ['Риски', 'Доходность'])
    if choice_risks == 'Риски':
        # Risks Layout
        risks = st.slider('Размер рисков %', 0, 100, step=1)
        st.metric(f'Риск', f'{risks} %')

        # Profit Layout
        st.metric(f'Профит', f'{int((100 + risks) * investment / 100)} ₽', f'{risks} %')
        profit = int((100 + risks) * investment / 100)
    else:
        # Profit Layout
        profit = st.slider('Профит', 0, investment, step=1)
        st.metric(f'Доходность', f'{profit} ₽', f'{int(profit / investment * 100)} %')

        # Risks Layout
        st.metric(f'Риск', f'{int(profit / investment * 100)} %')

    # On submit
    if st.button('Submit'):
        st.success(f'Ваш портфель составлен!')

        # getting ticker's weights
        # st.subheader("")
        weights = [random.Random().randint(1, 20) for i in range(len(chosen_symbols))]
        c = st.container()

        # Tickers Diagram
        diagram = st.plotly_chart(get_tickers_diagram(pd.DataFrame({'Количество': weights, 'Тикер': chosen_symbols})))

        # Tickers Layout
        for i in range(len(chosen_symbols)):
            with st.expander(f'{chosen_symbols[i]}'):
                cost, percs, day_low, day_high, capital, day_value, amount, pot_delta = 21.785, 3.34, 20.815, 22.78, 25110250000, 457740812, weights[i], 20
                # Head
                ticker_head_view = st.columns(3)
                ticker_head_view[0].title('Белон АО')
                ticker_head_view[1].metric(f'Цена', f'{cost} ₽', f'{percs} %')
                ticker_head_view[2].metric(f'Стоимость бумаг в портфеле', f'{cost * amount} ₽', f'{round(cost*amount - cost*amount/(100+percs)*100, 1)} ₽')
                # Desc 1
                ticker_head_view = st.columns(3)
                ticker_head_view[0].write('Диапазон за сегодня')
                ticker_head_view[0].subheader(f'{day_low} ₽ - {day_high} ₽')
                ticker_head_view[1].write('Объем торгов за сегодня')
                ticker_head_view[1].subheader(f'{day_value} ₽')
                ticker_head_view[2].write('Капитализация')
                ticker_head_view[2].subheader(f'{capital} ₽')
                # Desc 2
                ticker_main_view = st.columns([1, 2])
                ticker_main_view[1].write(pd.read_csv('blng.csv', sep=';', header=None), use_container_width=True)
                ticker_main_view[0].metric('Количество акций', amount)
                ticker_main_view[0].metric('Потенциальная прибыль', value=f'{amount*cost*(100+pot_delta)/100} ₽', delta=f'{pot_delta} %')
                item = 'MSFT.csv'
                df = pd.read_csv(f'MSFT.csv')
                df['10_ma'] = df['Close'].rolling(10).mean()
                df['20_ma'] = df['Close'].rolling(20).mean()
                # Performance
                week_perform = round((float(df.iloc[[-1]]['Open']) - float(df.iloc[[-7]]['Open'])) / float(df.iloc[[-7]]['Open']) * 100, 2)
                perform_cols = st.columns(5)
                perform_cols[0].metric('1W', value="", delta=f'{week_perform} %')
                # Graphic
                st.plotly_chart(get_candlestick_chart(df, item, 10, 20), use_container_width=True)
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


