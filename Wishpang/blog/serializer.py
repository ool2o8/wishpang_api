from rest_framework import serializers
from blog.models import Post, Product, ProductData
from blog.models import Comment
from account.serializer import UserSerializer
from django.contrib.auth.models import User

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username",)
        
class CommentSerializer(serializers.ModelSerializer):
    auth=AuthSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("id", "post_id", "auth", "contents", "created", "updated")

class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id", "username")

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    liker=LikeUserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "title", "auth", "created", "updated", "contents", "liker", "comment", "product")


class LikeSerializer(serializers.Serializer):
    id=serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductData
        fields="__all__"
        
class ProductDataListSerializer(serializers.ModelSerializer):
    productData=ProductDataSerializer(many=True, read_only=True)
    class Meta:
        model=ProductData
        fields="__all__"
