import pymysql
import pandas as pd

SERVER = ''
LOGIN = ''
PASS = ''
DBNAME = ''
TABLENAME = ''

# Инициализируем подключение, выбираем класс курсора, возвращающего словарь
try:
    connection = pymysql.connect(
        host=SERVER,
        user=LOGIN,
        password=PASS,
        database=DBNAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print("#" * 20)

# Исполняем курсор
    try:
        with connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM `{TABLENAME}`"
            cursor.execute(select_all_rows)
            dic = cursor.fetchall() # Полчаем все записи
    finally:
        connection.close()

except Exception as ex:
    print("Connection refused...")
    print(ex)

# Отправляем словарь в таблицу пандас
df = pd.DataFrame(dic)
df.sample(5)
