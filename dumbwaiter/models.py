from django.db import models
from dumbwaiter import app_settings

class DumbwaiterRecordManager(models.Manager):
    def limit_to(self, name, number):
        try:
            first_out_of_bounds = self.filter(name=name).order_by('-id')[number]
            self.filter(name=name, id__lte=first_out_of_bounds.id).delete()
        except IndexError:
            pass

class DumbwaiterRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)

    objects = DumbwaiterRecordManager()

    class Meta:
            abstract = True

class CachedResult(DumbwaiterRecord):
    data = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super(CachedResult, self).__init__(*args, **kwargs)
        if isinstance(self.data, basestring):
            try:
                self.data = app_settings.SERIALIZER.deserialize(self.data)
            except:
                pass

    def save(self, *args, **kwargs):
        pre_serialized = self.data
        try:
            self.data = app_settings.SERIALIZER.serialize(self.data)
            super(CachedResult, self).save(*args, **kwargs)
        finally:
            self.data = pre_serialized

class ErrorReport(DumbwaiterRecord):
    log = models.TextField(blank=True)
