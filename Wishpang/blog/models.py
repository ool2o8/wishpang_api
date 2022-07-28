from django.db import models
from django.urls import translate_url
from django.utils import timezone
from django.contrib.auth.models import User
import datetime



class Post(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    auth = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE, db_column="user_id")
    title = models.CharField(help_text="Post title",
                             max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    contents = models.TextField(
        help_text="post contents", blank=False, null=False)
    liker = models.ManyToManyField(User, related_name="like_post")

class Comment(models.Model):
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    post= models.ForeignKey(
        Post, related_name="comment", on_delete=models.CASCADE, db_column="post_id")
    contents = models.TextField(
        help_text="Comment contents", blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    auth = models.ForeignKey(User, related_name="comment",
                             on_delete=models.CASCADE, db_column="user_auth")

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Product(models.Model):
    id=models.BigAutoField(help_text="Product id",primary_key=True)
    name=models.CharField(help_text="product name",blank=False, max_length=100, null=False)
    image=models.ImageField(upload_to="image")

class Wish(models.Model):
    id = models.BigAutoField(primary_key=True)
    product=models.ForeignKey(Product,related_name="wish",on_delete=models.CASCADE, db_column="product_id")
    price=models.BigIntegerField(help_text="Product Price")
    wisher=models.ManyToManyField(User, related_name='wish')
    time=models.DateTimeField()