from rest_framework import viewsets

from blog.blog.models import Post
from blog.blog.models import Comment
from blog.blog.serializer import PostSerializer
from blog.blog.serializer import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def retrieve(self, request, pk):
        queryset = Post.objects.filter(id=pk).values()
        return super().retrieve(request, pk)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer