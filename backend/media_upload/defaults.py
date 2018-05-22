import os


BASE_DIR = os.path.dirname(
  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

DEFAULT_MEDIA_DIR = os.path.join(MEDIA_DIR, 'default')

DEFAULT_THEATER_IMAGE = os.path.join('default', 'theater.jpg')
DEFAULT_PROP_IMAGE = os.path.join('default', 'prop.png')
DEFAULT_MOVIE_IMAGE = os.path.join('default', 'theater.jpg')
DEFAULT_USER_IMAGE = os.path.join('default', 'theater.jpg')
