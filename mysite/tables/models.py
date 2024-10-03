from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=50)
    
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    releaseDate = models.DateField()
    year = models.IntegerField()
    director = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)

class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.TextField()