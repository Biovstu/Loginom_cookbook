import numpy as np, pandas as pd

# Импорт специализированных библиотек для испорта из Р7
import requests
import shutil
import tempfile
import os
import openpyxl


#Класс для работы с Р7
class r7docs:
    # Первичная инициализация
    def __init__(self, username, password, r7url):
        self.username = username
        self.password = password
        self.r7url = r7url
        self.token = ""
        
    # Получить токен для соединения    
    def auth(self):
        data = {
    "userName": self.username,
    "password": self.password
        }
        endpoint = "/api/2.0/authentication.json"
        url = f"{self.r7url}{endpoint}"
        response = requests.post(url, data=data)
        token = response.json()["response"]["token"]
        self.token = token
        return token
    
    # Скачать файл, возращает путь к скачанному файлу
    def download_file(self,fileid):
        
        endpoint = f"/api/2.0/files/file/{fileid}/presigneduri" 
        r = self.r7_get_request(endpoint = endpoint)
        url = r.json()["response"] # Считываем сгенерированную ссылку Р7 на скачивание файла
  
        r = self.r7_get_request(endpoint = url, skip_base_url = True, stream = True) # Скачиваем файл
    
        fp = tempfile.NamedTemporaryFile(delete = False) # Cоздаём временный файл и чтобы он не удалялся сразу
        path = fp.name
        
        # Записываем содержимое ответа в файл
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f) 
        
        return path
    
    # Get запрос в Р7 с использованием токена
    def r7_get_request(self, endpoint, params = "", skip_base_url = False, stream = False):
        
        # Если стоит skip_base_url = True, то будет обращение прямо по endpoint. Предполагается, что он полноценный. По умолчанию нет.    
        url = endpoint if skip_base_url else f"{self.r7url}{endpoint}"
        
        headers = {'Authorization': self.token}
        response = requests.get(url,params = params, headers = headers, stream = stream)
        
        return response
    
    def upload(self, file, folderid):
        file = {'upload_file': open(file,'rb')}
        headers = {'Authorization': self.token}
        endpoint = f"/api/2.0/files/{folderid}/upload"
        url = f"{self.r7url}{endpoint}"
        r = requests.post(url, files=file, headers = headers)
        
        return r


# Основной код

# Получаем переменные
log_in = ''
pass_word = ''
url_path = ''
id_file = ''
sheet = ''

#Создаем объект r7docs. Не меняем логин/пароль. Специально сделали в Р7.
r7 = r7docs(username = log_in, password = pass_word, r7url = url_path)

#Иницируем соединение c Р7
r7.auth()

#Передаём ID файла, который хотим скачать. Убедиться, что в Р7 к этому файлу есть доступ у пользователя svc_api. Если нет, то дать
# В path записываться путь скачанного файла. Файл скачивается во временную директорию
path = r7.download_file(fileid = id_file)

#Пример использования
r7_table = pd.read_excel(open(path, 'rb'), sheet_name = sheet, engine = 'openpyxl')