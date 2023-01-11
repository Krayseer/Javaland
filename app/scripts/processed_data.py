import sqlite3
import pandas as pd


def create_demand_csv(cursor):
    salary = cursor.execute("""
        SELECT STRFTIME('%Y', published_at) AS datetime, ROUND(AVG(salary), 2) FROM all_vacancies
        GROUP BY datetime;
        """)
    df = pd.DataFrame(salary.fetchall(), columns=['Год', 'Уровень зарплаты'])
    df.to_csv("../files/salary.csv", index=False)

    vacancy = cursor.execute("""
        SELECT STRFTIME('%Y', published_at) AS datetime, COUNT(*) FROM all_vacancies
        GROUP BY datetime;
        """)
    df = pd.DataFrame(vacancy.fetchall(), columns=['Год', 'Количество вакансий'])
    df.to_csv("../files/vacancy.csv", index=False)

    salary_profession = cursor.execute(f"""
        SELECT STRFTIME('%Y', published_at) AS datetime, ROUND(AVG(salary), 2) FROM all_vacancies
        WHERE (name LIKE '%java%' OR name LIKE '%джава%' OR name LIKE '%ява%')
        GROUP BY datetime;
        """)
    df = pd.DataFrame(salary_profession.fetchall(), columns=['Год', 'Уровень зарплаты'])
    df.to_csv("../files/salary_profession.csv", index=False)

    vacancy_profession = cursor.execute(f"""
        SELECT STRFTIME('%Y', published_at) AS datetime, COUNT(*) FROM all_vacancies
        WHERE (name LIKE '%java%' OR name LIKE '%джава%' OR name LIKE '%ява%')
        GROUP BY datetime;
        """)
    df = pd.DataFrame(vacancy_profession.fetchall(), columns=['Год', 'Количество вакансий'])
    df.to_csv("../files/vacancy_profession.csv", index=False)


def create_geography_csv(cursor):
    percent_of_areas = int(cursor.execute("SELECT COUNT(area_name) FROM all_vacancies").fetchone()[0] / 100)
    vacancy_rate = cursor.execute(f"""
        SELECT area_name, ROUND(CAST(COUNT(area_name) AS REAL) / {percent_of_areas}, 2) AS percent FROM all_vacancies
        GROUP BY area_name
        HAVING COUNT(area_name) > {percent_of_areas}
        ORDER BY percent DESC
        """)
    df = pd.DataFrame(vacancy_rate.fetchall(), columns=['Город', 'Доля вакансий'])
    df['Доля вакансий'] = df['Доля вакансий'].apply(lambda x: str(x) + "%")
    df.to_csv("../files/vacancy_rate.csv", index=False)

    level_salary = cursor.execute(f"""
        SELECT area_name, ROUND(AVG(salary), 0) as average FROM all_vacancies
        GROUP BY area_name
        HAVING COUNT(area_name) > {percent_of_areas}
        ORDER BY average DESC
        """)
    df = pd.DataFrame(level_salary.fetchall(), columns=['Город', 'Средняя зарплата'])
    df.to_csv("../files/level_salary.csv", index=False)


def create_skills_csv(cursor, on_profession):
    name = 'skills_profession' if on_profession else 'skills'
    query = "SELECT key_skills FROM all_vacancies WHERE key_skills IS NOT ''" if not on_profession else \
            """SELECT key_skills FROM all_vacancies WHERE key_skills IS NOT ''
            AND (name LIKE '%java%' OR name LIKE '%джава%' OR name LIKE '%ява%')"""
    result = {}
    skills = cursor.execute(query)
    df = pd.DataFrame(skills.fetchall(), columns=['key_skills'])
    for line in df.key_skills.tolist():
        for word in line.split('\n'):
            if word not in result:
                result[word] = 0
            result[word] += 1
    skills_dict = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])
    frame = {'Название': list(skills_dict.keys()), 'Количество': list(skills_dict.values())}
    pd.DataFrame(frame).to_csv(f"../files/{name}.csv", index=False)


# Получить всю необходимую аналитику из таблицы all_vacancies
def create_processed_csv_files():
    cursor = sqlite3.connect("../../db.sqlite3")

    create_demand_csv(cursor)
    create_geography_csv(cursor)
    create_skills_csv(cursor, False)
    create_skills_csv(cursor, True)


create_processed_csv_files()
