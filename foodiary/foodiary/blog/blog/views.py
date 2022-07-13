from django.http import JsonResponse
from django.shortcuts import redirect
from requests import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from blog.blog.models import Post
from blog.blog.models import Comment
from blog.blog.serializer import PostSerializer, LikeUserSerializer, LikeSerializer
from blog.blog.serializer import CommentSerializer
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.auth_id == request.user


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    def get(self, request):
        queryset =Post.objects.filter(auth_id=request.user.id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        queryset=Post.objects.create(
            title=request.POST.get('title'),
            auth=User.objects.get(id=request.user.id),
            contents=request.POST.get('contents')
        )
        serializer = PostSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def list(self, request, pk):
        queryset =Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request, pk):
        queryset = Comment.objects.create(
            auth=User.objects.get(id=request.user.id),
            post_id=Post.objects.get(id=pk),
            contents=request.POST.get('contents')
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#좋아요 기능
class PostLikeView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset=User.objects.all()
    serializer_class=LikeSerializer
    def get(self, request, post_pk):
        if request.user.is_authenticated:
            serializer_class=LikeSerializer
            post = Post.objects.get(id=post_pk)
            serializer = LikeSerializer(post)
            
            if post.liker.filter(pk=request.user.pk).exists():
                post.liker.remove(User.objects.get(id=request.user.id))
            else:
                post.liker.add(User.objects.get(id=request.user.id))
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return redirect('http://127.0.0.1/blog/{post_pk}/post/like-list/')

from account.account.serializer import UserSerializer

class PostLikeListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset=User.objects.all()
    def list(self, request, post_pk):
        queryset =User.objects.filter(like_post=post_pk)
        serializer = LikeUserSerializer(queryset, many=True)
        # if post.liker.filter(pk=request.user.pk).exists():
        return Response(serializer.data, status=status.HTTP_200_OK)