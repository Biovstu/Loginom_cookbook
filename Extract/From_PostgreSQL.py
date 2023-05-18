import psycopg2
from psycopg2 import OperationalError
import pandas as pd

db_name = ''
db_user = ''
db_password = ''
db_host = ''
db_port = ''
table = ''

try:
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port)
    print("Connection to PostgreSQL DB successful")
    try:
        with connection.cursor() as cursor:
            query = f'SELECT * FROM {table}'
            cursor.execute(query)
            result = cursor.fetchall()
            desc = cursor.description
    finally:
        connection.close()
except OperationalError as e:
    print(f"The error '{e}' occurred")

col = pd.DataFrame(desc)
col[0] = col[0].apply(lambda x: x[0]) # выделяем только назвнаия столбцов

# Создаем основную таблицу
df = pd.DataFrame(result, columns=col[0]) 