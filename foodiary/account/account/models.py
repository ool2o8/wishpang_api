from django.utils import timezone
from django.contrib.auth.models import User


class User(User):
	username = User.username
	password = User.password