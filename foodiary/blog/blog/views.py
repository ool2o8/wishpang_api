from requests import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from blog.blog.models import Post
from blog.blog.models import Comment
from blog.blog.serializer import PostSerializer
from blog.blog.serializer import CommentSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

from rest_framework import status
from rest_framework.response import Response

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly]
    authentication_classes=[SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(auth=request.user.id).values()
        return super().list(request, *args, **kwargs)
    def create(self, request):
        queryset=Post.objects.create(
            title=request.POST.get('title'),
            contents=request.POST.get('contents'),
            auth=request.user
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def retrieve(self, request, pk):
        queryset = Post.objects.filter(id=pk).values()
        return super().retrieve(request, pk)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer