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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from account.views import CreateUserViewset, logoutView, loginView
from account.views import KaKaoSignInCallBackView, KakaoGetLogin, KakaoGetLogout
from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('login/', auth_views.LoginView.as_view(template_name='account\login.html'), name="login"),
    path('login/', loginView.as_view({'post': 'create'}), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

   	path('api-jwt-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/',
         CreateUserViewset.as_view({'post': 'create'}), name='register'),
    path('api-jwt-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-jwt-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('kakao/login', KakaoGetLogin.as_view()),
    path('kakao/login/callback/', KaKaoSignInCallBackView.as_view()),

    path('kakao/logout', KakaoGetLogout.as_view())

]
