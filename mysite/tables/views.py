from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import User, Movie, Watchlist
from .serializer import UserSerializer, MovieSerializer, WatchlistSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
# Create you views here

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index. Bruh lmaooooo")
    return HttpResponse('Appssdfd.sdfsjs')