from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=10, default="user")


class Comment(models.Model):
    author = models.CharField(max_length=50)
    text = models.TextField()
    user_id = models.IntegerField(default=1)