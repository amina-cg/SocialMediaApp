from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostLike(models.Model):
    postlike_user = models.ForeignKey(User, on_delete=models.CASCADE)
    postlike_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # totla_likes =

    def __str__(self):
        return self.postlike_user.username


class PostComment(models.Model):
    postcomment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    postcomment_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # total_comments =

    def __str__(self):
        return self.postcomment_user.username





