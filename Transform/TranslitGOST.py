# Транслитерация Русский-Английский по ГОСТ 16876-71

trans = \
{
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'jo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'jj',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shh',
    'ъ': '"',
    'ы': 'y',
    'ь': "'",
    'э': 'eh',
    'ю': 'ju',
    'я': 'ja',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'JO',
    'Ж': 'ZH',
    'З': 'Z',
    'И': 'I',
    'Й': 'JJ',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'KH',
    'Ц': 'C',
    'Ч': 'CH',
    'Ш': 'SH',
    'Щ': 'SHH',
    'Ъ': '"',
    'Ы': 'Y',
    'Ь': "'",
    'Э': 'EH',
    'Ю': 'JU',
    'Я': 'JA',
    '-': '',
    ' ': ''
}

# Импортируем библиотеки
import numpy as np
import pandas as pd
import openpyxl

file_path = ''
sheet = ''
field = ''

# Читаем таблицу из файла
source = pd.read_excel(file_path, sheet_name=sheet)

# Задаем функцю по преобразованию текстовой строки в транслит
def translit(word):
    new_word = ''
    for n,i in enumerate(word):
        if i in trans.keys():
            if word[n-1] in [' ','-'] or n == 0:
                new_word += trans[i].upper()
            else:
                new_word += trans[i]
        else:
            new_word += i
    return new_word

# Добавляем столбец с транслитерируемыми строками
source[field + '_Translit'] = source[field].apply(translit)

# Возвращаем обратно в тот же файл и лист
source.to_excel(file_path, sheet_name=sheet)