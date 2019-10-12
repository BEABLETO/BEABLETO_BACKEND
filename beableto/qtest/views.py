from django.http import HttpResponse, JsonResponse
from accounts.models import User
from django.shortcuts import render
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict


def ret_phone(request):
    print(request.auth)
    data = User.objects.get(email=request.user.email)
    # data_list = serializers.serialize('json', data)
    return HttpResponse(data, content_type="text/json-comment-filtered")


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class GetUserInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        jsonData = model_to_dict(User.objects.get(email=request.user.email))
        wanted_keys = ['phone', 'guardian_phone']
        ret = dict((k, jsonData[k]) for k in wanted_keys if k in jsonData)
        return Response(ret)

