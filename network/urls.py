
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newpost"),
    path("profilePage", views.profile_view, name="profilepage"),
    path("followunfollow", views.follow_unfollow, name="followunfollow"),
    path("likeunlike", views.like_unlike, name="likeunlike"),
    path("followingPage", views.following_view, name="followingpage"),
]
