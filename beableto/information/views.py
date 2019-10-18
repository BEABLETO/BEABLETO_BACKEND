from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from information.serializers import LocationSerializer
from information.models import Location
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
from django.http import QueryDict
from accounts.models import User
import json


class LocationSaveView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # query_dict = QueryDict('', mutable=True)
        # query_dict.update(request.data)
        # query_dict.appendlist('user', request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class LocationGetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):  # Image, Comment 빼고는 묶는 작업 필요.
        rq_data = dict(request.data)
        print(rq_data)
        infos = Location.objects.filter(x_axis=rq_data['x_axis'][0], y_axis=rq_data['y_axis'][0])
        info_list = serializers.serialize('json', infos)
        return HttpResponse(info_list)



# class NearLocationView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):