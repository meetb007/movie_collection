from rest_framework import serializers

from collection.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField('get_uuid')

    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']

    def get_uuid(self, obj):
        return obj.id


class CollectionDetailsSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField('get_uuid')

    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']

    def get_uuid(self, obj):
        return obj.id