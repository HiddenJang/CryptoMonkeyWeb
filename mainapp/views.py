from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import utils
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                context = {'text': f'Пользователь {request.user.username} уже авторизован!'}
                return render(request, 'login_page.html', context)

            else:
                user_login = request.POST['login']
                user_password = request.POST['password']
                user = authenticate(request, username=user_login, password=user_password)
                if user is None:
                    context = {'text': 'Введен неверный логин или пароль!'}
                    return render(request, 'login_page.html', context)

                login(request, user)
                context = {'text': 'Вы успешно авторизованы! Нажмите кнопку <Войти>!'}
                return render(request, 'login_page.html', context)
        except Exception:
            context = {'text': 'Ошибка авторизации!'}
            return render(request, 'login_page.html', context)
    elif request.method == 'GET' and request.user.is_authenticated:
        return render(request, 'app_mainpage.html')
    else:
        return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    context = {'text': 'Вы успешно вышли из системы!'}
    return render(request, 'login_page.html', context)

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
            print('flag1')
            return redirect(logout_page)
        else:
            raise Exception
    except Exception:
        print('flag2')
        context = {'text': 'Ошибка входа! Попробуйте авторизоваться повторно!'}
        return render(request, 'login_page.html', context)
