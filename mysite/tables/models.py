from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    director = models.CharField(max_length=50, default='', blank=True)
    genre = models.CharField(max_length=50, default='', blank=True)
    poster = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    watchlist_name = models.CharField(max_length=50, default='', blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Not Watched')

    def __str__(self):
        return f'{self.watchlist_name} ({self.username})'