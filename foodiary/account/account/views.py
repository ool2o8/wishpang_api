from django.conf import settings
from django.views import View
from rest_framework import viewsets
from rest_framework.views import APIView
from account.account.serializer import *
from django.contrib.auth.models import User
from account.account.serializer import CreateUserSerializer

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import response, status
from rest_framework.response import Response

import requests
import os, json
from django.core.exceptions import ImproperlyConfigured

from django.http import JsonResponse
from django.db import models
from account.account.models import Profile
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from account.account.serializer import *
from django.contrib.auth import authenticate, login, logout


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


class CreateUserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer
    
    def create(self,request):
        serializer=CreateUserSerializer(request.POST)
        user=User.objects.create(
            username=request.POST.get('username'),
            password=make_password(request.POST.get('password'))
        )
        return Response(serializer.data,status=status.HTTP_200_OK)


class KakaoGetLogin(View):
    def get(self, request):
        REST_API_KEY = get_secret("KAKAO_REST_API_KEY")
        REDIRECT_URI = 'http://127.0.0.1:80/account/kakao/login/callback/'

        API_HOST = f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code'

        return redirect(API_HOST)


class KaKaoSignInCallBackView(APIView):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': get_secret("KAKAO_REST_API_KEY"),
            'redirection_uri': 'http://localhost:80/',
            'code': auth_code
        }

        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')

        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
        user_info=user_info_response.json()
        if not Profile.objects.filter(kakao_id=user_info["id"]).exists():
            user_register_data={
                'username': user_info["id"],
                'password': user_info["properties"]["nickname"]
            }
            user_register_response=requests.post('http://127.0.0.1/account/api-jwt-auth/register/', data=user_register_data)
            profile=Profile.objects.create(user=User.objects.get(username=user_info["id"]), kakao_id=user_info["id"], nickname=user_info["properties"]["nickname"])

        user_data={
                'username': user_info["id"],
                'password': user_info["properties"]["nickname"]
            }
        get_token_response=requests.post('http://127.0.0.1/account/api-jwt-auth/', data=user_data)
        user=authenticate(request, username=user_info["id"], password=user_info["properties"]["nickname"])
        if user is not None:
            login(request, user)
            self.request.session['id'] = user_info['id']
            remember_session = self.request.POST.get('remember_session', False)
        if remember_session:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        token=get_token_response.json()
        res=Response()
        res.set_cookie(key='jwt' ,value=token["access"], httponly=True)
        res.data={
            'jwt': token["access"]
            }
        return res
        # return redirect('http://127.0.0.1/')

class KakaoGetLogout(View):
    def get(self, request):
        REST_API_KEY = get_secret("KAKAO_REST_API_KEY")
        REDIRECT_URI = 'http://127.0.0.1:80/'

        API_HOST = f'http://kauth.kakao.com/oauth/logout?client_id=${REST_API_KEY}&logout_redirect_uri=${REDIRECT_URI}'

        return redirect(API_HOST)


# class kakaoLogoutCallbackView(APIView):
#     def get(self, request):

