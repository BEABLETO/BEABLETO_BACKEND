from information.models import Location
from rest_framework import serializers


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('user', 'location_name', 'location_address', 'x_axis', 'y_axis', 'slope', 'auto_door', 'elevator', 'toilet', 'comment', 'image')