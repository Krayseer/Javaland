import sqlite3
import pandas as pd
from average import get_average_salary


# Создать таблицу all_vacancies с обработанной информацией из файла vacancies_with_skills.csv
def create_table_with_salary():
    df = pd.read_csv("../files/vacancies_with_skills.csv", low_memory=False).fillna("")
    df.insert(2, 'salary', df.apply(lambda element: get_average_salary(element), axis=1))
    df.published_at = df.published_at.apply(lambda x: x[:-5])
    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
    df = df[(df.published_at != "2005-02-08T11:11:17") & (df.published_at != "2005-08-15T13:22:01")]
    df.to_sql("all_vacancies", con=sqlite3.connect("../../db.sqlite3"), index=False)


create_table_with_salary()
