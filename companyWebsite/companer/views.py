from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from .models import NavigationElements, BannerContent, Milestones, CompanyOverview, CompanyValue, Service, ClientTestimonial, VideoTestimonial, Project, Category, Newsletter, Blog, User

# Create your views here.


# Default view that the user will see on accessing the web app
def index(request):

    # Getting all the banner content
    banner = BannerContent.objects.first()

    # Returning the rendered data
    return render(request, "companer/index.html", {
        "banner": banner,
    })


# View to get the about route
def about(request):

    # First getting the required data
    milestones = Milestones.objects.all()
    overview = CompanyOverview.objects.first()
    values = CompanyValue.objects.all()

    # Now passing the data to HTML
    return render(request, "companer/about.html", {
        "milestones": milestones,
        "overview": overview,
        "values": values
    })


# View to get the services route
def services(request):

    # Getting all the data
    services = Service.objects.all()
    
    # Rendering the data
    return render(request, "companer/services.html", {
        "services": services
    })


# View to get the clients route
def clients(request):

    # Fetching the required data
    text_testimonials = ClientTestimonial.objects.all()
    video_testimonials = VideoTestimonial.objects.all()

    # Rendering the data
    return render(request, "companer/clients.html", {
        "text_testimonials": text_testimonials,
        "video_testimonials": video_testimonials
    })


# Projects category
def projects(request):

    # Fetching all the required data
    projects = Project.objects.all()
    categories = Category.objects.all()

    # Rendering the required data
    return render(request, "companer/projects.html", {
        "projects": projects,
        "categories": categories
    })


# View to handle newsletter submissions
def newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            # Check if the email is already subscribed
            if not Newsletter.objects.filter(email=email).exists():
                # Save the new subscriber
                Newsletter.objects.create(email=email)
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.warning(request, "This email is already subscribed.")
        return redirect('index')

    return render(request, 'companer/index.html')


# View for displaying all the blogs
def blog(request):

    # Getting all the blog posts
    posts = Blog.objects.all().order_by("-created_at")

    # Rendering said data
    return render(request, "companer/blogs.html", {
        "posts": posts
    })


# View for each individual blog post
def blog_detail(request, blog_id):

    # Getting the said blog
    post = get_object_or_404(Blog, id=blog_id)

    # Rendering said post
    return render(request, "companer/blog_details.html", {
        "post": post,
    })


# View for choosing and contacting us
def contact_choose(request):

    # Rendering the data
    return render(request, "companer/contact_choose.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "companer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "companer/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure passwords match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "companer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "companer/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "companer/register.html")


# HIRING
def hiring(request):

    return render(request, "companer/hiring.html")


# LISTING
def listing(request):

    return render(request, "companer/listing.html")