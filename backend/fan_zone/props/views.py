# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.paginator import Paginator

# from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet

# from authentication.models import User
# from authentication.permissions import IsFanZoneOrSystemAdmin

# from fan_zone.categories.models import Category

# from .models import UsedProp
# from .permissions import IsOwner
# from .serializers import MemberSerializer
# from .serializers import PublicSerializer
# from .serializers import RestrictedSerializer


# class PublicAPI(ViewSet):

#   @action(detail=False)
#   def count(self, request, *args, **kwargs):
#     queryset = UsedProp.objects.all()

#     category_id = request.GET.get('category')
#     if category_id:
#       get_object_or_404(Category, pk=category_id)
#       queryset = queryset.filter(category_id=category_id)

#     all = request.GET.get('all')
#     if not all:
#       approved = request.GET.get('approved')
#       if approved is not None:
#         queryset = queryset.filter(approved=approved=='true')
#       else:
#         queryset = queryset.filter(approved=True)

#     return Response(data=queryset.count())

#   def list(self, request, *args, **kwargs):
#     queryset = UsedProp.objects.all()

#     user_id = kwargs.pop('user_id', None)
#     if user_id:
#       get_object_or_404(User, pk=user_id)
#       queryset = queryset.filter(owner_id=user_id)

#     category_id = request.GET.get('category')
#     if category_id:
#       get_object_or_404(Category, pk=category_id)
#       queryset = queryset.filter(category_id=category_id)

#     all = request.GET.get('all')
#     if not all:
#       approved = request.GET.get('approved')
#       if approved is not None:
#         queryset = queryset.filter(approved=approved=='true')
#       else:
#         queryset = queryset.filter(approved=True)

#     num = request.GET.get('num') or 10
#     paginator = Paginator(queryset.order_by('title'), num)
#     page = request.GET.get('num') or 1

#     props = paginator.get_page(page)
#     return Response(data=PublicSerializer(props, many=True).data)

#   def retrieve(self, request, *args, **kwargs):
#     prop_id = kwargs.pop('pk')

#     user_id = kwargs.pop('user_id', None)
#     if user_id:
#       user = get_object_or_404(User, user_id)

#       try:
#         prop = user.usedprops.get(pk=prop_id)
#         return Response(data=PublicSerializer(prop).data)

#       except ObjectDoesNotExist:
#         return Response(
#           data={
#             'message': 'User {0} is not the owner of used prop {1}'
#               .format(user_id, prop_id)
#           }
#         )

#     else:
#       prop = get_object_or_404(UsedProp, pk=prop_id)
#       return Response(data=PublicSerializer(prop).data)


# class MemberAPI(ViewSet):
#   permission_classes = [IsAuthenticated, IsOwner]

#   def create(self, request, *args, **kwargs):
#     serializer = MemberSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     print(serializer.data)
#     return Response(data=serializer.data)

#   def destroy(self, request, *args, **kwargs):
#     prop_id = kwargs.pop('pk')
#     prop = get_object_or_404(UsedProp, pk=prop_id)
#     self.check_object_permissions(request, prop)
#     prop.delete()
#     return Response(
#       data={'message': 'Used prop {0} successfully deleted.'.format(prop_id)}
#     )

#   def update(self, request, *args, **kwargs):
#     prop_id = kwargs.pop('pk')
#     prop = get_object_or_404(UsedProp, pk=prop_id)
#     self.check_object_permissions(request, prop)

#     serializer = MemberSerializer(prop, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()

#     return Response(data=serializer.data)


# class RestrictedAPI(ViewSet):
#   permission_classes = [IsAuthenticated, IsFanZoneOrSystemAdmin]

#   def update(self, request, *args, **kwargs):
#     prop_id = kwargs.pop('pk')

#     prop = get_object_or_404(UsedProp, pk=prop_id)
#     prop.approved = True
#     prop.pending_approval = False
#     prop.save()

#     return Response(data=RestrictedSerializer(prop).data)
