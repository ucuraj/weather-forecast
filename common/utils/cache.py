from django.conf import settings
from django.core.cache import cache
from django.core.serializers import serialize, deserialize


def get_object_by_key(key, desearialize_obj=True):
    cache_obj = cache.get(key)
    if desearialize_obj:
        cache_obj = list(deserialize('json', cache_obj))
        if cache_obj:
            return cache_obj[0].object
    return cache_obj


def set_object_by_key(key, obj, serialize_obj=True):
    if serialize_obj:
        obj = serialize('json', [obj])
    return cache.set(key, obj, timeout=settings.DEFAULT_CACHING_TIME)


def is_cached(key):
    return True if cache.get(key) else False


def remaing_ttl(key):
    return cache.pttl(key)
