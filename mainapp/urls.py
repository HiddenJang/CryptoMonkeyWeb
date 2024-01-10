from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('home/', views.login_page, name='login_page'),
    path('login_page', views.login_page, name='login_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('registration', views.registration_page, name='registration_page'),
    path('registration/', views.registration_page, name='registration_page'),
    path('app_mainpage', views.app_mainpage, name='app_mainpage'),
    path('app_mainpage/', views.app_mainpage, name='app_mainpage'),
]