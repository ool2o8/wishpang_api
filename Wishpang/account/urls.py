"""account URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include

from account.views import CreateUserViewset, logoutView, loginView
from account.views import KaKaoSignInCallBackView, KakaoGetLogin, KakaoGetLogout
from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('login/', auth_views.LoginView.as_view(template_name='account\login.html'), name="login"),
    path('login', loginView.as_view({'post': 'create'}), name="login"),
    path('logout', logoutView.as_view(), name="logout"),

    path('register',
         CreateUserViewset.as_view({'post': 'create'}), name='register'),

    path('kakao/login', KakaoGetLogin.as_view()),
    path('kakao/login/callback', KaKaoSignInCallBackView.as_view()),

    path('kakao/logout', KakaoGetLogout.as_view())

]
