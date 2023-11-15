#!/usr/bin/env python
# coding: utf-8

# Импортрируем общие библиотеки

# In[1]:


import numpy as np
import pandas as pd
import warnings
import time
import sqlalchemy as sqla
from sqlalchemy.engine import URL
import requests
import urllib.parse


# In[2]:


API_TOKEN = '6175205144:AAH81U1fI8g_O6q5_Ogzq7TYeF7AQzYu1Jc'
CHAT_ID = '-1001552021322'
TEXT = '#M5K Начат расчет прогноза'
TEXT = urllib.parse.quote(TEXT)
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}')


# Импортируем библиотеки сглаживания

# In[3]:


from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import Holt


# Импортируем библиотеки прогнозирования

# In[4]:


from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.statespace.sarimax import SARIMAX


# Составляем функцию прогноза

# In[5]:


def return_forcast(incoming_df, steps=1, steps_back=None):    
    if not steps_back is None:
        steps_back *= -1
    forcast_df = incoming_df
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Авторегрессия без 'ct'
        for col in incoming_df.columns:
            for trend in ['n', 'c', 't','ct']:
                fcast = AutoReg(incoming_df[:steps_back][col], lags=12, trend=trend).fit().forecast(steps=steps)
                df = pd.DataFrame(fcast)
                df.rename(columns={0:f'{col}-AR({trend})'}, inplace=True)
                forcast_df = pd.concat([forcast_df, df], axis=1)
        # Скользящее среднее только 'c', 'ct'
        for col in incoming_df.columns:
            for trend in ['c', 'ct', 't']:
                fcast = ARIMA(incoming_df[:steps_back][col], order=(0, 0, 1), trend=trend).fit().forecast(steps=steps)
                df = pd.DataFrame(fcast)
                df.rename(columns={'predicted_mean':f'{col}-MA({trend})'}, inplace=True)
                forcast_df = pd.concat([forcast_df, df], axis=1)
        # Авторегрессия скользящего среднего
        for col in incoming_df.columns:
            for trend in ['n', 'c', 't', 'ct']:
                fcast = ARIMA(incoming_df[:steps_back][col], order=(1, 0, 1), trend=trend).fit().forecast(steps=steps)
                df = pd.DataFrame(fcast)
                df.rename(columns={'predicted_mean':f'{col}-ARMA({trend})'}, inplace=True)
                forcast_df = pd.concat([forcast_df, df], axis=1)
        # Авторегрессионное интегрированное скользящее среднее только 'n', 't'
        for col in incoming_df.columns:
            for trend in ['n', 't']:
                fcast = ARIMA(incoming_df[:steps_back][col], order=(1, 1, 1), trend=trend).fit().forecast(steps=steps)
                df = pd.DataFrame(fcast)
                df.rename(columns={'predicted_mean':f'{col}-ARIMA({trend})'}, inplace=True)
                forcast_df = pd.concat([forcast_df, df], axis=1)
        # Сезонное авторегрессионное интегрированное скользящее среднее
#         for col in incoming_df.columns:
#             for trend in ['n', 'c', 't', 'ct']:
#                 for season in [2, 4, 6, 12]:
#                     fcast = SARIMAX(incoming_df[:steps_back][col], order=(1, 1, 1), seasonal_order=(1, 0, 1, season), trend=trend).fit(disp=False).forecast(steps=steps)
#                     df = pd.DataFrame(fcast)
#                     df.rename(columns={'predicted_mean':f'{col}-SARIMA({trend}-{season})'}, inplace=True)
#                     forcast_df = pd.concat([forcast_df, df], axis=1)
    forcast_df[forcast_df < 0] = 0
    return forcast_df


# Подготовка исходных данных

# In[6]:


t = time.strftime('%x %X', time.localtime(time.time()))
print(f'{t} - Расчет начат')

# time_start = time.strftime('%Y-%m-%d', time.localtime(time.time()))

SERVER = '10.101.10.171'
LOGIN = 'dwh_full_access'
PASS = 'K4cUSPbSEdUhOwoi'
DBNAME = 'dwh'
TABLE_SALES = 'SYS_FORECASTING_SALES'
TABLE_PARAMS = 'SYS_FORECASTING_SMOOTH_PARAMS'
PORT = '5432'
TABLENAME = 'SYS_FORECASTING_CUMUL'

connection_url = URL.create(
    "postgresql",
    username=LOGIN,
    password=PASS,
    host=SERVER,
    port=PORT,
    database=DBNAME,
    query={},
)

# загрузка в базу без индексов с перезаписыванием
engine = sqla.create_engine(connection_url)
with engine.connect() as conn:
    source = pd.read_sql(TABLE_SALES, conn)
    smooth_params = pd.read_sql(TABLE_PARAMS, conn)
t = time.strftime('%x %X', time.localtime(time.time()))
print(f'{t} - Данные получены')


# In[7]:


# source


# In[8]:


# smooth_params


# In[9]:


products = source['Product'].unique() #[2001:] установить, если потребуется восстановление после сбоя
# pd.DataFrame(products)
# Добавляем к параметрам сглаживания недостающие продукты с параметрами по умолчанию 0,1
smooth_params = smooth_params.merge(pd.DataFrame(products), how='right', left_on='Product', right_on=0).drop(columns=[0])
smooth_params['smooth_level'].fillna(value=0.3, inplace=True)
smooth_params['smooth_trend'].fillna(value=0.1, inplace=True)
# smooth_params
# smooth_params.loc[smooth_params['Product'] == 'Формалин 10%, л', 'smooth_level'].reset_index(drop=True)[0]


# In[10]:


# products


# In[ ]:


t = time.strftime('%x %X', time.localtime(time.time()))
print(f'{t} - старт прогноза')
full_forecast = pd.DataFrame({})
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for num, product in enumerate(products): #['01033563-a80b-11e7-80e8-005056954729']
    # Выбираем исходные данные
        sales = source[source['Product'] == product]['QTY'].reset_index(drop=True)
        smoothing_level = smooth_params.loc[smooth_params['Product'] == product, 'smooth_level'].reset_index(drop=True)[0]
        smoothing_trend = smooth_params.loc[smooth_params['Product'] == product, 'smooth_trend'].reset_index(drop=True)[0]
    # Записываем базовые данные
        base_df = pd.DataFrame(sales)
        base_df.rename(columns={'QTY':'Base-0-0'}, inplace=True)
    # Простое экспоненциальное сглаживание
        ses_model = SimpleExpSmoothing(sales).fit(smoothing_level=smoothing_level, optimized=True)
        ses_smooth = ses_model.fittedfcast[1:]
        ses_df = pd.DataFrame(ses_smooth)
        ses_df.rename(columns={0:f'SES-{smoothing_level}-0'}, inplace=True)
        base_df = pd.concat([base_df, ses_df], axis=1)
    # Экспоненциальное сглаживание Хольта
        hes_model = Holt(sales, exponential=False).fit(smoothing_level=smoothing_level, smoothing_trend=smoothing_trend, optimized=True)
        hes_smooth = hes_model.fittedfcast[1:]
        hes_df = pd.DataFrame(hes_smooth)
        hes_df.rename(columns={0:f'HES-{smoothing_level}-{smoothing_trend}'}, inplace=True)
        base_df = pd.concat([base_df, hes_df], axis=1)
        base_df[base_df < 0] = 0
    # Создаем контрольный прогноз за последние 3 периода
        forcasted_df = return_forcast(base_df, steps=3, steps_back=3)
        forcasted_df_part = forcasted_df[-3:]
        forcasted_df_part = forcasted_df_part.drop(columns=[f'SES-{smoothing_level}-0',f'HES-{smoothing_level}-{smoothing_trend}'])
    # Считаем веса
        if forcasted_df_part.sum()['Base-0-0'] != 0:
            base = forcasted_df_part.sum()['Base-0-0']
        else:
            base = forcasted_df_part.sum().drop(['Base-0-0']).min()
        forecasting_weights = pd.DataFrame(forcasted_df_part.sum())
        forecasting_weights.rename(columns={0:'sum'}, inplace=True)
        forecasting_weights.drop(index=['Base-0-0'], inplace=True)
        def precision(x):
            precis = 1 - abs(x - base)/base
    #         if 0.7 < precis < 1.3:
    #             return precis
    #         else:
    #             return precis
            return precis
        forecasting_weights['weight'] = forecasting_weights['sum'].apply(precision)
        min_precision = forecasting_weights['weight'].quantile(0.7)
        forecasting_weights.loc[forecasting_weights['weight'] <= min_precision,'weight'] = 0
        sum_weight = forecasting_weights.sum()['weight']
    # Делаем полноценный прогноз
        forcasted_df = return_forcast(base_df, steps=12, steps_back=None)
        temp_forecast = pd.DataFrame(forcasted_df['Base-0-0'])
        temp_forecast['Forecast'] = 0
        for i in forcasted_df.index:
            calc = 0
            for type_fcast in forecasting_weights.index:
                calc += float(forcasted_df.loc[i, type_fcast]) * float(forecasting_weights.loc[type_fcast, 'weight']) / sum_weight
            temp_forecast.loc[i,'Forecast'] = calc
        temp_forecast = pd.DataFrame(temp_forecast.loc[:,'Forecast']).tail(12).reset_index(drop=True)
        temp_forecast['Product'] = product
        temp_forecast['Index'] = temp_forecast.index + 1
        temp_forecast['Precision'] = min_precision
        if full_forecast.shape[0] == 0:
            full_forecast = temp_forecast
        else:
            full_forecast = pd.concat([full_forecast,temp_forecast], axis=0, ignore_index=True)
        if (num + 1) % 1000 == 0: #Каждую 1000 продуктов
            t = time.strftime('%x %X', time.localtime(time.time()))
            print(f'{t} - Рассчитан {num + 1} из {len(products)}')
            full_forecast['Period'] = pd.Timestamp(t) #добавляем дату и время
            with engine.connect() as conn:
                full_forecast.to_sql(TABLENAME, conn, if_exists='append', index=False) #добавляем в базу
            full_forecast.drop(full_forecast.index, inplace=True) #чистим записи в прогнозном
t = time.strftime('%x %X', time.localtime(time.time()))
print(f'{t} - Рассчитан {num + 1} из {len(products)}')
full_forecast['Period'] = pd.Timestamp(t)
with engine.connect() as conn:
    full_forecast.to_sql(TABLENAME, conn, if_exists='append', index=False)
t = time.strftime('%x %X', time.localtime(time.time()))
print(f'{t} - Прогноз закончен')


# In[ ]:


TEXT = '#M5K Данные по прогнозу рассчитаны!'
TEXT = urllib.parse.quote(TEXT)
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}')

