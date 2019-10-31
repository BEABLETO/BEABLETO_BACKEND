from rest_framework import generics
from .serializers import SignUpSerializer, AuthTokenSerializer
from .models import User
from rest_auth.views import LoginView
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
import json
from django.forms.models import model_to_dict


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return SignUpSerializer


class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer


class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        info = {'email': request.user.email,
                'username': request.user.username,
                }
        print(info)
        return JsonResponse(info)


