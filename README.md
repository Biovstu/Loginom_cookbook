# Loginom_cookbook
Данная "поваренная книга" составлена из необходимых для продуктивной работы в Loginom наработок.
Все наработки разделены на 6 групп:
1. Extract. Содержит блоки для извлечения данных из различных источников
2. Load. Содердит блоки для выгрузки (отправки) данных в различные проемники
3. Logging. Содержит блоки для отправки уведомлений
4. Transform. Содержит блоки для осуществления различного рода преобразований
5. Others. Содержит блоки, не попадающие в другие группы
6. SandBox. Песочница служит для хранения различных черновиков

## 1. <a href="https://github.com/Biovstu/Loginom_cookbook/tree/e9c85ac5a5dcb1d1ab5407a0ade0b0be4ffd743b/Extract">Extract</a>

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td>From_dadata.py</td>
    <td>Получение данных из сервиса DaData</td>
  </tr>
  <tr>
    <td>From_OData.py</td>
    <td>Получение данных web-сервиса 1с посредством интерфейса OData</td>
  </tr>
  <tr>
    <td>From_OData_adding.py</td>
    <td>Обогощение имеющихся данных данными из web-сервиса 1с посредством интерфейса OData</td>
  </tr>
  <tr>
    <td>From_R7.py</td>
    <td>Получение данных из табличного документа Р7</td>
  </tr>
  <tr>
    <td>From_RSS_and_HTML.py</td>
    <td>Получение данных из web-рассылок RSS или HTML-страниц, содержищих таблицы</td>
  </tr>
</table>

## 2. <a href="https://github.com/Biovstu/Loginom_cookbook/tree/e9c85ac5a5dcb1d1ab5407a0ade0b0be4ffd743b/Load">Load</a>

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td>Max_length.py</td>
    <td>Определение максимальной длины записей в столбцах с текстовыми данными перед экспортом в SQL</td>
  </tr>
  <tr>
    <td>To_R7.py</td>
    <td>Создание многостраничного таблиного документа Р7</td>
  </tr>
  <tr>
    <td>To_xlsx.py</td>
    <td>Создание многостраничного табличного документа XLSX</td>
  </tr>
</table>

## 3. <a href="https://github.com/Biovstu/Loginom_cookbook/tree/e9c85ac5a5dcb1d1ab5407a0ade0b0be4ffd743b/Logging">Logging</a>

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td>Sending_in_telegram.py</td>
    <td>Отправка сообщений в телеграм от имени бота</td>
  </tr>
  <tr>
    <td>SendMail.py</td>
    <td>Отправка электронных писем через SMTP соединение</td>
  </tr>
  <tr>
    <td>Send_in_teleg_if.py</td>
    <td>Отправка сообщений в телеграм от имени бота при выполнении условия превышения размеров таблицы</td>
  </tr>
</table>

## 4. <a href="https://github.com/Biovstu/Loginom_cookbook/tree/e9c85ac5a5dcb1d1ab5407a0ade0b0be4ffd743b/Transform">Transform</a>

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td>Clear_fields.py</td>
    <td>Удаление из текстовых полей только непечатных символов, мнжественных пробелов и пробелов в начале и в конце строки</td>
  </tr>
  <tr>
    <td>Find_untypical_symbols.py</td>
    <td>Поиск упоминаний всех символов отличных от буквы или цифры</td>
  </tr>
  <tr>
    <td>IDRRef_to_Ref_Key.py</td>
    <td>Преобразование GUID'а объекта 1С из формата IDRRef в формат Ref_Key используемый OData</td>
  </tr>
  <tr>
    <td>Opening_fields.py</td>
    <td>Раскрытие записей, перечисленных в одной ячейке и разделенных символом</td>
  </tr>
  <tr>
    <td>QTY_unique.py</td>
    <td>Подсчет уникальных строк</td>
  </tr>
  <tr>
    <td>Std_mean_calc.py</td>
    <td>Расчет стандартного отклонения и среднего значения</td>
  </tr>
  <tr>
    <td>String_aggregation.py</td>
    <td>Группировка строковых значений</td>
  </tr>
  <tr>
    <td>TranslitGOST.py</td>
    <td>Транслитреация Русский-Английский по ГОСТ 16876-71</td>
  </tr>
  <tr>
    <td>Unknowing_returns_calc.py</td>
    <td>Распределение неизвестных возвратов, чтобы не образовывались отрицательные значения</td>
  </tr>
</table>

## 5. <a href="https://github.com/Biovstu/Loginom_cookbook/tree/e9c85ac5a5dcb1d1ab5407a0ade0b0be4ffd743b/Others">Others</a>

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td>bot_login.py</td>
    <td>Получение имени и ID пользователя в Телеграме</td>
  </tr>
  <tr>
    <td>CenaNomenklatury.py</td>
    <td>Раскрытие некорректных записей справочника 1С</td>
  </tr>
  <tr>
    <td>input_tables.py</td>
    <td>Костыль для работы со входящими данными</td>
  </tr>
  <tr>
    <td>In_list.py</td>
    <td>Проверка, явлется ли значение ячейки в списке отбора</td>
  </tr>
  <tr>
    <td>output_tables.py</td>
    <td>Костыль для работы со выходными данными</td>
  </tr>
</table>

## 6. SandBox

<table>
  <tr>
    <th>Имя файла</th>
    <th>Назначение</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
</table>
