from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from information.serializers import LocationSerializer
from information.models import Location
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
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

    def post(self, request):  # Image, Comment 빼고는 묶는 작업 필요.
        rq_data = dict(request.data)
        info = Location.objects.filter(x_axis=rq_data['x_axis'][0], y_axis=rq_data['y_axis'][0])

        isFirst = True
        isImage = True
        slope_mean = 0.0
        data_size = 0
        auto_door = 0
        elevator = 0
        toilet = 0
        comment = []
        location_name = ""
        location_address = ""
        image_field = ""

        for obj in info:
            obj_dict = obj.as_dict()
            data_size += 1
            if isFirst:
                isFirst = False
                location_name = obj_dict['location_name']
                location_address = obj_dict['location_address']
            if isImage:
                if obj_dict['image'] is not "":
                    image_field = obj_dict['image']
                    isImage = False

            slope_mean += obj_dict['slope']
            if obj_dict['auto_door']:
                auto_door += 1
            if obj_dict['elevator']:
                elevator += 1
            if obj_dict['toilet']:
                toilet += 1
            comment.append(obj_dict['comment'])

        slope_mean /= data_size  # mean 계산
        if auto_door >= int(data_size) / 2:
            auto_door_return = True
        else:
            auto_door_return = False

        if elevator >= int(data_size) / 2:
            elevator_return = True
        else:
            elevator_return = False

        if toilet >= int(data_size) / 2:
            toilet_return = True
        else:
            toilet_return = False

        res_dict = {
            'image': str(image_field),
            'location_name': location_name,
            'location_address ': location_address,
            'x_axis': float(rq_data['x_axis'][0]),
            'y_axis': float(rq_data['y_axis'][0]),
            'slope': slope_mean,
            'auto_door': auto_door_return,
            'elevator': elevator_return,
            'toilet': toilet_return,
            'comment': comment,
             }

        return JsonResponse(res_dict)


class LocationGetMarkers(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        # info = Location.objects.filter(x_axis=rq_data['x_axis'][0], y_axis=rq_data['y_axis'][0])
        info = Location.objects.filter(x_axis__range=(float(rq_data['lsx'][0]), float(rq_data['rnx'][0])), y_axis__range=(float(rq_data['lsy'][0]), float(rq_data['rny'][0]))).values('location_name', 'x_axis', 'y_axis')
        # info_list = serializers.serialize('json', info)
        ret_list = []
        for d in info:
            # j = json.dumps(d)
            # j = j[1:-1]
            ret_list.append(d)
        markers = dict()
        markers['markers'] = ret_list
        return JsonResponse(markers)


# class NearLocationView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):