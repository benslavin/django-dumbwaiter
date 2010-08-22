import pickle

class PickleSerializer(object):
    def serialize(self, obj):
        from dumbwaiter import app_settings
        return pickle.dumps(obj, app_settings.PICKLE_PROTOCOL).encode('base64')

    def deserialize(self, obj):
        return pickle.loads(obj.decode('base64'))

serializer = PickleSerializer()
