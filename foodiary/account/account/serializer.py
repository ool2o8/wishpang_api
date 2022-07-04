from rest_framework import serializers
from account.account.models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username", "password")