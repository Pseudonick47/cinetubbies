from django.core.paginator import Paginator
from django.utils.decorators import decorator_from_middleware
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, THEATER_ADMIN, FAN_ZONE_ADMIN, Friendship
from .permissions import IsSelfOrReadOnly, IsSystemAdmin
from .serializers import TheaterAdminSerializer, AdminSerializer, UserSerializer, FriendSerializer
from .utils import auth

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

  @action(detail=False)
  def active_user(self, request, *args, **kwargs):
    user = request.user
    user = User.objects.get(id=user.id)
    return Response(UserSerializer(user).data)

  def create(self, request):
    serializer = UserSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    user = serializer.save()

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    auth.send_verification_mail(user, 'token')
    return Response(auth.jwt_response_payload_handler(token, user))

  def partial_update(self, request, pk=None):
    user = User.objects.get(id=pk)
    self.check_object_permissions(request, user)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)

    serializer.save()
    return Response(serializer.data)

  def destroy(self, request, pk=None):
    user = User.objects.get(id=pk)
    self.check_object_permissions(request, user)
    user.delete()
    return Response({'message': 'User successfully deleted'})

class FriendViewSet(viewsets.ViewSet):
  def create(self, request, pk=None):
    user = request.user
    queryset = User.objects.all()
    friend = get_object_or_404(queryset, id=pk)

    a = Friendship.objects.filter(me_id=friend.id, friend_id=user.id).count()
    b = Friendship.objects.filter(me_id=user.id, friend_id=friend.id).count()
    if a == 0 and b == 0:
      friend_requests = Friendship.objects.create(me_id=user.id, friend_id=friend.id)
    elif a > 0:
      friend_requests = Friendship.objects.filter(me_id=friend.id, friend_id=user.id).get()
      friend_requests.accepted = True
      friend_requests.save()
    return Response({ 'friend': friend.id })

  def retrieve(self, request, pk=None):
    queryset = User.objects.all()
    user = get_object_or_404(queryset, id=pk)
    data = {
      'friends': FriendSerializer(user.friends(), many=True).data,
      'friend_requests': FriendSerializer(user.friend_requests(), many=True).data
    }
    return Response(data)

  def search_for_friends(self, request, query):
    user = request.user
    queryset = User.objects.all()
    search_results = queryset.exclude(id=user.id).exclude(id__in=user.friendships.only('id')).filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    data = {
      'results': FriendSerializer(search_results, many=True).data
    }
    return Response(data)

  def delete(self, request, pk=None):
    user = request.user
    Friendship.objects.filter(Q(me_id=pk, friend_id=user.id) | Q(me_id=user.id, friend_id=pk)).delete()

    return Response({'message': 'Friend successfully deleted'})


class AdminViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = AdminSerializer
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def list(self, request):
    role = request.GET.get('role')
    if role:
      admins = User.objects.filter(role=role)
    else:
      admins = User.objects.all().exclude(role='user')

    all_admins = request.GET.get('all')

    if all_admins:
      # user requested all admins of the same role
      admins = User.objects.filter(role=role)
      return Response(data=AdminSerializer(admins, many=True).data)

    # return paginated results
    num = request.GET.get('num')
    paginator = Paginator(admins, num if num else 10)
    page = request.GET.get('page')
    admins = paginator.get_page(page if page else 1)

    return Response(data=AdminSerializer(admins, many=True).data)

  def create(self, request):
    pwd = auth.generate_password()
    request.data['password'] = pwd

    if (request.data['role'] == THEATER_ADMIN[0]):
      serializer = TheaterAdminSerializer(data=request.data, partial=True)
    else:
      serializer = AdminSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    admin = serializer.save()

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(admin)
    token = jwt_encode_handler(payload)
    auth.send_mail_to_admin(admin, pwd, token)

    return Response(data=serializer.data)

  @action(detail=False)
  def count(self, request):
      role = request.GET.get('role')
      admins = User.objects.all().exclude(role='user')
      if role:
        return Response(data=admins.filter(role=role).count())
      else:
        return Response(data=admins.count())
