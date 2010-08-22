def get_value(name):
    from dumbwaiter.models import CachedResult
    try:
        return CachedResult.objects.filter(name=name).order_by('-pk')[0].data
    except CachedResult.DoesNotExist:
        return Nonw
