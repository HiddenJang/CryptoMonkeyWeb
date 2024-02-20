from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import utils
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.template.loader import render_to_string

from rest_framework.views import APIView
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import async_only_middleware
from rest_framework.response import Response

from asgiref.sync import async_to_sync

from .models import App_mainpage_states
from .serializers import MainpageStatesSerializer

from rest_framework.renderers import JSONRenderer

import logging
import asyncio


from .services.quote_info_service import QuoteInfo

logger = logging.getLogger('CryptoMonkeyWeb.views')

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                return redirect(app_mainpage)

            else:
                user_login = request.POST['login']
                user_password = request.POST['password']
                user = authenticate(request, username=user_login, password=user_password)
                if user is None:
                    context = {'text': 'Введен неверный логин или пароль!'}
                    return render(request, 'login_page.html', context)

                login(request, user)
                return redirect(app_mainpage)
        except Exception:
            context = {'text': 'Ошибка авторизации!'}
            return render(request, 'login_page.html', context)
    elif request.method == 'GET' and request.user.is_authenticated:
        return redirect(app_mainpage)
    else:
        return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    return redirect(login_page)

def registration_page(request):
    if request.method == 'POST':
        user_login = request.POST['login']
        user_password = request.POST['password']
        first_name = request.POST['name']
        email = request.POST['email']

        try:
            user = User.objects.create_user(user_login, email, user_password, first_name=first_name)
            user.save()
            context = {'text': 'Успешная регистрация! Нажмите кнопку <Войти>!'}
            return render(request, 'login_page.html', context)
        except utils.IntegrityError:
            context = {'text': 'Данный пользователь уже зарегистрирован!'}
            return render(request, 'registration_page.html', context)

    else:
        return render(request, 'registration_page.html')

def app_mainpage(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {}
            csrf_token = get_token(request)
            context['csrf_token'] = csrf_token
            return render(request, 'app_mainpage.html', context)
        else:
            context = {'text': 'Необходимо авторизоваться перед входом!'}
            #return redirect(reverse(login_page, kwargs=context))
            return redirect(login_page)
    else:
        return redirect(app_mainpage)


#_____________API______________#

@api_view(['POST'])
def add_mainpage_widgets_states_api(request):
    """Контроллер добавления/изменения состояний элементов (виджетов) главного окна"""

    App_mainpage_states.add_widgets_states(request)
    return JsonResponse({"Success": "true"}, status=200)

class QuotCoinInfo_api(View):
    """Контроллер получения данных по котировкам криптовалют с выбранных криптобирж"""

    async def post(self, request):
        mainpage_settings = dict(request.POST)
        mainpage_settings.pop('csrfmiddlewaretoken', 'key not found')

        async def func():
            pars_data = await QuoteInfo().get_coins_data(mainpage_settings)
            print(pars_data[0]["data"]["currency"])
            return JsonResponse(pars_data[0], status=200)

        while True:
            await func()
            await asyncio.sleep(3)
        return JsonResponse({"Stoped": "true"}, status=200)


class ApikeysInput_api(APIView):

    def get(self, request):
        context = {}
        csrf_token = get_token(request)
        context['csrf_token'] = csrf_token
        return JsonResponse({"Html": render_to_string("login_page.html", context)})


# @api_view(['POST'])
# @csrf_exempt
# def infoResult(request):
#     if request.method == 'POST':
#         print('infoResult=', request.method, request.POST)
#         mainpage_data = dict(request.POST)
#         return JsonResponse({"mainpage_data": mainpage_data}, safe=False)
#     else:
#         print('редирект на mainpage')
#         return redirect(app_mainpage)


# class PostRequest_api(viewsets.ModelViewSet):
#     queryset = App_mainpage_states.objects.all()
#     serializer_class = MainpageStatesSerializer
#     http_method_names = ['post']


# @api_view(['GET'])
# def mainpageStates_api(request):
#     app_mainpage_states = App_mainpage_states.objects.all()
#     serializer = MainpageStatesSerializer(app_mainpage_states, many=True)
#     return Response(serializer.data)