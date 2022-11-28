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
from blog.views import PostViewSet, UserPostView, CommentViewSet, PostLikeView, PostLikeListView, MyProductView, MyProductUpdate, ProductDataView, MyProductDataUpdateView

urlpatterns = [
    path('posts',  PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:pk>', PostViewSet.as_view({'get': 'retrieve'})),

    path('user-posts', UserPostView.as_view()),

    path('posts/<int:pk>/comment',
         CommentViewSet.as_view()),
    path('posts/<int:post_pk>/like', PostLikeView.as_view()),
    path('posts/<int:post_pk>/like-list',
         PostLikeListView.as_view()),
    path('bucket', MyProductUpdate.as_view()),
    path('product/my', MyProductView.as_view({'get':'get'})),
    path('product/<int:product_id>', ProductDataView.as_view({'get':'list'})),
    path('product-data', MyProductDataUpdateView.as_view()),#상품 업데이트
    ]
