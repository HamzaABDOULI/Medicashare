from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',include('home.urls')),
    path('',include('user.urls')),
]