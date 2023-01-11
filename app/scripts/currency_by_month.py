import datetime
import sqlite3
import pandas as pd
import requests
import xmltodict


# Создать таблицу currency_by_month с валютами в базе данных
def create_file_currency_by_month():
    df = pd.read_csv("../files/vacancies_with_skills.csv", low_memory=False)
    connection = sqlite3.connect("../../db.sqlite3")

    min_month = 1
    max_month = 12
    min_date = int(datetime.datetime.strptime(df.published_at.min(), '%Y-%m-%dT%H:%M:%S+%f').year)
    max_date = int(datetime.datetime.strptime(df.published_at.max(), '%Y-%m-%dT%H:%M:%S+%f').year)
    currencies = set(df.salary_currency.dropna().tolist())

    correct_vacancies = []
    for year in range(min_date, max_date + 1):
        for month in [f'{x:02}' for x in range(min_month, max_month + 1)]:
            response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month}/{year}')
            response_info = xmltodict.parse(response.content)
            vacancy = {'date': f'{year}-{month}'}
            for index in response_info['ValCurs']['Valute']:
                if index['CharCode'] in currencies:
                    nominal = float(index['Nominal'].replace(',', '.'))
                    value = float(index['Value'].replace(',', '.'))
                    vacancy[index['CharCode']] = round(value / nominal, 7)
                    vacancy['GEL'] = 27.04
            correct_vacancies.append(vacancy)

    pd.DataFrame(correct_vacancies).to_sql("currency_by_month", con=connection, index=False)


create_file_currency_by_month()
