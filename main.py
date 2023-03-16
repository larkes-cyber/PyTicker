

import datetime
import random

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import requests
from service import Service
import asyncio

from get_data import Ticker
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
import plotly.express as px
from model import portfolio_simulation

df = px.data.iris()
df = pd.read_csv('jopa.csv')

print(df)

# tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
# with tab1:
#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
# with tab2:
#     st.plotly_chart(fig, theme=None, use_container_width=True)





ALL_TICKERS = ['YNDX', 'VKCO', 'TCSG', 'POLY', 'OZON', 'OKEY', 'MDMG', 'QIWI', 'SFTL', 'HHRU', 'POSI', 'WUSH', 'GLTR',
               'GEMC', 'FIXP', 'FIVE', 'ETLN', 'CIAN', 'AGRO', 'UPRO', 'SFIN', 'ENPG', 'ENRU', 'PHOR', 'TRNFP', 'TGKA',
               'TATNP', 'TATN', 'FLOT', 'AFKS', 'SELG', 'SGZH', 'CHMF', 'SBERP', 'SBER', 'SMLT', 'RNFT', 'HYDR', 'RUAL',
               'RTKMP', 'RTKM', 'FEES', 'ROSN', 'RENI', 'PLZL', 'PIKK', 'NVTK', 'NLMK', 'MTSS', 'MOEX', 'MAGN', 'CBOM',
               'MTLRP', 'MTLR', 'MGNT', 'MVID', 'LKOH', 'LSRG', 'LENT', 'IRAO', 'DSKY', 'GMKN', 'GAZP', 'VTBR', 'BSPB',
               'BELU', 'AFLT', 'ALRS', 'MSNG']




# send user data
def sendUserData(login, password, type):
    print(type)
    res =  serv.sendUserData(login, password, type)
    print(res)
    st.session_state['auth'] = res
    st.session_state['err'] = not(res)
    st.experimental_rerun()


def get_candlestick_chart(df: pd.DataFrame, ticker, ma1, ma2):

    df['10_ma'] = df['close'].rolling(10).mean()
    df['20_ma'] = df['close'].rolling(20).mean()

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
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Candlestick chart'
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['date'], y=df[f'{ma1}_ma'], name=f'{ma1} SMA'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['date'], y=df[f'{ma2}_ma'], name=f'{ma2} SMA'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df['date'], y=df['value'], name='Volume'),
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


try:
    print(st.session_state['showNextInfo'])
except:
    st.session_state['showNextInfo'] = False

print('###########')
# auth part
if st.session_state['auth']:
    with st.sidebar:
        st.title("АВТОРИЗИРОВАН!!")
else:
    flag = True
    with st.sidebar:
        if st.checkbox('регистрация', False):
            flag = False
            st.title("Регистрация:")
        else:
            flag = True
            st.title("Войти:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button('Войти'):
            sendUserData(username, password,'login' if flag else 'reg')


# Title
title_cols = st.columns([1, 6])
title_cols[0].image(
    "https://user-images.githubusercontent.com/60555372/225298739-6126a612-44f3-4ff1-a78d-df1e58922cf2.png", width=100)
title_cols[1].write("""# PuTickers""")

chosen_symbols = []



choice = st.radio('', ['Просмотр тикеров', 'Создание портфеля'])
if choice == 'Создание портфеля':
    # Invest Size Slider
    investment = st.number_input('Размер инвестиций', 5000, 1000000, step=1000)
    st.write(f'Инвестируемая сумма денег: ₽{investment} РУБ')

    # Auto portfolio Configurator
    if not st.checkbox('Автоподбор тикеров', False):
        st.session_state['showNextInfo']=False
        chosen_symbols = st.multiselect('Введите 10 тикеров, из которых хотите составить портфель', ALL_TICKERS,
                                        [], disabled=False)
    else:
        st.session_state['showNextInfo']=True
        chosen_symbols = st.multiselect('Введите 10 тикsеров, из которых хотите составить портфель', ALL_TICKERS,
                                        [], disabled=True)
    if st.button("Подтвердить" if len(chosen_symbols) == 10 else "Выберите 10 тикеров!",disabled=len(chosen_symbols) != 10): st.session_state['showNextInfo']=True
    # Risks/Profit Layout
    if st.session_state['showNextInfo']:
        st.text('Что вам важно?')
        
        col1, col2 = st.columns(2)
        with col1:
            st.button('максимальная прибыль, высокие риски')
        with col2:
            st.button('умеренный доход с минимальными рисками')

        st.title(" ")
        col3, col4, col5 = st.columns([1,3, 4])
        with col3:
            st.metric(f'Доходность', f'{12} ₽', f'{int(45)} %')
        with col4:
            st.metric(f'Риск', f'34 %')


        fig = px.scatter(
            portfolio_simulation(chosen_symbols)[0],
            x="sepal_width",
            y="sepal_length",
            color="sepal_length",
            color_continuous_scale="blues",
        )


        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
     
        # On submit
        if st.button('Submit',key=2):
            st.success(f'Ваш портфель составлен!')
            print('###################')
            # getting ticker's weights
            # st.subheader("")
            weights = [random.Random().randint(1, 20) for i in range(len(chosen_symbols))]
            c = st.container()

            # Tickers Diagram
            diagram = st.plotly_chart(get_tickers_diagram(pd.DataFrame({'Количество': weights, 'Тикер': chosen_symbols})))

            # Tickers Layout
            for i in range(len(chosen_symbols)):
                with st.expander(f'{chosen_symbols[i]}'):

                    ticker_name = chosen_symbols[i]
                    ticker_loader = Ticker(ticker_name)
                    ticker_info = ticker_loader.get_ticker_info()
                    df = ticker_loader.get_history_ticker_day()
                    df.to_csv(f'{ticker_name}.csv')
                    df = pd.read_csv(f'{ticker_name}.csv', sep=',')
                    shortname = str(ticker_info['shortname'].loc[df.index[0]])
                    cost, percs, day_low, day_high, capital, day_value, amount, pot_delta = df.iloc[-1]['close'], round(df.iloc[-1]['close']/df.iloc[-1]['open']*100-100, 2), df.iloc[-1]['low'], df.iloc[-1]['high'], 25110250000, int(df.iloc[-1]['value']), \
                    weights[i], 20

                    # Head
                    ticker_head_view = st.columns(4)
                    ticker_head_view[0].subheader(shortname)
                    ticker_head_view[3].metric(f"Количество акций", amount)
                    ticker_head_view[1].metric(f'Цена', f'{cost} ₽', f'{percs} %')
                    ticker_head_view[2].metric(f'Стоимость бумаг в портфеле', f'{cost * amount} ₽',
                                            f'{round(cost * amount - cost * amount / (100 + percs) * 100, 1)} ₽')
                    # Desc 1
                    ticker_head_view = st.columns(3)
                    ticker_head_view[0].write('Диапазон за сегодня')
                    ticker_head_view[0].subheader(f'{day_low} ₽ - {day_high} ₽')
                    ticker_head_view[1].write('Объем торгов за сегодня')
                    ticker_head_view[1].subheader(f'{day_value} ₽')
                    ticker_head_view[2].metric('Потенциальная прибыль',
                                            value=f'{round(amount * cost * (100 + pot_delta) / 100 - amount * cost, 2)} ₽',
                                            delta=f'{pot_delta} %')
                    # ticker_head_view[2].write('Капитализация')
                    # ticker_head_view[2].subheader(f'{capital} ₽')

                    # Desc 2
                    ticker_main_view = st.columns(1)
                    ticker_main_view[0].write(ticker_info, use_container_width=True)
                    # Performance
                    st.subheader('Результаты')
                    week_perform = round(
                        (float(df.iloc[[-1]]['open']) - float(df.iloc[[-7]]['open'])) / float(df.iloc[[-7]]['open']) * 100,
                        2)
                    month_perform = round((float(df.iloc[[-1]]['open']) - float(df.iloc[[-30]]['open'])) / float(
                        df.iloc[[-30]]['open']) * 100, 2)
                    half_year_perform = round((float(df.iloc[[-1]]['open']) - float(df.iloc[[-180]]['open'])) / float(
                        df.iloc[[-180]]['open']) * 100, 2)
                    # year_perform = round((float(df.iloc[[-1]]['open']) - float(df.loc['2022:']['open'])) / float(
                    #     df.iloc[[-365]]['open']) * 100, 2)
                    # Performance view
                    perform_cols = st.columns(4)
                    perform_cols[0].metric('7 дней', value="", delta=f'{week_perform} %')
                    perform_cols[1].metric('30 дней', value="", delta=f'{month_perform} %')
                    perform_cols[2].metric('180 дней', value="", delta=f'{half_year_perform} %')
                    # perform_cols[3].metric('З65 дней', value="", delta=f'{year_perform} %')

                    # Graphic
                    print(df)
                    st.plotly_chart(get_candlestick_chart(df, ticker_name, 10, 20), use_container_width=True)
        st.write()
else:
    # ticker search
    ticker = st.selectbox('Введите тикер', ALL_TICKERS)
    try:
        ticker_loader = Ticker(ticker)
        ticker_loader.get_history_ticker_day().to_csv(f'{ticker}.csv')

        df = pd.read_csv(f'{ticker}.csv')

        st.plotly_chart(get_candlestick_chart(df, ticker, 10, 20), use_container_width=True)

        st.write(ticker_loader.get_ticker_info())
    except:
        st.error('Error while loading ticker')
