import pandas as pd

import sqlalchemy as sqla
from sqlalchemy.engine import URL

SERVER = ''
LOGIN = ''
PASS = ''
DBNAME = ''
TABLENAME = ''

connection_url = URL.create(
    "mssql+pyodbc",
    username=LOGIN,
    password=PASS,
    host=SERVER,
    port=None,
    database=DBNAME,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
        "authentication": "ActiveDirectoryIntegrated",
    },
)

engine = sqla.create_engine(connection_url)
with engine.connect() as conn:
    df = pd.read_sql_table(TABLENAME, conn)