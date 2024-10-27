from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Movie, Watchlist, WatchlistMovie
from .serializer import UserSerializer, MovieSerializer, WatchlistSerializer, WatchlistMovieSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'], url_path='newuser')
    def create_user(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {'username' : username, 'password' : password}
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'], url_path='login')
    def login(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_data = User.objects.get(username=username, password=password)
            serializer = UserSerializer(user_data)
            return Response({'message' : 'Login successful', 'user' : serializer.data}, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'error': 'Incorrect login credentials'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'], url_path='logout')
    def logout(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_data = User.objects.get(username=username)
            serializer = UserSerializer(user_data)
            return Response({'message' : 'Logout successful', 'user' : serializer.data}, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'error': 'Incorrect user credentials'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_user(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_data = User.objects.get(username=username, password=password)
            user_data.delete()
            return Response({'message' : 'User deleted successfully'}, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['PATCH'], url_path='update')
    def update_user(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        new_username = request.query_params.get('new_username')
        if new_username is not None:
            if User.objects.filter(username=new_username).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            user.username = new_username
        
        password = request.query_params.get('password')
        if password is not None:
            user.password = password
        
        is_admin = request.query_params.get('is_admin')
        if is_admin is not None:
            user.is_admin = is_admin.lower() == 'true'

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['GET'], url_path='movie')
    def get_movie(self, request):
        movie_name = request.query_params.get('name')

        if not movie_name:
            return Response({'error' : 'Movie name required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            movie_data = Movie.objects.get(title=movie_name)
            serializer = MovieSerializer(movie_data)
            return Response({'message' : 'Movie retrieved successfully', 'movie' : serializer.data}, status=status.HTTP_202_ACCEPTED)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'], url_path='movies')
    def get_movies(self, request):
        movie_name = request.query_params.get('name')

        if not movie_name:
            return Response({'error' : 'Movie name required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            movies = Movie.objects.filter(title__icontains=movie_name).values()
            return Response({'message' : 'Movies retrieved successfully', 'movie(s)' : movies}, status=status.HTTP_202_ACCEPTED)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie(s) not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_path='add')
    def add_movie(self, request):
        movie_name = request.query_params.get('name')

        if not movie_name:
            return Response({'error' : 'Movie name required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        year = request.query_params.get('year', Movie._meta.get_field('year').get_default())
        director = request.query_params.get('director', Movie._meta.get_field('director').get_default())
        genre = request.query_params.get('genre', Movie._meta.get_field('genre').get_default())
        description = request.query_params.get('description', Movie._meta.get_field('description').get_default())
        poster = request.query_params.get('poster', Movie._meta.get_field('poster').get_default())

        movie_data = {
            'title' : movie_name,
            'year' : year,
            'director' : director,
            'genre' : genre,
            'description' : description,
            'poster' : poster
        }
        serializer = MovieSerializer(data=movie_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_movie(self, request):
        movie_name = request.query_params.get('name')  

        if not movie_name:
            return Response({'error': 'Movie title is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            movie_data = Movie.objects.get(title=movie_name)
            movie_data.delete()
            return Response({'message' : 'Movie deleted successfully'}, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['PATCH'], url_path='edit')
    def edit_movie(self, request):
        movie_name = request.query_params.get('name')

        if not movie_name:
            return Response({'error': 'Movie name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            movie = Movie.objects.get(title=movie_name)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        title = request.query_params.get('title')
        if title is not None:
            movie.title = title
        
        year = request.query_params.get('year')
        if year is not None:
            movie.year = year
        
        director = request.query_params.get('director')
        if director is not None:
            movie.director = director

        genre = request.query_params.get('genre')
        if genre is not None:
            movie.genre = genre

        description = request.query_params.get('description')
        if description is not None:
            movie.description = description

        poster = request.query_params.get('poster')
        if poster is not None:
            movie.poster = poster

        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    @action(detail=False, methods=['GET'], url_path='lists')
    def get_distinct_watchlist_names(self, request):
        user = request.query_params.get('user')

        if not user:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            watchlists = Watchlist.objects.filter(user_id=user).values()
            return Response({'Watchlists': watchlists}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_path='newlist')
    def create_wishlist(self, request):
        name = request.query_params.get('name')
        user = request.query_params.get('user')

        if not name or not user:
            return Response({'error': 'Name and user_id are required'})
        
        wishlist_data = {'watchlist_name': name, 'user_id' : user}
        serializer = WatchlistSerializer(data=wishlist_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_watchlist(self, request):
        watchlist = request.query_params.get('watchlist')

        if not watchlist:
            return Response({'error': 'Watchlist id is required'})
        
        try:
            watchlist_data = Watchlist.objects.get(watchlist_id=watchlist)
            watchlist_data.delete()
            return Response({'message' : 'Watchlist deleted successfully'}, status=status.HTTP_202_ACCEPTED)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

class WatchlistMovieViewSet(viewsets.ModelViewSet):
    queryset = WatchlistMovie.objects.all()
    serializer_class = WatchlistMovieSerializer

    @action(detail=False, methods=['GET'], url_path='movies')
    def get_movies(self, request):
        watchlist = request.query_params.get('watchlist')

        if not watchlist:
            return Response({'error': 'Watchlist id required'})
        
        try:
            movies = WatchlistMovie.objects.filter(watchlist_id=watchlist).values()
            return Response({'Movies': movies}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_path='add')
    def add_to_list(self, request):
        movie = request.query_params.get('movie')
        watchlist = request.query_params.get('watchlist')
        watch_status = request.query_params.get('status')

        if not movie or not watchlist or not status:
            return Response({'error': 'Movie id, Watchlist id, and status required'})
        
        item_data = {'movie': movie, 'watchlist': watchlist, 'status':watch_status}
        serializer = WatchlistMovieSerializer(data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_from_watchlist(self, request):
        id = request.query_params.get('id')

        if not id:
            return Response({'error': 'ID required'})
        
        try:
            movie_data = WatchlistMovie.objects.get(id=id)
            movie_data.delete()
            return Response({'message' : 'Movie removed from watchlist successfully'}, status=status.HTTP_202_ACCEPTED)
        except WatchlistMovie.DoesNotExist:
            return Response({'error': 'Movie not found in Watchlist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
