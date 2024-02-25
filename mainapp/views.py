from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import settings
from .models import App_mainpage_states

from .services.login_and_registration_service import EntranceService
from .services.quote_info_service import QuoteInfo

import logging



logger = logging.getLogger('CryptoMonkeyWeb.views')

#_____________Page render views______________#

def login_page(request):
    login_result = EntranceService(request).login_user()
    if login_result["result"]:
        return redirect(login_result["page"])
    else:
        return render(request, login_result["page"], login_result["context"])

def registration_page(request):
    reg_result = EntranceService(request).registrate_user()
    if reg_result["result"]:
        return redirect(reg_result["page"])
    else:
        return render(request, reg_result["page"], reg_result["context"])

def logout_page(request):
    logout(request)
    return redirect(login_page)

@login_required(login_url='login_page')
def app_mainpage(request):
    if request.method == 'GET':
        return render(request, 'app_mainpage.html')
    else:
        return redirect(login_page)


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
        pars_data = {}
        pars_data["parsData"] = await QuoteInfo().get_coins_data(mainpage_settings)
        return JsonResponse(pars_data, status=200)


class KeysInput_api(APIView):
    """Контроллер получения ключей API криптобиржи для автоматической торговли"""
    def post(self, request):
        settings.API_KEYS[dict(request.POST)["APIkeysInputWindow_dropList_exchangeType"][0]] = {
            "api_key": dict(request.POST)["APIkeysInputWindow_textInp_apiKeyInput"][0],
            "secret_key": dict(request.POST)["APIkeysInputWindow_textInp_secretKeyInput"][0]
        }
        return JsonResponse({"Success": "true"}, status=200)


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