from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('home/', views.login_page, name='login_page'),
    path('login_page', views.login_page, name='login_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('registration', views.registration_page, name='registration_page'),
    path('registration/', views.registration_page, name='registration_page'),
    path('app_mainpage', views.app_mainpage, name='app_mainpage'),
    path('app_mainpage/', views.app_mainpage, name='app_mainpage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)