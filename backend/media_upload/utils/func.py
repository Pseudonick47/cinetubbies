import os
import uuid


def unique_name(filename):
  _, ext = os.path.splitext(filename)
  return "{0}{1}".format(uuid.uuid4(), ext)
