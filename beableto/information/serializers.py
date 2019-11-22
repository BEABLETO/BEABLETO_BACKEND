from information.models import Location, Bus, Road, Fragment, Record, Elevator
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


class FragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = ('start_x', 'start_y', 'end_x', 'end_y', 'middle_x', 'middle_y', 'slope')


class CurPoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('user', 'x', 'y', 'time')


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ('line', 'station', 'x_axis', 'y_axis', 'description')