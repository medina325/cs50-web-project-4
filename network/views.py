from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    paginator = Paginator(Post.objects.order_by("-creation_date"), 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    
    return render(request, "network/index.html", {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            # user = User.objects.create_user(username, email, password)
            user = User(username=request.POST["username"],
                        email=request.POST["email"],
                        password=password,
                        profile_pic_url=request.POST["img_url"]
                       )
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):
    
    if request.method == "POST":
        data = json.loads(request.body)

        newpost = Post(poster=request.user,
                       content=data.get("content", "")
                      )
        newpost.save()

        return JsonResponse(
            {
                "message": "Post created!",
                "newpost": newpost.serialize(),
            }, 
            status=201
            )
    
    return JsonResponse({"error": "Method should be POST"}, status=400)

@login_required
def profile_view(request):
    user = request.user    
    other_users = User.objects.exclude(pk=user.id)

    # Array of flags that tell if the current user is following the other users
    following_flags = [True if user.following.filter(pk=u.id).exists() else False for u in other_users]

    return render(request, "network/profilePage.html", {
        "user": user,
        "n_followers": user.followers.all().count(),
        "n_following": user.following.all().count(),
        "n_posts": user.posts.all().count(),
        "posts": user.posts.all(),
        "users_flags": zip(other_users, following_flags),
    })

# Obs.: I feel like not even me will be able to read line 105
# So the long version would be:
# following = list()
# for u in other_users:
#   if user.following.filter(pk=u.id).exists():
#       following.append(True)
#   else:
#       following.append(False)