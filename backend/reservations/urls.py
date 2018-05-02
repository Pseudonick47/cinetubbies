from django.urls import path

from .views import RewardScaleAPI

reward_scales = RewardScaleAPI.as_view({
  'get': 'list',
  'put': 'update_all'
})

reward_scale = RewardScaleAPI.as_view({
  'get': 'retrieve',
  'put': 'update'
})

urlpatterns = [
  path(
    route='rewards/',
    view=reward_scales,
    name='reward-scales'
  ),
  path(
    route='rewards/<slug:pk>',
    view=reward_scale,
    name='reward-scale'
  )
]
