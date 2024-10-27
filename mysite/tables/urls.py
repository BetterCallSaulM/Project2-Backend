from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'Users', UserViewSet)
router.register(r'Movies', MovieViewSet)
router.register(r'Watchlists', WatchlistViewSet)
router.register(r'WatchlistMovies', WatchlistMovieViewSet, basename='watchlistmovies')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]