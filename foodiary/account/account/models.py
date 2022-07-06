from django.forms import CharField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(User):
	username=User.username
	password=User.password