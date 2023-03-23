from sqlalchemy import text, create_engine
from email_validator import validate_email, EmailNotValidError
import pandas as pd



class Service():

    def sr_year_profit(self, db, tiker_name):  # доходность по месяцам одного тикера
        db[tiker_name] = db['close'].pct_change()
        return db

    def registed(self, email, password):
        engine = create_engine("postgresql://fgvqsuuw:fziWIx4G-xu3bPvFa4zVSo1TIPZf7Vyc@mel.db.elephantsql.com/fgvqsuuw")
        try:
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
        engine = create_engine("postgresql://fgvqsuuw:fziWIx4G-xu3bPvFa4zVSo1TIPZf7Vyc@mel.db.elephantsql.com/fgvqsuuw")
        try:
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

        return res

    def checkUserSession(save):
        try:
            session = open("session.txt")
            return True
        except:
            return False


