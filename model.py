from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

engine = create_engine("postgresql://fgvqsuuw:fziWIx4G-xu3bPvFa4zVSo1TIPZf7Vyc@mel.db.elephantsql.com/fgvqsuuw")


def sr_year_profit(df, tiker_name):   # доходность по месяцам одного тикера
    df[tiker_name] = df['close'].pct_change()
    df = df[['date', tiker_name]]
    df = df.set_index('date')
    return df['2022-1-1':]

def portfolio_simulation(tikers, iterations):
    df_tikers = pd.DataFrame()
    for tiker in tikers:
        df_tikers = df_tikers.add(sr_year_profit(pd.read_sql_query(f"SELECT * FROM history_tiker_month WHERE secid = '{tiker}'", con=engine), tiker), fill_value=0)

    info_mean = df_tikers.mean()
    tikers = list(info_mean[info_mean > 0].index)
    df_tikers = df_tikers[list(info_mean[info_mean > 0].index)]


    num_assets = len(df_tikers.columns)
    returns = df_tikers

    port = []
    port_returns = []
    port_vols = []
    
    for i in range (iterations):
        weights = np.random.dirichlet(np.ones(num_assets),size=1)[0]
        port.append(weights)
        port_returns.append(np.sum(returns.mean() * weights) * 252)
        port_vols.append(np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights))))
    
    # Convert lists to arrays
    df_model = pd.DataFrame()
    df_model['port_returns'] = np.array(port_returns)
    df_model['port_vols'] = np.array(port_vols)
    for index in range(len(tikers)):
        df_model[tikers[index]] = (np.array(port).T)[index]
    
    index_max_returns = df_model.sort_values(by='port_returns', ascending=False).index[0]
    index_min_vols = df_model.sort_values(by='port_vols', ascending=True).index[0]

    df_graph = pd.DataFrame({'sepal_length': np.array(port_returns), 'sepal_width': np.array(port_vols)})

    return df_graph, df_model.loc[[index_max_returns]], df_model.loc[[index_min_vols]]