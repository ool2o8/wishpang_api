"""blog URL Configuration

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
from django.contrib import admin
from django.urls import path
from blog.blog.views import PostViewSet, UserPostView, CommentViewSet, PostLikeView, PostLikeListView

urlpatterns = [
    path('post/',  PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('post/<int:pk>', PostViewSet.as_view({'get': 'retrieve'})),

    path('my-post/', UserPostView.as_view()),

    path('post/<int:pk>/comment/',CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('post/<int:post_pk>/like/', PostLikeView.as_view()),
    path('post/<int:post_pk>/like-list/', PostLikeListView.as_view({'get':'list'}))
]
