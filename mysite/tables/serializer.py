from rest_framework import serializers
from .models import User, Movie, Watchlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'is_admin']  

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'year', 'director', 'genre', 'poster']

class WatchlistSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()

    class Meta:
        model = Watchlist
        fields = ['watchlist_id', 'watchlist_name', 'username', 'movie', 'status']
