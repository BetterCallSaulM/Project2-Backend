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

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
