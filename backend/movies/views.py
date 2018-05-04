from django.shortcuts import render
from movies.serializers import MovieSerializer
from showtimes.serializers import ShowtimeSerializer
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
    serializer.save()
    return Response(serializer.data)

  def list(self, request):
    movies = Movie.objects.all()
    return Response(MovieSerializer(movies, many=True).data)

  # delete movie
  def destroy(self, request, pk=None):
    movie = get_object_or_404(Movie, pk=pk)
    self.check_object_permissions(request, movie)
    movie.delete()
    return Response({'message': 'Movie successfully deleted'})

  def retrieve(self, request, pk=None):
    movie = get_object_or_404(Movie, pk=pk)
    return Response(data=MovieSerializer(movie).data)

  def update(self, request, pk=None):
    movie = get_object_or_404(Movie, id=pk)
    self.check_object_permissions(request, movie)
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  @action(detail=True)
  def get_showtimes(self, request, pk=None):
    movie = get_object_or_404(Movie, id=pk)
    showtimes = movie.showtimes.all()
    return Response(ShowtimeSerializer(showtimes, many=True).data)

  @action(detail=True)
  def update_rating(self, request, pk=None):
    vote, _ = Voting.objects.get_or_create(
      user_id=request.user.id,
      movie_id=pk
    )
    vote.rating = request.data['rating']
    vote.save()
    rating = Voting.objects.filter(
      movie_id=pk).aggregate(rating=Avg('rating')
    )
    voters = len(Voting.objects.filter(movie_id=pk).all())
    data = {'rating':rating,'voters':voters}
    return Response(data)
