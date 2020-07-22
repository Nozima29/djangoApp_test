from django.urls import path
from . import views


app_name = 'conflict'
urlpatterns = [
    path('', views.create_form, name='create_form'),
]
