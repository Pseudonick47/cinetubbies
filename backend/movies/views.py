from django.shortcuts import render
from movies.serializers import MovieSerializer
from movies.models import Movie
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .permissions import IsCreatorOrReadOnly
from authentication.models import TheaterAdmin
from django.shortcuts import get_object_or_404

class MovieViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows movies to be viewed or edited.
  """
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  permission_classes = [IsCreatorOrReadOnly]

  # create new movie
  def create(self, request):
    serializer = MovieSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    serializer.validated_data['admin'] = request.user
    admin = TheaterAdmin.objects.get(user_ptr_id=request.user.id)
    serializer.validated_data['theater'] = admin.theater
    serializer.save()
    return Response(serializer.data)

  def list(self, request):
    admin = TheaterAdmin.objects.get(user_ptr_id=request.user.id)
    movies = Movie.objects.filter(theater_id=admin.theater).all()
    return Response(MovieSerializer(movies, many=True).data)

  # delete movie
  def destroy(self, request, pk=None):
    movie = Movie.objects.get(id=pk)
    self.check_object_permissions(request, movie)
    movie.delete()
    return Response({'message': 'Movie successfully deleted'})

  @action(detail=False)
  def update_info(self, request):
    movie = Movie.objects.get(id=request.data['movie_id'], admin_id=request.data['admin_id'])
    movie.title = request.data['title']
    movie.genre = request.data['genre']
    movie.director = request.data['director']
    movie.actors = request.data['actors']
    movie.description = request.data['description']
    movie.duration = request.data['duration']
    movie.save()
    return Response(MovieSerializer(movie).data)

  def retrieve(self, request, pk=None):
    movie = Movie.objects.get(id=pk)
    return Response(data=MovieSerializer(movie).data)

  def update(self, request, pk=None):
    movie = get_object_or_404(Movie, id=pk)
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
