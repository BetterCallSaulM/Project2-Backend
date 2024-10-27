from rest_framework import serializers
from .models import User, Movie, Watchlist, WatchlistMovie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'is_admin']  

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'year', 'director', 'genre', 'description', 'poster']

class WatchlistSerializer(serializers.ModelSerializer):
    # username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) # StringRelatedField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Watchlist
        fields = ['watchlist_id', 'watchlist_name', 'user_id']

class WatchlistMovieSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    watchlist = serializers.PrimaryKeyRelatedField(queryset=Watchlist.objects.all())

    class Meta:
        model = WatchlistMovie
        fields = ['id', 'movie', 'watchlist', 'status']