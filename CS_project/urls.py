"""CS_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CS_app import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('/', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index_student/', views.index_student),
    path('search/', views.search),
    path('search_result/', views.search_result),
    path('state/', views.state),
    path('opening/', views.opening),
    path('opening_result/', views.opening_result),
    path('arrange/', views.arrange),
    path('apply/', views.apply),
    path('get_post/', views.get_post),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls'))   # 增加这一行
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
