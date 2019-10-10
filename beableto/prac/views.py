from django.http import HttpResponse
from rest_framework import viewsets
from prac.serializers import UserSerializer
from prac.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def index(request):
    return HttpResponse("Hello World")


def test(request):
    return HttpResponse("asdf")