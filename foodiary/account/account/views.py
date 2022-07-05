from django.views import View
from rest_framework import viewsets
from account.account.serializer import *
from django.contrib.auth.models import User
from account.account.serializer import CreateUserSerializer

class CreateUserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests
import os, json
from django.core.exceptions import ImproperlyConfigured

from django.http import JsonResponse

secret_file = os.path.join(r"C:\side_project\foodiary\foodiary\foodiary",'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

class KakaoGetLogin(View):
    def get(self, request):
        REST_API_KEY = get_secret("KAKAO_REST_API_KEY")
        REDIRECT_URI = 'http://127.0.0.1:80/account/kakao/login/callback/'

        API_HOST = f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code'

        return redirect(API_HOST)


class KaKaoSignInCallBackView(View):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': get_secret["KAKAO_REST_API_KEY"],
            'redirection_uri': 'http://localhost:80/account/kakao/callback',
            'code': auth_code
        }

        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')

        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

        return JsonResponse({"user_info": user_info_response.json()})
