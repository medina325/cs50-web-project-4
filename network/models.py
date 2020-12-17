from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_pic_url = models.URLField(default="https://i.imgur.com/HglJAz8.jpeg")
    followers = models.ManyToManyField("self", related_name="followers", blank=True)
    following = models.ManyToManyField("self", related_name="following", blank=True)
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

    def serialize(self):
        return {
            "id": self.id,
            "likers": [liker.username for liker in self.likers.all()],
            "poster": self.poster.username,
            "url": self.poster.profile_pic_url,
            "number_likes": self.number_likes,
            "content": self.content,
            "creation_date": self.creation_date.strftime("%b %#d %Y, %#I:%M %p"),
        }

    def __str__(self):
        return f"{self.poster.username}"
