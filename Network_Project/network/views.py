from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Importing the paginator class from django
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.csrf import csrf_exempt

# My models and Forms i will be using
from .models import User, NewPost
from .forms import NewPostForm


# Function which returns posts in sets of 10
def paginating_poster(posts, page_number):

    # Paginating my posts to ten posts per page
    paginator = Paginator(posts, 10)

    # Trying to get page number
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    return paginated_posts


# Default homepage of the app
def index(request):

    # Getting all the posts
    posts = NewPost.objects.all().order_by("-time")

    # Now getting the page number
    page_number = request.GET.get("page")

    # Paginating the posts
    paginated_posts = paginating_poster(posts, page_number)

    return render(request, "network/index.html", {
        "posts": paginated_posts
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# If user wanna create new posts
@login_required
def new_post(request):

    # If user made a post then
    if request.method == "POST":
        
        # Getting data first
        form_data = NewPostForm(request.POST)

        # Checking if data is valid
        if form_data.is_valid():

            # Creating an instance of the new post to add user
            new_post = form_data.save(commit=False)

            # Assigning the user
            new_post.creator = request.user

            # Saving the data
            new_post.save()

            # Now redirect the user to default page
            return redirect("index")

    # If user got here through get
    else:
        
        # Setting up the form
        form = NewPostForm()
  
    # Redirecting the user
    return render(request, "network/newPost.html", {
        "form": form
    })


# View when a user accesses a profile
def profile_user(request, username):

    # Now getting the user currently logged in
    profile_viewer = get_object_or_404(User, username=username)

    # Checking here if its the user or someone else
    own_user = request.user == profile_viewer

    # Now i will be getting all the posts made by user in reverse order
    posts = NewPost.objects.filter(creator=profile_viewer).order_by("-time")

    # Now getting the page number
    page_number = request.GET.get("page")

    # Calling the paginator function
    paginated_posts = paginating_poster(posts, page_number)

    # Checking if the user is following this person
    is_following = request.user.is_authenticated and request.user.following.filter(id=profile_viewer.id).exists() #type: ignore

    # Returning all the data to the form
    return render(request, "network/profile.html", {
        "username": username,
        "profile_viewer": profile_viewer,
        "own_user": own_user,
        "posts": paginated_posts,
        "is_following": is_following
    })


# When a user wants to follow or not
@csrf_exempt
def toggle_follow(request, username):

    # Checking that the request method was POST
    if request.method == "POST":

        # First getting the user to follow
        user_to_follow = get_object_or_404(User, username=username)

        # Now making a checking to follow or unfollow
        if user_to_follow != request.user:
            if request.user.following.filter(id=user_to_follow.id).exists(): #type: ignore
                request.user.following.remove(user_to_follow)

                # Entering a check
                following_status = False

            else:
                request.user.following.add(user_to_follow)
                following_status = True
            
            # Return the updated follower count
            followers_count = user_to_follow.followers.count()
            return JsonResponse({"following_status": following_status, "followers_count": followers_count})
        
    # If some kinda error arises
    return JsonResponse({"error": "Invalid request"}, status = 400)


# When a user wants to follow or not
def original(request, username):

    # Checking that the request method was PUT
    if request.method == "POST":

        # First getting the user to follow
        user_to_follow = get_object_or_404(User, username=username)

        # Now making a checking to follow or unfollow
        if user_to_follow != request.user:
            if request.user.following.filter(id=user_to_follow.id).exists(): #type: ignore
                request.user.following.remove(user_to_follow)

            else:
                request.user.following.add(user_to_follow)

    # Returning the error JSON response
    return redirect("profile_user", username=username)


# View for user who want to access his followings posts
def following(request):

    # First getting the data from the database
    following_users = request.user.following.all()

    # Now getting the desired posts of the following accounts
    posts = NewPost.objects.filter(creator__in = following_users).order_by("-time")

    # Now getting the page number
    page_number = request.GET.get("page")

    # PAGINATION
    paginated_posts = paginating_poster(posts, page_number)

    # Now sending the data back to template
    return render(request, "network/following.html", {
        "posts": paginated_posts
    })


# First making a view which allows users to edit a post
@login_required
@csrf_exempt
def edit_post(request, post_id):

    # First making sure user got here correctly
    if request.method == "POST":
        
        # Getting the post thats to be edited
        post = get_object_or_404(NewPost, id=post_id)

        # Ensuring that the user is creator of the post
        if post.creator != request.user:
            return JsonResponse({"error": "You are not allowed to edit this post"}, status = 403)
        
        # Get the new content of the post
        new_content = request.POST.get("content", "")

        # Setting the new content
        post.content = new_content

        # Now saving the post
        post.save()

        # Now letting the user know we did id boiz
        return JsonResponse({"message": "Post edited successfully", "content": new_content})
    
    # If some kinda error arises
    return JsonResponse({"error": "Invalid request"}, status = 400)


# Creating API for liking a post
@csrf_exempt
def like_post(request, post_id):

    # First making the post method
    if request.method == "POST":

        # Now getting the post on which user clicked
        post = get_object_or_404(NewPost, id=post_id)

        # Checking if the post is liked
        if post.likes.filter(id=request.user.id).exists():
            
            # Removing the user
            post.likes.remove(request.user)
            liked = False
        
        else:

            # Adding user
            post.likes.add(request.user)
            liked = True
        
        # Now returning JSON response
        return JsonResponse({"liked": liked, "like_count": post.like_count()})
    
    # If some error occured
    return JsonResponse({"Error": "Invalid Request"}, status = 403)