from information.models import Location, Bus, Road
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('user', 'location_name', 'location_address', 'x_axis', 'y_axis', 'slope', 'auto_door', 'elevator', 'toilet', 'comment', 'image')


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('user', 'area', 'line', 'height')


class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = ('user', 'road', 'slope')