from django.db import models
from django.urls import translate_url
from django.utils import timezone
from django.contrib.auth.models import User



class Post(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    auth = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE, db_column="user_id")
    title = models.CharField(help_text="Post title",
                             max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, default='')
    updated = models.DateTimeField(auto_now=True, default='')
    contents = models.TextField(
        help_text="post contents", blank=False, null=False)


class Comment(models.Model):
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    post_id = models.ForeignKey(
        Post, related_name="comment", on_delete=models.CASCADE, db_column="post_id")
    contents = models.TextField(
        help_text="Comment contents", blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, default='')
    updated = models.DateTimeField(auto_now=True, default='')
    