from django.shortcuts import render
from movies.serializers import MovieSerializer
from movies.models import Movie
from rest_framework import viewsets
from rest_framework.decorators import action

class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # creating new movie
    @action(detail=False)
    def create(self, request, * args, ** kwargs):
        movie = Movie.create_movie(request.data)
        return Response(MovieSerializer(movie).data)