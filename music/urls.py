from django.urls import path
from . import views


app_name = 'music'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('<int:song_id>/vote/', views.vote, name='vote'),
]
