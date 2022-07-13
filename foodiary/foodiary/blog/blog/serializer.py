from rest_framework import serializers
from blog.blog.models import Post
from blog.blog.models import Comment
from account.account.serializer import UserSerializer
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post_id", "contents", "created", "updated")


class PostSerializer(serializers.ModelSerializer):
    post = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "title", "auth", "created", "updated", "contents", "post")

class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id", "username")
        
class LikeSerializer(serializers.Serializer):
    id=serializers.IntegerField()