from .models import Movie
from django.contrib import admin
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import MovieSerializer
from rest_framework import status

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_added')  # Fields to display in the list view
    search_fields = ('title', 'description') 
from rest_framework import permissions, viewsets


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def movie_list(request):
    if request.method == 'GET':
        # Retrieve all movies
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new movie
        serializer = MovieSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def movie_detail(request, pk):
    try:
        # Retrieve the movie by primary key
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve details of a specific movie
        serializer = MovieSerializer(movie, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update an existing movie
        serializer = MovieSerializer(movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a movie
        movie.delete()
        return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)