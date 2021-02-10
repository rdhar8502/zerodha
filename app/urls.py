from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('details_page/<code>', details_page, name='details_page'),
    path('details_page/<code>/details_csv', download_csv, name='download_csv'),
    path('api/names', auto_fill, name='auto_fill')
]
