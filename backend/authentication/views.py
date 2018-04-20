from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.response import Response
from.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from .middlewares.arst import SimpleMiddleware
from django.utils.decorators import decorator_from_middleware
from rest_framework_jwt.settings import api_settings
from .utils import auth

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (IsOwnerOrReadOnly,)

  @action(detail=False)
  def current_user(self, request, *args, **kwargs):
    user = request.user
    return Response(UserSerializer(user).data)

  @action(detail=False)
  def register(self, request, * args, ** kwargs):
    user = User(**request.data)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return Response(auth.jwt_response_payload_handler(token, user))

  def perform_create(self, serializer):
    serializer.save()
