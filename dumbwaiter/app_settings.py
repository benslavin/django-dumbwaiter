import pickle
from django.conf import settings
from django.utils import importlib

__all__ = ['SERIALIZER', 'THREADED', 'FUNCTION_LIST', 'MAX_SAVED', 'DEFAULT_FREQUENCY', 'PICKLE_PROTOCOL']

SERIALIZER_NAME = getattr(settings, 'DUMBWAITER_SERIALIZER', 'dumbwaiter.serializers.pickler')
THREADED = getattr(settings, 'DUMBWAITER_THREADED', True)
FUNCTION_LIST = getattr(settings, 'DUMBWAITER_FUNCTION_LIST', [])
MAX_SAVED = getattr(settings, 'DUMBWAITER_DEFAULT_SAVED', 10)
DEFAULT_FREQUENCY = getattr(settings, 'DUMBWAITER_DEFAULT_FREQUENCY', 5*60)
PICKLE_PROTOCOL = getattr(settings, 'DUMBWAITER_PICKLE_PROTOCOL', pickle.HIGHEST_PROTOCOL)

SERIALIZER = getattr(importlib.import_module(SERIALIZER_NAME), 'serializer')
