from django.forms import CharField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User, BaseUserManager
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nickname = models.TextField(max_length=50, null=True)
	kakao_id = models.BigIntegerField(null=False)

class Coupang(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	username=models.CharField(max_length=128, null=False)
	password=models.CharField(max_length=128, null=False)