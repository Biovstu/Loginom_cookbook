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
        "authentication": "ActiveDirectoryIntegrated", # удалить строку, если запуск с сервера выдает ошибку аутентификации
    },
)

# запрос таблицы
engine = sqla.create_engine(connection_url)
with engine.connect() as conn:
    df = pd.read_sql_table(TABLENAME, conn)

# запрос по строке SQl

query = 'SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;\
SET NOCOUNT ON;\
select \
[loginom].[ref_sql_to_string](t1._Fld2218RRef) as Place_Key, \
t1._Fld2225  as Volume, \
t2._Code as Code, \
[loginom].[ref_sql_to_string](t2._Fld5249RRef) as Type_Key, \
t3._Description as Type_Description, \
t3._Fld6370 as MaxVolume, \
t5._Description as Zona \
from dbo._InfoRg2217 as t1 \
inner join \
dbo._Reference91 as t2 \
on t1._Fld2218RRef = t2._IDRRef \
inner join \
dbo._Reference173X1 as t3 \
on t2._Fld5249RRef = t3._IDRRef \
inner join \
dbo._InfoRg2560 as t4 \
on t2._IDRRef = t4._Fld2561RRef \
inner join \
dbo._Reference74X1 as t5 \
on t4._Fld2562RRef = t5._IDRRef'

with engine.connect() as conn:
    df2 = pd.read_sql_query(query, conn) # для работы функции обязательно нужна версия Pandas 2.0
df2