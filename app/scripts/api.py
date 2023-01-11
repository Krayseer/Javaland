import pandas as pd
import requests


def get_vacancies_on_page(date, page, res):
    path = f'https://api.hh.ru/vacancies?specialization=1&date_from={date}&date_to={date}&page={page}&per_page=100'
    [res.append([element['name'],
                 element['snippet']['responsibility'],
                 element['snippet']['requirement'],
                 element['employer']['name'],
                 element['salary']['from'] if element['salary'] is not None else None,
                 element['salary']['to'] if element['salary'] is not None else None,
                 element['salary']['currency'] if element['salary'] is not None else None,
                 element['area']['name'],
                 element['published_at']]) for element in requests.get(path).json()['items']]


def get_average(element):
    salary = list(map(float, list(filter(None, [element.salary_from, element.salary_to]))))
    summary = int(sum(salary) / len(salary)) if len(salary) > 0 else None
    return f'{summary} {element.salary_currency}' if summary is not None else None


def create_data_file(date):
    result = []
    pages = 20
    [get_vacancies_on_page(date, page, result) for page in range(pages)]

    header = ["name", "description", "key_skills", "employer_name", "salary_from", "salary_to", "salary_currency",
              "area_name", "published_at"]
    rus_header = ["Название вакансии", "Описание вакансии", "Навыки", "Компания", "Оклад",
                  "Название региона", "Дата публикации вакансии"]

    df = pd.DataFrame(result, columns=header).fillna("")
    df = df[df.name.str.lower().str.contains("java") | df.name.str.lower().str.contains("джава") |
            df.name.str.lower().str.contains("ява")]
    df.insert(4, 'salary', df.apply(lambda element: get_average(element), axis=1))
    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency']).fillna("").sort_values('published_at')[:10]
    df.published_at = df.published_at.apply(lambda x: x[:-5])
    df.columns = rus_header
    return df
