import pandas as pd
import requests
from django.db import models
from app.scripts import average


class Home(models.Model):
    title = models.CharField('Название', max_length=50)
    general = models.TextField('General information')
    scope = models.TextField('Scope application')
    hard_skills = models.TextField('Hard skills')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информация"
        verbose_name_plural = "Домашняя страница"


class Skills(models.Model):
    title = models.CharField('Название', max_length=50)
    content = models.FileField(upload_to='app/admin/skills')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Скиллы"


class Demand(models.Model):
    title = models.CharField('Название', max_length=50)
    content = models.FileField(upload_to='app/admin/demand')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Востребованность"


class ApiVacancies(models.Model):
    date = models.CharField('Дата', max_length=50)

    def __str__(self):
        return 'Дата'

    def get_vacancies_on_page(self, date, page, res):
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

    def create_data_file(self, date):
        result = []
        pages = 20
        [self.get_vacancies_on_page(date, page, result) for page in range(pages)]

        header = ["name", "description", "key_skills", "employer_name", "salary_from", "salary_to", "salary_currency",
                  "area_name", "published_at"]
        rus_header = ["Название вакансии", "Описание вакансии", "Навыки", "Компания", "Оклад",
                      "Название региона", "Дата публикации вакансии"]

        df = pd.DataFrame(result, columns=header).fillna("")
        df = df[df.name.str.lower().str.contains("java") | df.name.str.lower().str.contains("джава") |
                df.name.str.lower().str.contains("ява")]
        df.insert(4, 'salary', df.apply(lambda element: average.get_average_salary(element), axis=1))
        df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
        df.columns = rus_header
        return df

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Последние вакансии"


class Geography(models.Model):
    title = models.CharField('Название', max_length=50)
    content = models.FileField(upload_to='app/admin/geography')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "География"
