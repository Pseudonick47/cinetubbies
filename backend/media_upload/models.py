import os
import datetime

from django.db import models

from .utils.func import unique_name


OFFICIAL_PROP_IMAGE = ('o', 'Official Prop Image')

IMAGE_KIND = (
  OFFICIAL_PROP_IMAGE,
)


def official_props_dir():
  now = datetime.datetime.now()
  return os.path.join(
    'props', 'official', str(now.year), str(now.month), str(now.day)
  )

def generate_image_path(instance, filename):
  dir = ''
  if instance.kind == OFFICIAL_PROP_IMAGE[0]:
    dir = official_props_dir()

  return os.path.join('images', dir, unique_name(filename))


class Image(models.Model):
  id = models.AutoField(primary_key=True)
  kind = models.CharField(max_length=1, choices=IMAGE_KIND)
  data = models.ImageField(upload_to=generate_image_path)
