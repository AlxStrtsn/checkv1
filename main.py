import json
import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from pathlib import Path

directory = 'in'
source_dir = Path(directory)
target_dir = Path('in_')

str1 = ''

df = pd.DataFrame([])
q = 0

for i in os.scandir(directory):  # сканирование директории
    with open(i, encoding='UTF-8') as json_file:
        # try:
        data = json.load(json_file)
    q = q + 1

    j = len(data[0]['ticket']['document']['receipt']['items'])

    date = data[0]['createdAt'].split("T")[0]   # дата  dd-mm-yy    2024-05-01T15:22:00+03:00  -> 2024-05-01
    time = data[0]['createdAt'].split("T")[1]   #                   2024-05-01T15:22:00+03:00  -> 15:22:00+03:00
    time = time.split("+")[0]                   # время hh-mm-ss    15:22:00+03:00             -> 15:22:00

    if "operatorInn" in data[0]['ticket']['document']['receipt']:
        operatorInn = data[0]['ticket']['document']['receipt']['operatorInn']
    else:
        operatorInn = "0"

    if "retailPlaceAddress" in data[0]['ticket']['document']['receipt']:
        retailPlaceAddress = data[0]['ticket']['document']['receipt']['retailPlaceAddress']
    else:
        retailPlaceAddress = "0"

    if "operator" in data[0]['ticket']['document']['receipt']:
        operator = data[0]['ticket']['document']['receipt']['operator']
    else:
        operator = "0"


    #TODO сделать процедуру работа с числом и перевод в строку
    #TODO вычиления в коде, таблица в коде

    print(q, "\t", i)
    for k in range(j):
        df2 = { '№': '=СТРОКА()-СТРОКА(Т_ГлавнаяТаблица[[#Заголовки];[№]])',
                'Чек кол-во': q,
                'Файл': i,
                'Дата': date,
                'Месяц': '=ТЕКСТ(E3;"ММММ")',
                'ДеньМесяца': '=ДЕНЬ(E3)',
                "Время": time,
                "_id": data[0]['_id'],
                "Магазин по чеку (организация)": data[0]['ticket']['document']['receipt']['user'],
                'Магазин по чеку': data[0]['ticket']['document']['receipt']['retailPlace'],
                'Магазин': "",
                'Магазин тип': "",
                'Товар по чеку': str(data[0]['ticket']['document']['receipt']['items'][k]['name']).strip(),
                'Товар краткое наименование': '=ВПР(N3;Таблица_товаров!C:D;2;0)',
                'Товарная групп': '=ВПР(O3;Таблица_товаров!D:E;2;0)',
                'Товар тип': "",
                'Цена': str(data[0]['ticket']['document']['receipt']['items'][k]['price'] / 100).replace('.', ','),
                'Количество': str(data[0]['ticket']['document']['receipt']['items'][k]['quantity']).replace('.', ','),
                "Сумма": str(data[0]['ticket']['document']['receipt']['items'][k]['sum'] / 100).replace('.', ','),
                'Сумма чека': str(data[0]['ticket']['document']['receipt']['totalSum'] / 100).replace('.', ','),
                'paymentType': data[0]['ticket']['document']['receipt']['items'][k]['paymentType'],
                'userInn': str(data[0]['ticket']['document']['receipt']['userInn']),
                'kktRegId': str(data[0]['ticket']['document']['receipt']['kktRegId']),
                'metadata_id': str(data[0]['ticket']['document']['receipt']['metadata']['id']),
                'ofdId': str(data[0]['ticket']['document']['receipt']['metadata']['ofdId']),
                'Адрес магазина 1 (address)': data[0]['ticket']['document']['receipt']['metadata']['address'],
                'Адрес магазина 2 (retailPlaceAddress)': retailPlaceAddress,
                'receiveDate': data[0]['ticket']['document']['receipt']['metadata']['receiveDate'],
                'operator': operator,
                'numberKkt': str(data[0]['ticket']['document']['receipt']['numberKkt']),
                'fiscalSign': str(data[0]['ticket']['document']['receipt']['fiscalSign']),
                'operatorInn': str(operatorInn),
                'fiscalDriveNumber': str(data[0]['ticket']['document']['receipt']['fiscalDriveNumber']),
                'messageFiscalSign': (data[0]['ticket']['document']['receipt']['messageFiscalSign']),
                'fiscalDocumentNumber': str(data[0]['ticket']['document']['receipt']['fiscalDocumentNumber']),
                'user_data_id': str(data[0]['ticket']['document']['receipt']['user_data']['id'])
               }
        df = df._append(df2, ignore_index=True)

df = df.sort_values(["Дата", "Время"])

#df['№'] = range(1, len(df)+1)

print(tabulate(df, headers='keys', tablefmt='psql'))

#dateN = datetime
timeN = datetime.now()
#print(timeN.strptime("%H-%M-%S"))
print(timeN.strftime("%Y.%m.%d_%H-%M-%S"))

df.to_csv(timeN.strftime("%Y.%m.%d_%H-%M-%S")+'example6.txt', sep='\t', index=False)


# Создаём целевую папку, если её нет
target_dir.mkdir(exist_ok=True)

# Перемещаем все *-файлы
for file in source_dir.glob('*'):
    new_path = target_dir / file.name  # Сохраняем имя файла
    try:
        file.rename(new_path)
        print("Файл успешно перемещён!")
    except FileNotFoundError:
        print("Исходный файл не найден!")
    except PermissionError:
        print("Нет прав на перемещение!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
