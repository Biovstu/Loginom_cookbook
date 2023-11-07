import pandas as pd

import sqlalchemy as sqla
from sqlalchemy.engine import URL

SERVER = ''
LOGIN = ''
PASS = ''
DBNAME = ''
TABLENAME = ''
PORT = ''

connection_url = URL.create(
    "postgresql",
    username=LOGIN,
    password=PASS,
    host=SERVER,
    port=PORT,
    database=DBNAME,
    query={},
)

# запрос таблицы
engine = sqla.create_engine(connection_url)
with engine.connect() as conn:
    df = pd.read_sql_table(TABLENAME, conn)