from rest_framework import serializers
from .models import User, Movie, Watchlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'releaseDate', 'year', 'director', 'genre']

class WatchlistSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()  # This can be changed to UserSerializer if you want detailed user data
    movie_id = MovieSerializer()

    class Meta:
        model = Watchlist
        fields = ['watchlist_id', 'username', 'movie_id', 'status']
