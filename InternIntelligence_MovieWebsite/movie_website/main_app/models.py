from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.



# Model for movie genres
class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    


# Model for movie directors
class Person(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


# Making a model for Movies
class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField()
    poster_url = models.URLField()
    release_date = models.DateField()
    rating = models.FloatField(validators=[
        MinValueValidator(0), MaxValueValidator(10)
    ])
    genre = models.ManyToManyField(Genre, related_name="genre")
    director = models.ManyToManyField(Person, related_name="movies")

    def __str__(self):
        return self.title