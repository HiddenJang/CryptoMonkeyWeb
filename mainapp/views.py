from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import utils
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.template.loader import render_to_string

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .models import App_mainpage_states
from .serializers import MainpageStatesSerializer

from rest_framework.renderers import JSONRenderer
import json
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
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                context = {}
                csrf_token = get_token(request)
                context['csrf_token'] = csrf_token
                return render(request, 'app_mainpage.html', context)
            else:
                context = {'text': 'Необходимо авторизоваться перед входом!'}
                return render(request, 'login_page.html', context)
        elif request.method == 'POST':
            print(f'Нажата кнопка ЗАГРУЗИТЬ ДАННЫЕ!')
            mainpage_data = dict(request.POST)
            mainpage_data.pop('csrfmiddlewaretoken')
            for data in mainpage_data:
                elementsState = App_mainpage_states()
                elementsState.elementName = data
                elementsState.elementValue = mainpage_data[data][0]
                elementsState.save()
            return redirect(app_mainpage)
        else:
            raise Exception
    except Exception as ex:
        print(f'mainpage except {ex}')
        context = {'text': 'Ошибка входа! Попробуйте авторизоваться повторно!'}
        return render(request, 'login_page.html', context)

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

#_____________API______________#

class MainpageStates_api(APIView):

    def post(self, request):
        mainpage_data = dict(request.POST)
        print(mainpage_data)
        mainpage_data.pop('csrfmiddlewaretoken', 'key not found')
        for data in mainpage_data:
            if App_mainpage_states.objects.filter(elementName=data).exists():
                elementsState = App_mainpage_states.objects.filter(elementName=data).first()
                elementsState.elementValue = mainpage_data[data][0]
                print('Row updated')
            else:
                elementsState = App_mainpage_states()
                elementsState.elementName = data
                elementsState.elementValue = mainpage_data[data][0]
                print('Row created')
            elementsState.save()
        return JsonResponse({"Success": "true"}, status=200)

class ApikeysInput_api(APIView):

    def get(self, request):
        context = {}
        csrf_token = get_token(request)
        context['csrf_token'] = csrf_token
        return JsonResponse({"Html": render_to_string("login_page.html", context)})


# class PostRequest_api(viewsets.ModelViewSet):
#     queryset = App_mainpage_states.objects.all()
#     serializer_class = MainpageStatesSerializer
#     http_method_names = ['post']


# @api_view(['GET'])
# def mainpageStates_api(request):
#     app_mainpage_states = App_mainpage_states.objects.all()
#     serializer = MainpageStatesSerializer(app_mainpage_states, many=True)
#     return Response(serializer.data)