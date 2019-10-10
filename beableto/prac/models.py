from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable
from django import forms


class User(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=30)
    guardian_phone = models.CharField(max_length=30)
    aids = models.CharField(max_length=30)
    push_agree = models.BooleanField()


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    instance.password = make_password(instance.password)

