import time
from sqlalchemy import create_engine, text
from email.utils import parseaddr
from email_validator import validate_email, EmailNotValidError
import pandas as pd
import numpy as np
import math

class Service():

    def sr_year_profit(self, db, tiker_name):   # доходность по месяцам одного тикера
        db[tiker_name] = db['close'].pct_change()
        return db

    def registed(self, email, password):
        try:
            engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
            validate_email(email)
            data = pd.read_sql_query(sql=text(f"SELECT * FROM user_auth WHERE email = '{email}'"), con=engine.connect())
            if len(data) != 0:
                return False
            data = pd.DataFrame(data={'email': [email], 'password': [password]})
            data = data.set_index('email')
            data.to_sql(f'user_auth', engine, if_exists='append')
            return True
        except EmailNotValidError as Err:
            return False

    def login(self, email, password):
        try:
            engine = create_engine("postgresql://fgvqsuuw:SI4HeiCDMZ2CplWiUk4oxDHATWVirVDQ@mel.db.elephantsql.com/fgvqsuuw")
            validate_email(email)
            data = pd.read_sql_query(sql=text(f"SELECT * FROM user_auth WHERE email = '{email}'"), con=engine.connect())
            if len(data) == 0:
                return False
            if data['password'][0] != password:
                return False
            return True
        except EmailNotValidError as Err:
            return False
        
    def sendUserData(self, login, password, type):
        res = ''
        if type == 'login':
            res = self.login(login, password)
        else:
            res = self.registed(login, password)

        if res: 
            with open('session.txt', 'w') as f:
                f.write('auth')

        return  res
        
    def checkUserSession(save):
        try:
           session = open("session.txt")
           return True
        except:
            return False
    
    
    