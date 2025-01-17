from django.urls import path

from . import views

urlpatterns = [
    # This route is my website default index page mainly the encyclopedia page
    path("", views.index, name="index"),

    # This will be my default wiki search site
    path("wiki/", views.wiki, name="wiki"),

    # This when user searches a specific article in http
    path("wiki/<str:title>", views.title, name="title"),

    # This when the user searches for article in search bar
    path("wiki/search/", views.search, name="search"),

    # If user wanna create a new page
    path("wiki/newpage/", views.newpage, name="newpage"),

    # If user clicks the random button
    path("wiki/random/", views.random_page, name="random_page"),

    # If user wants to edit a wiki page
    path('wiki/edit/<str:title>', views.edit, name="edit")
]
