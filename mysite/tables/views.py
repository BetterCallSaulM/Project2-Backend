from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Movie, Watchlist
from .serializer import UserSerializer, MovieSerializer, WatchlistSerializer

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

        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_data = User.objects.get(username=username)
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

        poster = request.query_params.get('poster')
        if poster is not None:
            movie.poster = poster

        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    @action(detail=False, methods=['GET'], url_path='list')
    def get_list(self, request):
        list_name = request.query_params.get('list_name')
        username = request.query_params.get('user')

        if not list_name or not username:
            return Response({'error' : 'List name and username required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            list_data = Watchlist.objects.filter(watchlist_name=list_name, username=username).values()
            return Response({'message' : 'List retrieved successfully', 'watchlist' : list_data}, status=status.HTTP_202_ACCEPTED)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
