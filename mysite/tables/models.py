from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    director = models.CharField(max_length=50, default='', blank=True)
    genre = models.CharField(max_length=50, default='', blank=True)
    description = models.CharField(max_length=1000, default='', blank=True)
    poster = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    watchlist_name = models.CharField(max_length=50, default='', blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.watchlist_name} ({self.user_id})'
    
class WatchlistMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Not Watched')

    def __str__(self):
        return f'{self.movie} ({self.watchlist})'