from django.db import models
from django.contrib.auth.models import User, AbstractUser


class BaseModel(models.Model):
    content = models.TextField()

    class Meta:
        abstract = True

class Post(BaseModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')