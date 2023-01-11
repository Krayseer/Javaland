import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def generate_demand_images(name, title, column):
    fig, ax = plt.subplots()
    x_year = pd.read_csv(f'../files/{name}.csv')['Год'].tolist()

    ax.bar(np.arange(len(x_year)), pd.read_csv(f'../files/{name}.csv')[column].tolist())
    ax.tick_params(axis='x', labelsize=8, rotation=90)
    ax.tick_params(axis='y', labelsize=8)
    ax.set_xticks(np.arange(len(x_year)), x_year)
    ax.set_title(title, fontsize=11)
    ax.grid(axis='y')

    plt.tight_layout()
    plt.savefig(f'../static/graphics/{name}.png')


def generate_skills_image(name, title):
    skills = pd.read_csv(f"../files/{name}.csv")
    fig, ax = plt.subplots()

    ax.bar(range(len(skills['Название'].tolist())), list(skills['Количество'].tolist()), align='center')
    ax.tick_params(axis='x', labelsize=6, rotation=45)
    ax.set_xticks(range(len(skills['Название'].tolist())), list(skills['Название'].tolist()))
    ax.set_title(title, fontsize=11)
    ax.grid(axis='y')

    plt.tight_layout()
    plt.savefig(f'../static/graphics/{name}.png')


def generate_geography_images(name, title, column):
    df = pd.read_csv(f"../files/{name}.csv")
    if title == "Доля вакансий по городам":
        df['Доля вакансий'] = df['Доля вакансий'].apply(lambda x: float(x[:-1]))
    fig, ax = plt.subplots()

    ax.bar(range(len(df['Город'].tolist())), list(df[column].tolist()), align='center')
    ax.tick_params(axis='x', labelsize=6, rotation=45)
    ax.set_xticks(range(len(df['Город'].tolist())), list(df['Город'].tolist()))
    ax.set_title(title, fontsize=11)
    ax.grid(axis='y')

    plt.tight_layout()
    plt.savefig(f'../static/graphics/{name}.png')


# Создать графики из csv файлов
def create_all_images():
    generate_demand_images('salary', 'Динамика уровня зарплат по годам', 'Уровень зарплаты')
    generate_demand_images('vacancy', 'Динамика количества вакансий по годам', 'Количество вакансий')
    generate_demand_images('salary_profession', 'Динамика уровня зарплат по годам для выбранной профессии',
                           'Уровень зарплаты')
    generate_demand_images('vacancy_profession', 'Динамика количества вакансий по годам для выбранной профессии',
                           'Количество вакансий')
    generate_geography_images('level_salary', "Уровень зарплат по городам", "Средняя зарплата")
    generate_geography_images('vacancy_rate', "Доля вакансий по городам", "Доля вакансий")
    generate_skills_image('skills', 'ТОП-10 навыков по годам')
    generate_skills_image('skills_profession', 'ТОП-10 навыков по годам для выбранной профессии')


create_all_images()
