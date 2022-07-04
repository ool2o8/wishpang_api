from rest_framework import viewsets
from account.account.serializer import *
from django.contrib.auth.models import User
from account.account.serializer import CreateUserSerializer

class CreateUserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer

        

