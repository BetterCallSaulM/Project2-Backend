from rest_framework import serializers
from .models import User, Movie, Watchlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'year', 'director', 'genre', 'poster']

class WatchlistSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # ForeignKey to User
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())  # ForeignKey to User

    class Meta:
        model = Watchlist
        fields = ['watchlist_id', 'watchlist_name', 'username', 'movie', 'status']
