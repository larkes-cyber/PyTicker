import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")

tikers = ['VKCO', 'GAZP', 'LKOH', 'POLY', 'POSI', 'SBER', 'OZON', 'AFLT', 'MTLR', 'PIKK']

def sr_year_profit(df, tiker_name):   # доходность по месяцам одного тикера
    df[tiker_name] = df['close'].pct_change()
    df = df[['date', tiker_name]]
    df = df.set_index('date')
    return df['2022-1-1':]

def portfolio_simulation(tikers):
    df_tikers = pd.DataFrame()
    for tiker in tikers:
        df_tikers = df_tikers.add(sr_year_profit(pd.read_sql_query(f"SELECT * FROM history_tiker_month WHERE secid = '{tiker}'", con=engine), tiker), fill_value=0)

    num_assets = 10
    
    returns = df_tikers

    portfolio = []
    port_returns = []
    port_vols = []
    
    for i in range (300):
        weights = np.random.dirichlet(np.ones(num_assets),size=1)
        weights = weights[0]
        portfolio.append(weights)
        port_returns.append(np.sum(returns.mean() * weights) * 252)
        port_vols.append(np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights))))
    
    # Convert lists to arrays
    portfolio = np.array(portfolio)
    port_returns = np.array(port_returns)
    port_vols = np.array(port_vols)

    port = np.column_stack([port_returns, port_vols])
    index_max_returns = np.where(port == np.amax(port, axis = 0)[0])[0][0]
    max_returns = port[index_max_returns]
    max_portfolio = portfolio[index_max_returns]

    df_graph = pd.DataFrame({'sepal_length': port_returns, 'sepal_width': port_vols})

    return df_graph, max_returns, max_portfolio

print(portfolio_simulation(tikers))
