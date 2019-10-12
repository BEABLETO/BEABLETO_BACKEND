from rest_framework import generics
from .serializers import SignUpSerializer, AuthTokenSerializer
from .models import User
from rest_auth.views import LoginView
from django.forms.models import model_to_dict
from rest_framework.response import Response


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return SignUpSerializer



class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer

