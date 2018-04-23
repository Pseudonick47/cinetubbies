from django.shortcuts import render
from movies.serializers import MovieSerializer
from movies.models import Movie
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # create new movie
    def create(self, request):
        serializer = MovieSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

    # delete movie
    def destroy(self, request, pk=None):
        movie = Movie.objects.get(id=pk)
        movie.delete()
        return Response({'message': 'Movie successfully deleted'})