"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'res'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('index/<int:pg>/', views.res_index, name='index'),
    path('detail/<int:res_seq>/', views.res_detail),
    path('join/', views.res_join_form),
    path('save/', views.res_join_save, name='join_save'),
    path('write/', views.write, name='write'),
    path('write_save/', views.write_save, name='write_save'),
    path('logon/', views.logon, name='logon'),
    path('logout/', views.logout, name='logout'),
    path('deletepost/', views.deletepost, name='deletepost/'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)