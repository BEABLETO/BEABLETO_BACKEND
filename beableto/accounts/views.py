from rest_framework import generics
from .serializers import SignUpSerializer, AuthTokenSerializer
from .models import User
from rest_auth.views import LoginView


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return SignUpSerializer


class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer

