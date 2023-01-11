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
