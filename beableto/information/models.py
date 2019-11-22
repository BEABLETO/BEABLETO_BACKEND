from django.db import models
from accounts.models import User
from beableto import settings


class Location(models.Model):
    # 외래키
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=100)
    x_axis = models.FloatField()
    y_axis = models.FloatField()
    slope = models.IntegerField()
    auto_door = models.BooleanField()
    elevator = models.BooleanField()
    toilet = models.BooleanField()

    # Optional
    image = models.ImageField(upload_to='locationImage/', blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def as_dict(self):
        return {
            "user": self.user,
            "location_name": self.location_name,
            "location_address": self.location_address,
            "x_axis": self.x_axis,
            "y_axis": self.y_axis,
            "slope": self.slope,
            "auto_door": self.auto_door,
            "elevator": self.elevator,
            "toilet": self.toilet,
            "image": self.image,
            "comment": self.comment,
        }


class Bus(models.Model):
    # 외래키
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    area = models.CharField(max_length=30)
    line = models.CharField(max_length=30)
    height = models.IntegerField()

    def as_dict(self):
        return {
            'user': self.user,
            'area': self.area,
            'line': self.line,
            'height': self.height,
        }


class Road(models.Model):
    # 외래키
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    road = models.CharField(max_length=5000)
    slope = models.IntegerField()


class Fragment(models.Model):
    # 외래키
    road = models.ForeignKey(Road, on_delete=models.CASCADE, null=True)

    start_x = models.FloatField()
    start_y = models.FloatField()
    end_x = models.FloatField()
    end_y = models.FloatField()

    # For easy computation
    middle_x = models.FloatField()
    middle_y = models.FloatField()

    slope = models.IntegerField(default=1)

    def as_dict(self):
        return {
            'start_x': self.start_x,
            'start_y': self.start_y,
            'end_x': self.end_x,
            'end_y': self.end_y,
            'middle_x': self.middle_x,
            'middle_y': self.middle_y,
            'slope': self.slope,
        }


class Record(models.Model):
    # 외래키
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    x = models.FloatField()
    y = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'time': self.time
        }


class Elevator(models.Model):
    line = models.IntegerField()
    station = models.CharField(max_length=100)
    x_axis = models.FloatField()
    y_axis = models.FloatField()
    description = models.CharField(max_length=100)

    def as_dict(self):
        return {
            'x_axis': self.x_axis,
            'y_axis': self.y_axis,
            'station': self.station,
            'line': self.line,
            'description': self.description,
        }