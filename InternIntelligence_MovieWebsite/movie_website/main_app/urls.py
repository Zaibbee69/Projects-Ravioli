from django.urls import path
from .views import index, movie_details, search_results

urlpatterns = [
    path("", index, name="index"),
    path("movie/<int:movie_id>/", movie_details, name="movie_details"),
    path("search/", search_results, name="search_results"),
]
