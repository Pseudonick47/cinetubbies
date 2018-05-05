import copy

from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer

from cinetubbies.utils.func import update

from fan_zone.props.serializers import PropSerializer

from .models import UsedProp


class PublicSerializer(PropSerializer):
  owner = UserSerializer(
    read_only=True,
  )
  post_date = serializers.DateTimeField(
    read_only=True,
  )
  expiration_date = serializers.DateTimeField(
    read_only=True,
  )

  def to_representation(self, obj):
    ret = super().to_representation(obj)
    ret['postDate'] = ret.pop('post_date')
    ret['expirationDate'] = ret.pop('expiration_date')
    return ret


class MemberSerializer(PublicSerializer):
  owner_id = serializers.PrimaryKeyRelatedField(
    queryset=User,
    write_only=True,
    required=True,
    allow_null=False,
  )

  def to_internal_value(self, data):
    d = copy.deepcopy(data)
    d['owner_id'] = d.pop('ownerId')
    return super().to_internal_value(d)

  def create(self, validated_data):
    return UsedProp.objects.create(**validated_data)

  def update(self, prop, validated_data):
    prop = update(prop, **validated_data)
    prop.save()
    return prop


class RestrictedSerializer(PublicSerializer):
  approved = serializers.BooleanField(
    read_only=True,
  )
  pending_approval = serializers.BooleanField(
    read_only=True,
  )

  def to_representation(self, obj):
    ret = super().to_representation(obj)
    ret['pendingApproval'] = ret.pop('pending_approval')
    return ret
