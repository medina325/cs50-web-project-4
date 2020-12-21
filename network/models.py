from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, profile_pic_url, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.username = username
        user.profile_pic_url = profile_pic_url
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, profile_pic_url=None, password=None):
        user = self.create_user(
            email,
            username=username,
            profile_pic_url=profile_pic_url,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, default="default@default.com")
    username = models.TextField(unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    # Custom fields
    followers = models.ManyToManyField("self", related_name="following", blank=True, symmetrical=False)
    profile_pic_url = models.URLField()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'profile_pic_url'] # USERNAME_FIELD and password are already required by default

    objects = UserManager()

    # Methods for the user
    def __str__(self):
        return f"{self.username}"

    # def get_full_name(self):
    #     return f"{self.username}"

    # def get_short_name(self):
    #     return f"{self.username}" 

    def has_perm(self, perm, obje=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


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
        return f"{self.poster.username}-{self.id}"
