from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import KeysInput_api, QuotCoinInfo_api

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'api/v1/get', MainpageStates_api)
# router.register(r'api/v2/post/', PostRequest_api)


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
    #path('', include(router.urls)),
    path('api/v1/states/', views.add_mainpage_widgets_states_api),
    path('api/v1/get_quot_info/', QuotCoinInfo_api.as_view()),
    path('api/v1/api_keys/', KeysInput_api.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)