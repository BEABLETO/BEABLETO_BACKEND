from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from information.serializers import LocationSerializer, BusSerializer, RoadSerializer
from information.models import Location, Bus
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import QueryDict
from accounts.models import User
import json
from .utilities import bracket_clear
from .utilities import MarkerClass
import json
import requests


class LocationSaveView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)
        rq_data['user'] = request.user.pk
        serializer = self.get_serializer(data=rq_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class LocationGetView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):  # Image, Comment 빼고는 묶는 작업 필요.
        rq_data = dict(request.data)
        info = Location.objects.filter(x_axis=float(rq_data['x_axis']), y_axis=float(rq_data['y_axis']))

        isFirst = True
        isImage = True
        slope_mean = 0
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
                if str(obj_dict['image']) is not "":
                    image_field = str(obj_dict['image'])
                    isImage = False

            slope_mean += obj_dict['slope']
            if obj_dict['auto_door']:
                auto_door += 1
            if obj_dict['elevator']:
                elevator += 1
            if obj_dict['toilet']:
                toilet += 1
            if str(obj_dict['comment']) is not "":
                comment.append(bracket_clear(str(obj_dict['comment'])))

        slope_mean = round(slope_mean / float(data_size))  # mean 계산
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

        location_name = bracket_clear(location_name)
        location_address = bracket_clear(location_address)

        res_dict = {
            'image': str(image_field),
            'location_name': location_name,
            'location_address ': location_address,
            'x_axis': float(rq_data['x_axis']),
            'y_axis': float(rq_data['y_axis']),
            'slope': slope_mean,
            'auto_door': auto_door_return,
            'elevator': elevator_return,
            'toilet': toilet_return,
            'comment': comment,
             }

        return JsonResponse(res_dict)


class LocationGetMarkersVIew(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        # info = Location.objects.filter(x_axis=rq_data['x_axis'][0], y_axis=rq_data['y_axis'][0])
        print(rq_data['lsx'])
        print(rq_data['rnx'])
        info = Location.objects.filter(x_axis__range=(float(rq_data['lsx']), float(rq_data['rnx'])), y_axis__range=(float(rq_data['lsy']), float(rq_data['rny'])))

        index = 0
        marker_list = []
        cord_dict = {}
        marker_set = set()
        for obj in info:
            obj_dict = obj.as_dict()
            obj_cord = (obj_dict['x_axis'], obj_dict['y_axis'])
            if obj_cord in marker_set:
                key = str(obj_cord[0]) + " " + str(obj_cord[1])
                marker_index = cord_dict[key]
                marker_list[marker_index].updataValue(obj_dict['slope'], obj_dict['auto_door'], obj_dict['elevator'], obj_dict['toilet'])
            else:
                marker_set.add(obj_cord)
                key = str(obj_cord[0]) + " " + str(obj_cord[1])
                cord_dict[key] = index
                index += 1
                newMarker = MarkerClass(obj_cord[0], obj_cord[1], obj_dict['slope'], obj_dict['auto_door'], obj_dict['elevator'], obj_dict['toilet'], obj_dict['location_name'])
                marker_list.append(newMarker)

        ret_list = []
        for m in marker_list:
            # j = json.dumps(d)
            # j = j[1:-1]
            ret_list.append(m.getAsDict())
        markers = dict()
        markers['markers'] = ret_list
        return JsonResponse(markers)


class BusSaveView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)
        rq_data['user'] = request.user.pk
        serializer = self.get_serializer(data=rq_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class GetPathsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)


class RoadSaveView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = RoadSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)
        db_data = {}
        db_data['user'] = request.user.pk
        road_str = ""
        for point in request.data['coordinate']:
            road_str += str(point['x_axis'])
            road_str += " "
            road_str += str(point['y_axis'])
            road_str += " "
        db_data['road'] = road_str
        db_data['slope'] = rq_data['slope']
        serializer = self.get_serializer(data=db_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


# 사용자의 경로 구성을 돕기위한 정보 Return View
class GetBaseWalkView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        with open('tmap.txt') as f:
            api_key = f.readline()
            f.close
        headers = {'Accept': "application/json",
                   # 'Content-Type': "application/json; charset=UTF-8",
                   'appKey': api_key,
                   'Accept-Language': "ko",
                   }
        # 우리 (x, y)와 T-MAP(x, y) 순서 다름
        body = {'startX': str(rq_data['start_y_axis']),
                'startY': str(rq_data['start_x_axis']),
                'endX': str(rq_data['end_y_axis']),
                'endY': str(rq_data['end_x_axis']),
                # 'reqCoordType': "WGS84GEO",
                'startName': "안뇽",
                'endName': "잘가",
                }
        print(body)
        r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))

        print(r)
        while str(r) != "<Response [200]>":
            print(r)
            r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
        ret_data =[]
        for element in r.json()['features']:
            if element['geometry']['type'] == 'LineString':
                # print(element['geometry']['coordinates'])
                for point in element['geometry']['coordinates']:
                    temp_point = {}
                    temp_point['x_axis'] = point[1]
                    temp_point['y_axis'] = point[0]
                    if temp_point not in ret_data:
                        ret_data.append(temp_point)
        ret_dict = dict()
        ret_dict['path'] = ret_data
        print(ret_dict)
        return JsonResponse(ret_dict)
