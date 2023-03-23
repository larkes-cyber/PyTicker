from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("postgresql://fgvqsuuw:fziWIx4G-xu3bPvFa4zVSo1TIPZf7Vyc@mel.db.elephantsql.com/fgvqsuuw")


class Ticker:
    def __init__(self, ticker) -> None:
        self.ticker = ticker

    def get_ticker_info(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM tiker_info WHERE secid = '{self.ticker}'"), con=engine.connect())

    def get_history_ticker_hour(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_hour WHERE secid = '{self.ticker}'"), con=engine.connect())
    
    def get_history_ticker_day(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_day WHERE secid = '{self.ticker}'"), con=engine.connect())

    def get_history_ticker_week(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_week WHERE secid = '{self.ticker}'"), con=engine.connect())
    
    def get_history_ticker_month(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_month WHERE secid = '{self.ticker}'"), con=engine.connect())

    def get_history_ticker_quarter(self):
        return pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_quarter WHERE secid = '{self.ticker}'"), con=engine.connect())

