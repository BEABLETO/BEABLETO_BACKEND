from prac.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'user_id', 'password', 'phone', 'guardian_phone', 'aids', 'push_agree')