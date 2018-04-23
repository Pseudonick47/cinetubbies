from django.shortcuts import render
from movies.serializers import MovieSerializer
from movies.models import Movie
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .permissions import IsSelfOrReadOnly

class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSelfOrReadOnly]

    # create new movie
    def create(self, request):
        serializer = MovieSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.validated_data['admin_id'] = request.user
        serializer.save()
        return Response(serializer.data)

    @action(detail=False)
    def getMovies(self, request):
        movies = Movie.objects.get()
        return Response(MovieSerializer(movies).data)

    # delete movie
    def destroy(self, request, pk=None):
        movie = Movie.objects.get(id=pk)
        self.check_object_permissions(request, movie)
        movie.delete()
        return Response({'message': 'Movie successfully deleted'})