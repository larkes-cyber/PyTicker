from sqlalchemy import create_engine, text
import pandas as pd
engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")

class Tiker():
    def __init__(self, tiker) -> None:
        self.tiker = tiker

    def get_tiker_info(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM tiker_info WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data

    def get_history_tiker_hour(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_hour WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data
    
    def get_history_tiker_day(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_day WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data

    def get_history_tiker_week(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_week WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data
    
    def get_history_tiker_month(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_month WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data

    def get_history_tiker_quarter(self):
        self.engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
        conn = engine.connect()
        data = pd.read_sql_query(sql=text(f"SELECT * FROM history_tiker_quarter WHERE secid = '{self.tiker}'"), con=conn)
        conn.close()
        return data