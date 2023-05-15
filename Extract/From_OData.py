import numpy as np, pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth

LOGIN = ''
PASSWORD = ''
ODATASERVER = ''
# Здесь может быть код работы с данными
basic = HTTPBasicAuth(LOGIN.encode('utf-8'), PASSWORD.encode('utf-8'))
refs = 'Ref_Key,Артикул,Code,Description,ЕдиницаИзмерения____Presentation,ЕдиницаИзмерения_Key,био_ОсновнойПоставщик____Presentation,био_ОсновнойПоставщик_Key,СпособОбеспеченияПотребностей____Presentation,СпособОбеспеченияПотребностей_Key,био_СрокПоставкиОтПоставщика,СхемаОбеспечения____Presentation,СхемаОбеспечения_Key,Производитель____Presentation,Производитель_Key,СкладскаяГруппа____Presentation,СкладскаяГруппа_Key,Качество,био_ТемператураТранспортировки____Presentation,био_ТемператураТранспортировки_Key,ОбособленнаяЗакупкаПродажа,ВидНоменклатуры____Presentation,ВидНоменклатуры_Key,НаименованиеПолное,био_Направление____Presentation,био_Направление_Key,Описание,Parent____Presentation,Parent_Key,IsFolder,био_СтранаПроисхождения____Presentation,био_СтранаПроисхождения_Key,ГруппаАналитическогоУчета____Presentation,ГруппаАналитическогоУчета_Key,био_НоменклатураПоставщика____Presentation,био_НоменклатураПоставщика_Key,био_КодОКПД2____Presentation,био_КодОКПД2_Key,био_ОсновнойМенеджер____Presentation,био_ОсновнойМенеджер_Key,СтавкаНДС,био_СкидкаМаксимальная,био_GMМинимальная,СрокГодности,био_КоличествоДнейТранспортировки,био_НаценкаНаДопРасходы,ПодразделениеПартнера____Presentation,ПодразделениеПартнера_Key,био_МинимальныйГарантированныйСрокГодности,ВесЧислитель,ОбъемЧислитель,ТребуетсяЗащитаОтПопаданияСвета,био_Комментарий,био_ТребуетсяПаспортБезопасности,био_НаименованиеДляПаспортаБезопасности,био_ТоварМедНазначения,био_ТехническоеЗадание,био_Прослеживаемость,био_СсылкаНаКТРУ,ГруппаДоступа____Presentation,ГруппаДоступа_Key,ВестиУчетПоГТД,ВесИспользовать,ОбъемИспользовать,ВесЗнаменатель,ОбъемЗнаменатель,био_МИ,ВестиУчетСертификатовНоменклатуры,ЕстьТоварыДругогоКачества,био_ГруппаУправленияЗапасами____Presentation,био_ГруппаУправленияЗапасами_Key,ГруппаФинансовогоУчета____Presentation,ГруппаФинансовогоУчета_Key,био_СреднемесячныйСпрос,био_ДатаСоздания,био_ТекущееРегистрационноеУдостоверение____Presentation,био_ТекущееРегистрационноеУдостоверение_Key,Неликвид,био_Замена,био_КратностьЗамены,ТипНоменклатуры,био_КратностьУпаковки,КодТНВЭД_Key,КодТНВЭД____Presentation'

# Если полей больше 20, то делаем так
refs = refs.replace('Ref_Key,','').replace('Ref_Key','') # поле guid, так как потом его добавим принудительно
ref = refs.split(',') # превращаем в список
dif = 15 # задаем максимальное количество возвращаемых полей
ref_dif = []
if len(ref) // dif > 0:
    for i in range(len(ref) // dif):
        ref_dif.append(','.join(ref[i * dif:i * dif+dif]))
if len(ref) % dif != 0:
    ref_dif.append(','.join(ref[len(ref)- (len(ref) % dif):]))
download_data = pd.DataFrame({})
for i,col in enumerate(ref_dif):
    if col != 'Ref_Key':
        buff_resp = requests.get(f"{ODATASERVER}/Catalog_Номенклатура?$select=Ref_Key,{col}", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
        buff_df = pd.read_json(json.dumps(buff_resp.json()['value']))
        if i == 0:
            download_data = buff_df # при извлечении первой группы полей просто копируем базу
        else:
            download_data = download_data.merge(buff_df, left_on='Ref_Key', right_on='Ref_Key', how='left') # последующие группы добавляем посредством левого соединения

# Если полей меньше 20, то делаем так
buff_resp = requests.get(f"{ODATASERVER}/Catalog_СегментыНоменклатуры?$select={refs}", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
download_data = pd.read_json(json.dumps(buff_resp.json()['value']))