from sqlalchemy import create_engine, text
from email.utils import parseaddr
from email_validator import validate_email, EmailNotValidError

def registed(email, password):
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

def login(email, password):
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