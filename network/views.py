from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from .models import User, Posts, Follow, Likes
import json
from django.core.paginator import Paginator


def index(request):
    posts = Posts.objects.all().order_by('-id')

    # Pagination
    paginator = Paginator(posts, 10)
    # Get the current page number, second argument is the default page number
    page_number = request.GET.get('page', 1)
    # Returns a Page object (https://docs.djangoproject.com/en/3.0/ref/paginator/#methods)
    page = paginator.get_page(page_number)
   
    return render(request, "network/index.html", {
        'posts': page, 'paginator': paginator, 'page_number': int(page_number)
    })


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
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        gender = request.POST["gender"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, gender=gender, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == 'POST':
        if (request.POST["message"] != ''):
            create = Posts()
            create.post = request.POST["message"]
            create.user = request.user
            create.save()

    return HttpResponseRedirect(reverse('index'))


def edit_post(request, id):
    if request.method == 'PUT':
        post = Posts.objects.get(id=id)
        # Convert JSON string into a Python Dictionary
        data = json.loads(request.body)
        # Get contents of data (body)
        body = data.get("body")

        post.post = body
        post.save()
            
    return HttpResponseRedirect(reverse('index'))


# Like/Unlike a post
def like(request, id, update):
    # Add/remove likes in database
    if update == 'likes':
        if request.method == 'POST':
            post = Posts.objects.get(id=id)
            
            # Check if the current user already likes the post
            likes = Likes.objects.filter(user=request.user).filter(postid=post.id)
            
            if likes.exists():
                likes.delete()
                # Update the total likes
                post.total_likes = Likes.objects.filter(postid=post.id).count()
                post.save()
            else:
                like_update = Likes()
                like_update.user = request.user
                like_update.postid = post
                like_update.liked = True
                like_update.save()
                # Update the total likes
                post.total_likes = Likes.objects.filter(postid=post.id).count()
                post.save()

    # Get the actual likes from database (Used in JS)
    if update == 'likes-get':
        if request.method == "GET":
            post = Posts.objects.get(id=id)
            # Create a JSON-encoded response with JsonResponse()
            return JsonResponse(post.create_dict())

    return HttpResponseRedirect(reverse('index'))


# Follow/unfollow a user
def follow(request, id, update):
    if update == 'follow':
        if request.method == 'POST':
            # Current user
            current_user = request.user
            # The user who wish to follow/unfollow
            follow_user = User.objects.get(id=id)
            
            # Check if the current user is already following the selected user
            follow = Follow.objects.filter(user_id=current_user.id).filter(following=id)

            if follow.exists():
                follow.delete()
            else:
                follow_update = Follow()
                follow_update.user = current_user
                follow_update.following = follow_user.id
                follow_update.save()

    return HttpResponseRedirect(reverse('index'))


# Page of posts for the following users
def following(request, id):
    # Select current user
    current_user = Follow.objects.filter(user_id=id)
    
    # List of following users by current user
    ids = []
    for post in current_user:
        ids.append(post.following)
    # Filter a list of value with Django's special __in operator
    posts = Posts.objects.filter(user_id__in=ids).order_by('-id')

    # Pagination
    paginator = Paginator(posts, 10)
    # Get the current page number, second argument is the default page number
    page_number = request.GET.get('page', 1)
    # Returns a Page object (https://docs.djangoproject.com/en/3.0/ref/paginator/#methods)
    page = paginator.get_page(page_number)
   
    return render(request, "network/following.html", {
        'posts': page, 'paginator': paginator, 'page_number': int(page_number)
    })
    

# User's profile page
def profile(request, id):
    profile = User.objects.get(id=id)
    posts = Posts.objects.all().filter(user_id=id).order_by('-id')
    # is_follow is for the initial follow/unfollow button to load 
    is_follow = Follow.objects.filter(user_id=request.user.id).filter(following=id)
    # Number of followers
    follower = Follow.objects.filter(following=id).count()
    # Number of following
    following = Follow.objects.filter(user_id=id).count()

    # Pagination
    paginator = Paginator(posts, 10)
    # Get the current page number, second argument is the default page number
    page_number = request.GET.get('page', 1)
    # Returns a Page object (https://docs.djangoproject.com/en/3.0/ref/paginator/#methods)
    page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        'profile': profile, 'posts': page, 'is_follow': is_follow, 'follower': follower, 
        'following': following, 'paginator': paginator, 'page_number': int(page_number)
    })

