from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.response import Response
from.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from .middlewares.arst import SimpleMiddleware
from django.utils.decorators import decorator_from_middleware
from .utils import auth

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (IsOwnerOrReadOnly,)

  @action(detail=False)
  def current_user(self, request, *args, **kwargs):
    user = request.user
    return Response(UserSerializer(user).data)

  def perform_create(self, serializer):
    serializer.save()
