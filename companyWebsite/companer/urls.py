from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


# All my website urls for handling data
urlpatterns = [
    # Url for users to loging int
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    
    # Default path of my website which opens everytime
    path("", views.index, name="index"),

    # Path to the about section of the app
    path("about/", views.about, name="about"),

    # Path for the services section
    path("services/", views.services, name="services"),

    # Path for the clients
    path("clients/", views.clients, name="clients"),

    # Path for projects
    path("projects/", views.projects, name="projects"),

    # Handling newsletter requests
    path("newsletter/", views.newsletter, name="newsletter"),

    # Path for the blogs
    path("blog/", views.blog, name="blog"),

    # View for each individual blog
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),

    # View for Contact and choose us Pages
    path("contoose/", views.contact_choose, name="contact_choose"),

    # HIRING
    path("hiring/", views.hiring, name="hiring"),

    # LISTING
    path("listing/", views.listing, name="listing")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

