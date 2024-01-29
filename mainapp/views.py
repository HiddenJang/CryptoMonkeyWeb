from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import utils
from django.contrib.auth.decorators import login_required
from .models import App_mainpage_states

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MainpageStatesSerializer
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
                return render(request, 'app_mainpage.html')
            else:
                context = {'text': 'Необходимо авторизоваться перед входом!'}
                return render(request, 'login_page.html', context)
        elif request.method == 'POST':
            print(f'Нажата кнопка ЗАГРУЗИТЬ ДАННЫЕ!')
            print(f'{request.POST}')
            mainpage_data = dict(request.POST)
            mainpage_data.pop('csrfmiddlewaretoken')
            for data in mainpage_data:
                print(data)
                elementsState = App_mainpage_states()
                elementsState.widget = data.split('_')[0]
                elementsState.elementType = data.split('_')[1]
                elementsState.elementValue = mainpage_data[data][0]
                elementsState.save()
            return redirect(app_mainpage)
        else:
            raise Exception
    except Exception:
        context = {'text': 'Ошибка входа! Попробуйте авторизоваться повторно!'}
        return render(request, 'login_page.html', context)

class MainpageStates_api(APIView):

    def get(self, request):
        states = App_mainpage_states.objects.all()
        serializer = MainpageStatesSerializer(states, many=True)
        return Response(serializer.data)