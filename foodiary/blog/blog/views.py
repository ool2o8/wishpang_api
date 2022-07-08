from requests import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from blog.blog.models import Post
from blog.blog.models import Comment
from blog.blog.serializer import PostSerializer
from blog.blog.serializer import CommentSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly]
    authentication_classes=[SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def retrieve(self, request, pk):
        queryset = Post.objects.filter(id=pk, ).values()
        return super().retrieve(request, pk, headers={"Authorization": f'Bearer ${access_token}'})


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer