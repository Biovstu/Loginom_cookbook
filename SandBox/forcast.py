#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


import openpyxl


# # Получение набора данных

# In[3]:


source = pd.read_excel('C:\\Users\\konstantin_kutovoy\\Documents\\BioVstu\\Регулярные\\forcast.xlsx', sheet_name='Лист2')


# In[4]:


source


# In[5]:


pd.DataFrame(source['Продукт'].unique())


# # Autoregression (AR)

# In[6]:


# AR example
from statsmodels.tsa.ar_model import AutoReg
from random import random
# contrived dataset
data = [x + random() for x in range(10, 100)]
data


# In[7]:


len(data)


# In[8]:


# fit model
model = AutoReg(data, lags=12)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(data), len(data)+11)
print(yhat)


# In[9]:


len(yhat)


# In[10]:


df1 = pd.DataFrame(data)
df1.rename(columns={0:'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)


# In[11]:


df = pd.concat([df1, df2], axis=0, ignore_index=True)
df


# In[12]:


plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# Таким образом сделаем вывод о настройках функция
# model.fit().predict(s, qty)
# возвращаяет массив прогнозных значений начиная с позиции s в количестве qty

# При этом в качестве нулевого значения выводит NaN

# Функция имеет следующие параметры:
# class statsmodels.tsa.ar_model.AutoReg(
# endog,
# lags,
# trend='c',
# seasonal=False,
# exog=None,
# hold_back=None,
# period=None,
# missing='none',
# *,
# deterministic=None,
# old_names=False)

# ## Проверим на примере Изопрепа

# In[13]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во']
sr


# In[14]:


# fit model
model = AutoReg(sr, lags=12)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
print(yhat)


# In[15]:


df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)


# In[16]:


df = pd.concat([df1, df2], axis=0, ignore_index=True)
df


# In[17]:


plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# ## Проверим на примере Формалина

# In[18]:


sr = source[source['Продукт'] == 'Формалин 10%, л']['Кол-во'].reset_index(drop=True)
# fit model
model = AutoReg(sr, lags=12)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[19]:


df.tail(12)


# В обоих случаях алгоритм на прогнозный период как бы асимптотиески приводит к некой средней величине.<p>
# Которую выдно, если указать значение параметра lag=0

# In[20]:


sr = source[source['Продукт'] == 'Формалин 10%, л']['Кол-во'].reset_index(drop=True)
# fit model
model = AutoReg(sr, lags=12, trend='n')
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# Разные значения параметра trend дают различный результат.<p>
# Наилучшее значение при значении 'ct'

# In[21]:


sr = source[source['Продукт'] == 'Формалин 10%, л']['Кол-во'].reset_index(drop=True)
# fit model
model = AutoReg(sr, lags=12, trend='ct')
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# А в комбинации с lag=0, в результате получается трендовая прямая<p>
# Видимо к ней график снова и стремиться асимптотически

# In[22]:


sr = source[source['Продукт'] == 'Формалин 10%, л']['Кол-во'].reset_index(drop=True)
# fit model
model = AutoReg(sr, lags=0, trend='ct')
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(0, len(sr)-1)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Trend'}, inplace=True)
df = pd.concat([df1, df2], axis=1)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Trend'], label='Trend')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# # Moving Average (MA)

# In[24]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
# MA example
from statsmodels.tsa.arima.model import ARIMA
# fit model
model = ARIMA(sr, order=(0, 0, 1), enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[27]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
# MA example
# from statsmodels.tsa.arima.model import ARIMA
# fit model
model = ARIMA(sr, order=(0, 0, 12), trend='ct', enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# Аналогично подбираем лучшее значение параметра trend='ct'

# # Autoregressive Moving Average (ARMA)

# In[28]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
# MA example
# from statsmodels.tsa.arima.model import ARIMA
# fit model
model = ARIMA(sr, order=(12, 0, 12), enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[104]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
# MA example
# from statsmodels.tsa.arima.model import ARIMA
# fit model
model = ARIMA(sr, order=(12, 0, 12), trend='ct')
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# # Autoregressive Integrated Moving Average (ARIMA)

# In[105]:


sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
# MA example
# from statsmodels.tsa.arima.model import ARIMA
# fit model
model = ARIMA(sr, order=(12, 1, 12), trend='n')
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11, typ='levels')
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# # Seasonal Autoregressive Integrated Moving-Average (SARIMA)

# In[106]:


# SARIMA example
from statsmodels.tsa.statespace.sarimax import SARIMAX
# contrived dataset
# fit model
sr = source[source['Продукт'] == 'ИзоПреп, л']['Кол-во'].reset_index(drop=True)
model = SARIMAX(sr, order=(1, 1, 1), seasonal_order=(12, 0, 12, 2))
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[107]:


model = SARIMAX(sr, order=(1, 1, 1), seasonal_order=(12, 0, 12, 2), trend='ct')
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[108]:


model = SARIMAX(sr, order=(1, 1, 1), seasonal_order=(12, 0, 12, 4), trend='ct')
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[109]:


model = SARIMAX(sr, order=(1, 1, 1), seasonal_order=(12, 0, 12, 6), trend='ct')
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[117]:


model = SARIMAX(sr, order=(1, 1, 1), seasonal_order=(12, 0, 12, 12), trend='ct')
model_fit = model.fit(disp=False)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={'predicted_mean':'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# # Simple Exponential Smoothing (SES)

# In[110]:


# SES example
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

# contrived dataset
data = [x + random() for x in range(1, 100)]
# fit model
model = SimpleExpSmoothing(data)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(data), len(data)+11)
df1 = pd.DataFrame(data)
df1.rename(columns={0:'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# # Holt Winter’s Exponential Smoothing (HWES)

# In[122]:


# contrived dataset
# fit model
model = SimpleExpSmoothing(sr, initialization_method='legacy-heuristic')
model_fit = model.fit(smoothing_level=0.1, optimized=True)
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[115]:


# HWES example
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# contrived dataset

# fit model
model = ExponentialSmoothing(sr, seasonal_periods=4)
model_fit = model.fit()
# make prediction
yhat = model_fit.predict(len(sr), len(sr)+11)
df1 = pd.DataFrame(sr)
df1.rename(columns={'Кол-во':'Base'}, inplace=True)
df2 = pd.DataFrame(yhat)
df2.rename(columns={0:'Forecast'}, inplace=True)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
plt.figure(figsize=(10, 4))
sns.lineplot(x=df.index, y=df['Base'], label='Base')
sns.lineplot(x=df.index, y=df['Forecast'], label='Forecast')
plt.title('Сравнение прогноза')
plt.xlabel('Период')
plt.ylabel('Результат')
plt.legend()
plt.show()


# In[ ]:




