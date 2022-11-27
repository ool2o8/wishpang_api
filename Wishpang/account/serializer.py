
from rest_framework import serializers
from account.models import Profile, User, Coupang
from django.contrib.auth.hashers import make_password

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username", "password")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username", "password")
        
class CreateUserProfile(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("nickname",)

class CoupangSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupang
        fields=("username", "password")