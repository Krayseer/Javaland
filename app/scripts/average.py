import sqlite3


def get_average_salary(element):
    cursor = sqlite3.connect("../../db.sqlite3").cursor()
    salary = list(map(float, list(filter(None, [element.salary_from, element.salary_to]))))
    if element.salary_currency not in ["", "RUR"]:
        query = cursor.execute(f"""SELECT {element.salary_currency} 
        FROM currency_by_month WHERE date = '{element.published_at[:7]}'""")
        ratio = query.fetchone()[0]
        index = float(ratio) if ratio is not None else 1
    else:
        index = 1
    return int(sum(salary) / len(salary) * index) if len(salary) > 0 else None
