from rest_framework import serializers
from blog.models import Post, Product, Wish
from blog.models import Comment
from account.serializer import UserSerializer
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post_id", "contents", "created", "updated")

class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id", "username")

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    liker=LikeUserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "title", "auth", "created", "updated", "contents", "liker", "comment")


class LikeSerializer(serializers.Serializer):
    id=serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        
class WishSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=Wish
        fields="__all__"

class ProductPriceSerializer(serializers.ModelSerializer):
    wish=WishSerializer()
    class Meta:
        model=Product
        fields="__all__"