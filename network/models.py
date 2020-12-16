from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    number_followers = models.PositiveIntegerField(default=0)
    number_following = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    likers = models.ManyToManyField("User", related_name="liked_posts", blank=True)

    number_likes = models.PositiveIntegerField(default=0)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.username}"
