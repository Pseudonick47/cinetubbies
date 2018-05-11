"""Usefull utility functions."""

import _pickle


def update(obj: object, **kwargs) -> object:
  """Returns obj with updated attributes.

  Args:
    obj: Object to be updated.
    **kwargs: (key, value) pairs where key represents objects attribute to be
      updated and value is the new value to be set.
  Returns:
    Object with updated attributes.
  Raises:
    UserWarning: A warning when attempting to update an attribut that doesn't
      exist.
  """
  for k, v in kwargs.items():
    if not hasattr(obj, k):
      raise UserWarning(
        'Instance of {0} has no attribute {1}. New one will be created with \
        the value of {2}'.format(type(obj), k, v)
      )
    setattr(obj, k, v)
  return obj


def deepcopy(obj):
  """Faster deepcopy.

  Based on c implementation of pickle.

  Args:
    obj: Object to be copied.
  Returns:
    Copied object.
  """
  return _pickle.loads(_pickle.dumps(obj))


def print_urls(urllist, depth=0):
  """Prints all application URLs.

  Recursively walks through URL paths and prints them in terminal.

  Args:
    urllist: Root URLs.
    depth: Current URL depth.
  """

  for entry in urllist:
    print("  " * depth, entry.pattern)
    if hasattr(entry, 'url_patterns'):
      print_urls(entry.url_patterns, depth + 1)
