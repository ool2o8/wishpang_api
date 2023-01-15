from django.db import models
from django.urls import translate_url
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Product(models.Model):
    id=models.BigAutoField(help_text="Product id",primary_key=True)
    name=models.CharField(help_text="product name",blank=False, max_length=100, null=False)
    image=models.ImageField(upload_to="images/")
    url=models.CharField(help_text="product url",blank=False, max_length=200, null=False)
    wisher=models.ManyToManyField(User, related_name='product')


class ProductData(models.Model):
    id = models.BigAutoField(primary_key=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_data')
    price=models.BigIntegerField(help_text="Product Price")
    time=models.DateField(auto_now=True)


class Post(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    auth = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE, db_column="user_id")
    title = models.CharField(help_text="Post title",
                             max_length=100, blank=False, null=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
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



