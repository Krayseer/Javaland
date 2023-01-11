from django.shortcuts import render
from app.models import *


def index_page(request):
    data = {
        'general': Home.objects.get(id=1).general.split('\r\n'),
        'scope': Home.objects.get(id=1).scope.split('\r\n'),
        'hard_skills': Home.objects.get(id=1).hard_skills.split('\r\n')
    }
    return render(request, 'index.html', context=data)


def skills_page(request):
    data = {
        'skills': pd.read_csv(Skills.objects.get(title='skills').content).to_html(index=False),
        'skills_profession': pd.read_csv(Skills.objects.get(title='skills_profession').content).to_html(index=False)
    }
    return render(request, 'skills.html', context=data)


def demand_page(request):
    data = {
        'salary': pd.read_csv(Demand.objects.get(title='salary').content).to_html(index=False),
        'vacancy': pd.read_csv(Demand.objects.get(title='vacancy').content).to_html(index=False),
        'salary_profession': pd.read_csv(Demand.objects.get(title='salary_profession').content).to_html(index=False),
        'vacancy_profession': pd.read_csv(Demand.objects.get(title='vacancy_profession').content).to_html(index=False)
    }
    return render(request, 'demand.html', context=data)


def last_vacancies_page(request):
    data = {
        'last_vacancies': ApiVacancies().create_data_file(ApiVacancies.objects.get(id=1).date).to_html(index=False)
    }
    return render(request, 'last_vacancies.html', context=data)


def geography_page(request):
    data = {
        'level_salary': pd.read_csv(Geography.objects.get(title='level_salary').content).to_html(index=False),
        'vacancy_rate': pd.read_csv(Geography.objects.get(title='vacancy_rate').content).to_html(index=False)
    }
    return render(request, 'geography.html', context=data)
