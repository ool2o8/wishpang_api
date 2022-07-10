from rest_framework import serializers
from blog.blog.models import Post
from blog.blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post_id", "contents", "created", "updated")


class PostSerializer(serializers.ModelSerializer):
    post = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "title", "auth", "created", "updated", "contents", "post")
