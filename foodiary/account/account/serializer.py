from rest_framework import serializers
from account.account.models import Profile, User
from django.contrib.auth.hashers import make_password

class CreateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=("username", "password")

class CreateUserProfile(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("nickname")