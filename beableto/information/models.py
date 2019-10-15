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
    comment = models.CharField(max_length=200)