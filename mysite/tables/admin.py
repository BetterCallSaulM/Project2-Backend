from django.contrib import admin

from .models import User, Movie, Watchlist

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Watchlist)
