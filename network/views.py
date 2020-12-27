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

# Obs.: I feel like not even I will be able to read lines such as lines 35, 41 and 136
# So the long version of such lines (line 136 in the example below) would be something like this:
# following = list()
# for u in other_users:
#   if user.following.filter(pk=u.id).exists():
#       following.append(True)
#   else:
#       following.append(False)


def index(request):    
    # The idea here is to zip 3 arrays and iterate through them in the template: 
    # 1. The posts
    # 2. For each post a flag saying if the user likes the post or not
    # 3. For each post the number of likes

    posts = Post.objects.order_by("-creation_date")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    # Array of flags that tell what posts the current user likes 
    like_flags = [True if p.likers.filter(pk=request.user.id).exists() else False for p in posts]

    # Array of number of likes per post
    likes_per_post = [p.likers.count() for p in posts]

    return render(request, "network/index.html", {
        "user": request.user,
        "paginator": paginator,
        "previous_pages": [i for i in range(1, page_obj.number)],
        "next_pages": [i for i in range(page_obj.number+1, paginator.num_pages+1)],
        "page_obj": page_obj,
        "posts_flags": zip(page_obj, like_flags, likes_per_post)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

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
            email = request.POST["email"]
            username = request.POST["username"]
            profile_pic_url = request.POST["img_url"]
            
            user = User.objects.create_user(email, username, profile_pic_url, password)
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
        content = data.get("content", "")

        newpost = Post(poster=request.user,
                       content=content
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
def profile_view(request, page_user_id):
    # Current logged user
    user = request.user

    # User having it's profile page displayed
    page_user = User.objects.get(pk=page_user_id) 

    # Other users   
    other_users = User.objects.exclude(pk=page_user.id)

    # Array of flags that tells if the current user is following the other users
    following_flags = [True if user.following.filter(pk=u.id).exists() else False for u in other_users]

    posts = page_user.posts.all()
    # Creating pagination
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    
    # This flag tells if the current user follows the "page user" to determine which button shall be presented 
    # follow or unfollow 
    follow_unfollow_flag = page_user.followers.filter(pk=user.id).exists()
    return render(request, "network/profilePage.html", {
        "user": user,
        "page_user": page_user,
        "follow_unfollow_flag": follow_unfollow_flag, 
        "n_followers": page_user.followers.all().count(),
        "n_following": page_user.following.all().count(),
        "n_posts": page_user.posts.all().count(),
        "posts": posts,
        "other_users_flags": zip(other_users, following_flags),
        "paginator": paginator,
        "previous_pages": [i for i in range(1, page_obj.number)],
        "next_pages": [i for i in range(page_obj.number+1, paginator.num_pages+1)],
        "page_obj": page_obj,
    })


@csrf_exempt
@login_required
def following_view(request):
    user = request.user
    
    # Create ordered list of posts from users being followed by the current user
    following_posts = list()
    for following_user in user.following.all():
        for post in following_user.posts.all():
            following_posts.append(post)

    following_posts.sort(key=lambda post: post.creation_date, reverse=True)

    # Array of flags that tell what posts the current user likes 
    like_flags = [True if p.likers.filter(pk=user.id).exists() else False for p in following_posts]

    # Array of number of likes per post
    likes_per_post = [p.likers.count() for p in following_posts]

    # Creating pagination
    paginator = Paginator(following_posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "network/followingPage.html", {
        "user": user,
        "posts_flags": zip(following_posts, like_flags, likes_per_post),
        "paginator": paginator,
        "previous_pages": [i for i in range(1, page_obj.number)],
        "next_pages": [i for i in range(page_obj.number+1, paginator.num_pages+1)],
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required
def follow_unfollow(request):

    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        
        flag = data.get("flag", "")
        target_user_id = data.get("target_user", "")

        if flag:
            user_to_follow = User.objects.get(pk=target_user_id)
            
            if (user_to_follow.followers.filter(pk=user.id).exists()):
                return JsonResponse({"error": f"{user.username} already follows {user_to_follow.username}"}, status=400)
            
            user_to_follow.followers.add(user)
            user_to_follow.save()
        else:
            user_to_unfollow = User.objects.get(pk=target_user_id)

            if (user_to_unfollow.followers.filter(pk=user.id).exists() == False):
                return JsonResponse({"error": f"{user.username} doesn't follow {user_to_unfollow.username}"}, status=400)
            
            user_to_unfollow.followers.remove(user)
            user_to_unfollow.save()

        return JsonResponse({"message": "Done!"}, status=201)
    
    return JsonResponse({"error": "Method should be PUT"}, status=400)


@csrf_exempt
@login_required
def like_unlike(request):
    
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)

        flag = data.get("flag", "")
        target_post_id = data.get("target_post", "")

        if flag:
            post_to_be_liked = Post.objects.get(pk=target_post_id)

            if (post_to_be_liked.likers.filter(pk=user.id).exists()):
                return JsonResponse({"error": f"{user.username} already likes this post"}, status=400)
            
            post_to_be_liked.likers.add(user)
            post_to_be_liked.save()

            return JsonResponse({"message": "Post liked!"}, status=201)
        else:
            post_to_be_unliked = Post.objects.get(pk=target_post_id)

            if (post_to_be_unliked.likers.filter(pk=user.id).exists() == False):
                return JsonResponse({"error": f"{user.username} already dislikes this post"}, status=400)
            
            post_to_be_unliked.likers.remove(user)
            post_to_be_unliked.save()

            return JsonResponse({"message": "Post disliked!"}, status=201)

    return JsonResponse({"error": "Method should be PUT"}, status=400)


@csrf_exempt
@login_required
def save_edited_post(request):
    
    if request.method == "PUT":
        data = json.loads(request.body)

        post_id = data.get("post_id", "")
        post = Post.objects.get(pk=post_id)
        post.content = data.get("edited_content", "")
        post.save()

        return JsonResponse({"message": "Post edited successfully!"}, status=201)


    return JsonResponse({"error": "Method should be PUT"}, status=400)
