from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('demand/', demand_page),
    path('geography/', geography_page),
    path('skills/', skills_page),
    path('last/', last_vacancies_page),
]
