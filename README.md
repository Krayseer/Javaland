# Алгоритм работы 
1) Выполняется скрипт currency_by_month, который запоминает, какие валюты встречаются в файле vacancies_with_skills.csv и с помощью api выгружает значения валют за конкретные периоды времени
2) Выполняется скрипт all_vacancies, который создает таблицу "all_vacancies" в базе данных с обработанной информацией из файла vacancies_with_skills.csv
3) Выполняется скрипт processed_data, который формирует csv файлы с обработанной информацией, а именно, с таблицами, которые будут использоваться на страницах сайта
4) Выполняется скрипт generate_images, который создает графики на основе csv файлов, полученных в пункте 3

# Страницы на сайте

## Главная
В админку по разделам фиксируется текст, который будет отображаться на главной странице. А именно разделы: общая информация, область применения, hard skills

## Востребованность
В админку фиксируются названия файлов и сами файлы, например: для файла salary.csv нужно указать название "salary". Файлы, которые должны загружаться в админку: salary.csv, vacancy.csv, salary_profession.csv, vacancy_profession.csv

## География 
Работает наподобие страницы "Востребованность". Файлы, которые должны загружаться в админку: level_salary.csv, vacancy_rate.csv

## Скиллы
Работает наподобие страницы "Востребованность". Файлы, которые должны загружаться в админку: skills.csv, skills_profession.csv

## Последние вакансии
В админке фиксируется дата, по которой из api hh.ru будет выгружаться информация по вакансиям по выбранной профессии. При заходе на страницу срабатывает скрипт api.py, который соответственно и выгружает всю информацию из api hh.ru
