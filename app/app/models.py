from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, default='user')


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)


class Comment(models.Model):
    content = models.TextField()
    author = models.TextField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')