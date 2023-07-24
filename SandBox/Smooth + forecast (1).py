#!/usr/bin/env python
# coding: utf-8

# Импортрируем общие библиотеки

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl
import warnings
import time


# Импортируем библиотеки сглаживания

# In[2]:


from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import Holt


# Подготовка исходных данных

# In[3]:


source = pd.read_excel('C:\\Users\\konstantin_kutovoy\\Documents\\BioVstu\\Регулярные\\forcast.xlsx', sheet_name='Лист2')
isoprep = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во']
formalin = source[source['Продукт'] == 'Формалин 10%, л']['Кол-во'].reset_index(drop=True)
lezvia = source[source['Продукт'] == 'Лезвия, шт']['Кол-во'].reset_index(drop=True)
meshocki = source[source['Продукт'] == 'Мешочки биопсийные']['Кол-во'].reset_index(drop=True)
kolca = source[source['Продукт'] == 'Кольца заливочные, шт.']['Кол-во'].reset_index(drop=True)
gistofor = source[source['Продукт'] == 'Гистофор 20%, л']['Кол-во'].reset_index(drop=True)
tush = source[source['Продукт'] == 'Тушь гистологическая, л']['Кол-во'].reset_index(drop=True)
antitelo = source[source['Продукт'] == 'Антитела к ROS1, тест']['Кол-во'].reset_index(drop=True)
sales = isoprep


# Сглаживание

# In[4]:


t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Расчет начат')
isoprep_df = pd.DataFrame(sales)
isoprep_df.rename(columns={'Кол-во':'Base'}, inplace=True)
isoprep_model = SimpleExpSmoothing(sales).fit(smoothing_level=0.1, optimized=True)
isoprep_smooth = isoprep_model.fittedfcast[1:]
df1 = pd.DataFrame(isoprep_smooth)
df1.rename(columns={0:'SES'}, inplace=True)
isoprep_df = pd.concat([isoprep_df, df1], axis=1)
isoprep_model = Holt(sales, exponential=False).fit(smoothing_level=0.1, smoothing_trend=0.2, optimized=True)
isoprep_smooth = isoprep_model.fittedfcast[1:]
df2 = pd.DataFrame(isoprep_smooth)
df2.rename(columns={0:'HES'}, inplace=True)
isoprep_df = pd.concat([isoprep_df, df2], axis=1)
isoprep_df


# In[5]:


isoprep_df.loc[isoprep_df['SES'] < 0,'SES'] = 0
isoprep_df.loc[isoprep_df['HES'] < 0,'HES'] = 0


# In[6]:


isoprep_df


# In[7]:


plt.figure(figsize=(10, 4))
sns.lineplot(isoprep_df)
plt.title('Сравнение сглаживания')
plt.xlabel('Период')
plt.ylabel('Кол-во')
plt.legend()
plt.show()


# Расчет прогноза

# In[8]:


from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


# Подберем возможные комбинации прогнозируемых данных в зависимости от предварительного сглаживания (нет, SES, HES) и 4х возможных значений тренда ['n', 'c', 't', 'ct']

# In[9]:


isoprep_fcast = isoprep_df[:-2]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Авторегрессия
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = AutoReg(isoprep_df[:-5][col], lags=12, trend=trend).fit().forecast(steps=3)
            df = pd.DataFrame(fcast)
            df.rename(columns={0:f'{col}-AR({trend})'}, inplace=True)
            isoprep_fcast = pd.concat([isoprep_fcast, df], axis=1)
    # Скользящее среднее
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = ARIMA(isoprep_df[:-5][col], order=(0, 0, 1), trend=trend).fit().forecast(steps=3)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-MA({trend})'}, inplace=True)
            isoprep_fcast = pd.concat([isoprep_fcast, df], axis=1)
    # Авторегрессия скользящего среднего
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = ARIMA(isoprep_df[:-5][col], order=(1, 0, 1), trend=trend).fit().forecast(steps=3)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-ARMA({trend})'}, inplace=True)
            isoprep_fcast = pd.concat([isoprep_fcast, df], axis=1)
    # Авторегрессионное интегрированное скользящее среднее только 'n', 't'
    for col in isoprep_df.columns:
        for trend in ['n', 't']:
            fcast = ARIMA(isoprep_df[:-5][col], order=(1, 1, 1), trend=trend).fit().forecast(steps=3)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-ARIMA({trend})'}, inplace=True)
            isoprep_fcast = pd.concat([isoprep_fcast, df], axis=1)
    # Сезонное авторегрессионное интегрированное скользящее среднее
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            for season in [2, 4, 6, 12]:
                fcast = SARIMAX(isoprep_df[:-5][col], order=(1, 1, 1), seasonal_order=(1, 0, 1, season), trend=trend).fit(disp=False).forecast(steps=3)
                df = pd.DataFrame(fcast)
                df.rename(columns={'predicted_mean':f'{col}-SARIMA({trend}-{season})'}, inplace=True)
                isoprep_fcast = pd.concat([isoprep_fcast, df], axis=1)


# In[10]:


isoprep_fcast


# In[11]:


isoprep_fcast_part = isoprep_fcast[-3:]
isoprep_fcast_part = isoprep_fcast_part.drop(columns=['SES','HES'])
plt.figure(figsize=(10, 4))
sns.lineplot(isoprep_fcast_part)
plt.title('Сравнение прогнозов')
plt.xlabel('Период')
plt.ylabel('Кол-во')
plt.legend()
plt.show()


# Расчитаем вес каждого из вариантов прогнозов<p>
# Вес определим как обратную величину от отклонения (1 - delta)<p>
# При этом добавим условие, что допустимым отклонением считаем величину +-30%

# In[12]:


isoprep_fcast_part


# In[13]:


isoprep_fcast_part.sum()


# In[14]:


isoprep_fcast_part.sum().drop(['Base']).min()


# In[15]:


if isoprep_fcast_part.sum()['Base'] != 0:
    base = isoprep_fcast_part.sum()['Base']
else:
    base = isoprep_fcast_part.sum().drop(['Base']).min()
isoprep_weight = pd.DataFrame(isoprep_fcast_part.sum())
isoprep_weight.rename(columns={0:'sum'}, inplace=True)
isoprep_weight.drop(index=['Base'], inplace=True)
def precision(x):
    precis = 1 - abs(x / base - 1)
    if 0.7 < precis < 1.3:
        return precis
    else:
        return 0
isoprep_weight['weight'] = isoprep_weight['sum'].apply(precision)
isoprep_weight


# In[16]:


t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Расчет закончен')


# In[17]:


sum_weight = isoprep_weight.sum()['weight']


# In[18]:


isoprep_weight[isoprep_weight['weight'] != 0].mean()['weight']


# In[19]:


isoprep_fcast_part = isoprep_df
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Авторегрессия
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = AutoReg(isoprep_df[:-2][col], lags=12, trend=trend).fit().forecast(steps=6)
            df = pd.DataFrame(fcast)
            df.rename(columns={0:f'{col}-AR({trend})'}, inplace=True)
            isoprep_fcast_part = pd.concat([isoprep_fcast_part, df], axis=1)
    # Скользящее среднее
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = ARIMA(isoprep_df[:-2][col], order=(0, 0, 1), trend=trend).fit().forecast(steps=6)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-MA({trend})'}, inplace=True)
            isoprep_fcast_part = pd.concat([isoprep_fcast_part, df], axis=1)
    # Авторегрессия скользящего среднего
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            fcast = ARIMA(isoprep_df[:-2][col], order=(1, 0, 1), trend=trend).fit().forecast(steps=6)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-ARMA({trend})'}, inplace=True)
            isoprep_fcast_part = pd.concat([isoprep_fcast_part, df], axis=1)
    # Авторегрессионное интегрированное скользящее среднее только 'n', 't'
    for col in isoprep_df.columns:
        for trend in ['n', 't']: # 'n', 'c', 't', 'ct'
            fcast = ARIMA(isoprep_df[:-2][col], order=(1, 1, 1), trend=trend).fit().forecast(steps=6)
            df = pd.DataFrame(fcast)
            df.rename(columns={'predicted_mean':f'{col}-ARIMA({trend})'}, inplace=True)
            isoprep_fcast_part = pd.concat([isoprep_fcast_part, df], axis=1)
    # Сезонное авторегрессионное интегрированное скользящее среднее
    for col in isoprep_df.columns:
        for trend in ['n', 'c', 't', 'ct']:
            for season in [2, 4, 6, 12]:
                fcast = SARIMAX(isoprep_df[:-2][col], order=(1, 1, 1), seasonal_order=(1, 0, 1, season), trend=trend).fit(disp=False).forecast(steps=6)
                df = pd.DataFrame(fcast)
                df.rename(columns={'predicted_mean':f'{col}-SARIMA({trend}-{season})'}, inplace=True)
                isoprep_fcast_part = pd.concat([isoprep_fcast_part, df], axis=1)
# isoprep_fcast_part


# Определим значение средневзвешенного прогноза

# In[20]:


isoprep_forecast = pd.DataFrame(isoprep_fcast_part['Base'])
isoprep_forecast['Forecast'] = 0
for i in isoprep_forecast.index:
    calc = 0
    for type_fcast in isoprep_weight.index:
        calc += isoprep_fcast_part.loc[i, type_fcast] * isoprep_weight.loc[type_fcast, 'weight'] / sum_weight
    isoprep_forecast.loc[i,'Forecast'] = calc


# In[21]:


isoprep_forecast.tail(10)


# In[22]:


plt.figure(figsize=(10, 4))
sns.lineplot(isoprep_forecast[-10:])
plt.title('Сравнение прогнозов')
plt.xlabel('Период')
plt.ylabel('Кол-во')
plt.legend()
plt.show()


# In[24]:


isoprep_weight


# In[ ]:




