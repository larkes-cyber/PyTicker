import datetime
import random

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from service import Service
from get_data import Ticker
from model import portfolio_simulation



ALL_TICKERS = ['YNDX', 'VKCO', 'TCSG', 'POLY', 'OZON', 'OKEY', 'MDMG', 'QIWI', 'SFTL', 'HHRU', 'POSI', 'WUSH', 'GLTR',
               'GEMC', 'FIXP', 'FIVE', 'ETLN', 'CIAN', 'AGRO', 'UPRO', 'SFIN', 'ENPG', 'ENRU', 'PHOR', 'TRNFP', 'TGKA',
               'TATNP', 'TATN', 'FLOT', 'AFKS', 'SELG', 'SGZH', 'CHMF', 'SBERP', 'SBER', 'SMLT', 'RNFT', 'HYDR', 'RUAL',
               'RTKMP', 'RTKM', 'FEES', 'ROSN', 'RENI', 'PLZL', 'PIKK', 'NVTK', 'NLMK', 'MTSS', 'MOEX', 'MAGN', 'CBOM',
               'MTLRP', 'MTLR', 'MGNT', 'MVID', 'LKOH', 'LSRG', 'LENT', 'IRAO', 'DSKY', 'GMKN', 'GAZP', 'VTBR', 'BSPB',
               'BELU', 'AFLT', 'ALRS', 'MSNG']
FEATURED_TICKERS = ['SBER', 'POLY', 'VKCO', 'LKOH', 'OZON', 'MTLR', 'POSI', 'BELU', 'PIKK', 'NVTK']


# send user data
def sendUserData(login, password, type):
    res = serv.sendUserData(login, password, type)
    st.session_state['auth'] = res
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
            sendUserData(username, password, 'login' if flag else 'reg')

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

    # Risks/profit
    risk_profit = st.radio(label="Что вам важно?", options=['Максимальная прибыль c высокими риски', 'Умеренный доход с минимальными рисками'])

    # Auto portfolio Configurator
    if not st.checkbox('Автоподбор тикеров', True):
        st.session_state['showNextInfo'] = False
        chosen_symbols = st.multiselect('Введите 10 тикеров, из которых хотите составить портфель', ALL_TICKERS,
                                        FEATURED_TICKERS, disabled=False)
    else:
        st.session_state['showNextInfo'] = False
        chosen_symbols = st.multiselect('Введите 10 тикеров, из которых хотите составить портфель', ALL_TICKERS,
                                        FEATURED_TICKERS, disabled=True)
    if st.button("Подтвердить" if len(chosen_symbols) == 10 else "Выберите 10 тикеров!",
                 disabled=len(chosen_symbols) != 10):
        st.session_state['showNextInfo'] = True

        # Risks/Profit Layout
        graph_port, max_returns, min_risks = portfolio_simulation(chosen_symbols)
        chosen_symbols = list(max_returns.columns)[2:]

        chosen_type = max_returns if risk_profit == "Максимальная прибыль c высокими риски" else min_risks

        weights = [chosen_type[i][chosen_type[i].index[0]] for i in chosen_symbols]

        col3, col4 = st.columns(2)
        with col3:
            st.metric(f'Доходность', f'{int((chosen_type["port_returns"][chosen_type["port_returns"].index[0]])/100*investment)} ₽', f'{round(chosen_type["port_returns"][chosen_type["port_returns"].index[0]], 2)} %')
        with col4:
            st.metric(f'Риск', f'{round(chosen_type["port_vols"][chosen_type["port_vols"].index[0]], 2)} %')

        port_graph = px.scatter(
            graph_port,
            x="sepal_width",
            y="sepal_length",
            color="sepal_length",
            color_continuous_scale="blues",
        )

        st.plotly_chart(port_graph, theme="streamlit", use_container_width=True)

        # On submit
        st.success(f'Ваш портфель составлен!')
        
        # getting ticker's weights
        tickers_costs = list(map(lambda x: round(x*investment), weights))
        weights = list(map(lambda x: x*100, weights))
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
                shortname = str(ticker_info['shortname'].loc[df.index[0]])
                cost, percs, day_low, day_high, capital, day_value, pot_delta = df.iloc[-1]['close'], round \
                        (df.iloc[-1]['close'] / df.iloc[-1]['open'] * 100 - 100, 2), df.iloc[-1]['low'], df.iloc[-1][
                        'high'], 25110250000, int(df.iloc[-1]['value']), 20
                amount = round(tickers_costs[i]/cost, 1)
                # Head
                ticker_head_view = st.columns(3)
                ticker_head_view[0].subheader(shortname)
                ticker_head_view[2].metric(f"Количество акций", amount)
                ticker_head_view[1].metric(f'Стоимость бумаг в портфеле', f'{round(cost * amount)} ₽',
                                               f'{round(cost * amount - cost * amount / (100 + percs) * 100, 1)} ₽')
                # Desc 1
                ticker_head_view = st.columns([1, 2])
                ticker_head_view[1].write('Диапазон за сегодня')
                ticker_head_view[1].subheader(f'{day_low} ₽ - {day_high} ₽')
                ticker_head_view[0].metric(f'Цена', f'{cost} ₽', f'{percs} %')
                # ticker_head_view[2].metric('Потенциальная прибыль',
                #                                value=f'{round(amount * cost * (100 + pot_delta) / 100 - amount * cost, 2)} ₽',
                #                                delta=f'{pot_delta} %')
                # ticker_head_view[2].write('Капитализация')
                # ticker_head_view[2].subheader(f'{capital} ₽')

                # Desc 2
                ticker_main_view = st.columns([2, 1])
                ticker_main_view[0].write(ticker_info, use_container_width=True)
                ticker_main_view[1].write('Объем торгов за сегодня')
                ticker_main_view[1].subheader(f'{day_value} ₽')
                # Performance
                st.subheader('Результаты')
                week_perform = round(
                        (float(df.iloc[[-1]]['open']) - float(df.iloc[[-7]]['open'])) / float
                        (df.iloc[[-7]]['open']) * 100,
                        2)
                month_perform = round((float(df.iloc[[-1]]['open']) - float(df.iloc[[-30]]['open'])) / float(
                        df.iloc[[-30]]['open']) * 100, 2)
                half_year_perform = round((float(df.iloc[[-1]]['open']) - float(df.iloc[[-180]]['open'])) / float(
                        df.iloc[[-180]]['open']) * 100, 2)
                # year_perform = round((float(df.iloc[[-1]]['open']) - float(df.loc['2022:']['open'])) / float(
                #     df.iloc[[-365]]['open']) * 100, 2)
                # Performance view
                perform_cols = st.columns(3)
                perform_cols[0].metric('7 дней', value="", delta=f'{week_perform} %')
                perform_cols[1].metric('30 дней', value="", delta=f'{month_perform} %')
                perform_cols[2].metric('180 дней', value="", delta=f'{half_year_perform} %')
                # perform_cols[3].metric('З65 дней', value="", delta=f'{year_perform} %')

                # Graphic
                st.plotly_chart(get_candlestick_chart(df, ticker_name, 10, 20), use_container_width=True)
        st.write()
else:
    # ticker search
    ticker = st.selectbox('Введите тикер', ALL_TICKERS)
    try:
        # Load ticker
        ticker_loader = Ticker(ticker)
        df = ticker_loader.get_history_ticker_day()

        # Show ticker
        st.plotly_chart(get_candlestick_chart(df, ticker, 10, 20), use_container_width=True)
        st.write(ticker_loader.get_ticker_info())
    except:
        st.error('Error while loading ticker')
