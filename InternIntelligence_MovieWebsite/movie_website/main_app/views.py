from django.shortcuts import render
from django.http import HttpResponse
from api.tmdb_api import (
    get_popular_movies,
    get_top_rated_movies,
    get_now_playing_movies,
    get_trending_movies,
    search_movies,
    get_movie_details,
    get_movie_credits,
    get_similar_movies
)

# Home Page (Displays Popular, Top-Rated, Now-Playing, Trending Movies)
def index(request):
    movie_categories = {
        "Popular Movies": get_popular_movies(),
        "Top Rated Movies": get_top_rated_movies(),
        "Now Playing Movies": get_now_playing_movies(),
        "Trending Movies": get_trending_movies(),
    }

    context = {"movie_categories": movie_categories}
    return render(request, "main_app/index.html", context)

# Movie Details Page
def movie_details(request, movie_id):
    movie = get_movie_details(movie_id)
    credits = get_movie_credits(movie_id)
    similar_movies = get_similar_movies(movie_id)

    if not movie:
        return HttpResponse("Movie not found", status=404)

    context = {
        "movie": movie,
        "credits": credits,
        "similar_movies": similar_movies,
    }
    return render(request, "main_app/movie_details.html", context)

# Search Movies
def search_results(request):
    query = request.GET.get("query", "")
    sort_by = request.GET.get("sort_by", "popularity.desc")
    genre_id = request.GET.get("genre_id")

    movies = search_movies(query, sort_by, genre_id) if query else []
    
    context = {
        "query": query,
        "movies": movies,
    }
    return render(request, "main_app/search_results.html", context)