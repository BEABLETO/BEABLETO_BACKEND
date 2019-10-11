from django.http import HttpResponse, JsonResponse
from accounts.models import User
from django.shortcuts import render
from django.core import serializers


def ret_phone(request):
    print(request.auth)
    data = User.objects.get(email=request.user.email)
    # data_list = serializers.serialize('json', data)
    return HttpResponse(data, content_type="text/json-comment-filtered")