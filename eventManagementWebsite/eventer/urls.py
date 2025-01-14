from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


# All the routing system of the website
urlpatterns = [

    # Url for users to loging int
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    
    # Default homepage view of the web app
    path("", views.index, name="index"),

    # When users want to signup for newsletters
    path("newsletter/", views.newsletter, name="newsletter_signup"),

    # When user wants to know about ongoing events
    path("events/", views.events, name="events"),

    # Path for fetching calender data
    path("events/feeds/", views.events_feed, name="events_feed"),

    # Path for when user click on a specific event
    path("events/<int:event_id>/details", views.event_details, name="event_details"),

    # Path for when user want to register for an event
    path("events/registration", views.register_for_event, name="register_for_event"),

    # Path for the gallery template
    path("gallery/", views.gallery, name="gallery"),

    # Path for the blogs
    path("blog/", views.blog, name="blog"),

    # View for each individual blog
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),

    # URL for contacting
    path('contact/', views.contact_page, name='contact_page')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)