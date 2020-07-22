from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('conflict/', include('conflict.urls')),
    path('music/', include('music.urls')),
    path('admin/', admin.site.urls),
]
