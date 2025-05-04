import requests
from django.conf import settings

# Importing the api key and url
TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# Function to get the popular movies
def get_popular_movies():
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])

    # Print debug info if request fails
    print(f"Error: {response.status_code}, Response: {response.text}")
    return None


# Function to get the top rated movies
def get_top_rated_movies():

    # Making the url request
    url = f"{TMDB_BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US&page=1"

    # Siphoning the URL request
    response = requests.get(url)

    # Checking if request was made correctly
    if response.status_code == 200:
        
        # Return the data in json format and convert it into a list
        return response.json().get("results", [])
    
    # If Errors Occur
    print(f"Error: {response.status_code}, Response: {response.text}")
    return None


# Function to get the now playing movies
def get_now_playing_movies():
    url = f"{TMDB_BASE_URL}/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])
    
    print(f"Error: {response.status_code}, Response: {response.text}" )
    return None


# Function to search for movies
def search_movies(query, sort_by="popularity.desc", genre_id=None):
    url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&language=en-US&query={query}&page=1&sort_by={sort_by}"
    
    # Apply genre filter correctly before the request
    if genre_id:
        url += f"&with_genres={genre_id}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])
    
    print(f"Error: {response.status_code}, Response: {response.text}")
    return None



# Function to get a movie by ID
def get_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    
    print(f"Error: {response.status_code}, Response: {response.text}")
    return None


# Function to get the credits for a movie
def get_movie_credits(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    
    print(f"Error: {response.status_code}, Response: {response.text}")
    return None
    

# Function to get similar movies
def get_similar_movies(movie_id, page=1):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/similar?api_key={TMDB_API_KEY}&language=en-US&page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])

    print(f"Error: {response.status_code}, Response: {response.text}")
    return None


# Function to get the trending movies
def get_trending_movies(time_window="week"):
    url = f"{TMDB_BASE_URL}/trending/movie/{time_window}?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])
    return None
