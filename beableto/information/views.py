from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import LocationSerializer, BusSerializer, RoadSerializer, FragmentSerializer, CurPoseSerializer, ElevatorSerializer, HelpSerializer
from .models import Location, Bus, Fragment, Road, Record, Elevator, Help
from accounts.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
import googlemaps
from .utilities import bracket_clear, arg_max, check_area, spacebar_clear
from .utilities import MarkerClass, FragmentClass, UserRankClass
import json
import requests
import datetime, time
from django.db.models import Q
from math import sqrt
import operator


class LocationSaveView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)
        rq_data['user'] = request.user.pk
        rq_data['location_name'] = rq_data['location_name'][0]
        rq_data['x_axis'] = rq_data['x_axis'][0]
        rq_data['y_axis'] = rq_data['y_axis'][0]
        rq_data['slope'] = rq_data['slope'][0]
        rq_data['location_address'] = rq_data['location_address'][0]
        rq_data['auto_door'] = rq_data['auto_door'][0]
        rq_data['elevator'] = rq_data['elevator'][0]
        rq_data['toilet'] = rq_data['toilet'][0]

        if rq_data.get('image') != None:
            rq_data['image'] = rq_data['image'][0]
        if rq_data.get('comment') != None:
            rq_data['comment'] = rq_data['comment'][0]


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


class LocationGetAllMarkersVIew(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # info = Location.objects.filter(x_axis=rq_data['x_axis'][0], y_axis=rq_data['y_axis'][0])
        info = Location.objects.filter()

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
    queryset = Road.objects.all()
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
        start = time.time()
        rq_data = dict(request.data)
        with open('tmap.txt') as f:
            tmap_api_key = f.readline()
            f.close()
        with open('googlemaps.txt') as f:
            gmap_api_key = f.readline()
            f.close()
        gmaps = googlemaps.Client(key=gmap_api_key)
        # dt = datetime.datetime.now()
        d = datetime.date(2019, 12, 2)
        t = datetime.time(14, 23, 38)
        dt = datetime.datetime.combine(d, t)
        di = gmaps.directions((str(rq_data['start_x_axis']), str(rq_data['start_y_axis'])), (str(rq_data['end_x_axis']), str(rq_data['end_y_axis'])), mode="transit", departure_time=dt, alternatives=True, language="ko")
        print(rq_data)
        paths = {}
        path_list = []
        for path_index in range(0, len(di)):
            path = {}
            sub_path_list = []
            for sub_google_path in range(len(di[path_index]['legs'][0]['steps'])):
                sub_path = {}

                # Front의 요청에 의한 포멧팅
                sub_path['type'] = None
                sub_path['time'] = None
                sub_path['color'] = None
                sub_path['departure'] = None
                sub_path['arrival'] = None

                # Walk 필드
                sub_path['walk_start_x'] = None
                sub_path['walk_start_y'] = None
                sub_path['walk_end_x'] = None
                sub_path['walk_end_y'] = None
                sub_path['walk_seq'] = None
                sub_path['walk_sub'] = None

                # Bus 필드
                sub_path['bus_start_x'] = None
                sub_path['bus_start_y'] = None
                sub_path['bus_end_x'] = None
                sub_path['bus_end_y'] = None
                sub_path['bus_line'] = None
                sub_path['bus_area'] = None
                sub_path['bus_height'] = None
                sub_path['bus_poly'] = None

                # Train 필드
                sub_path['train_start_x'] = None
                sub_path['train_start_y'] = None
                sub_path['train_end_x'] = None
                sub_path['train_end_y'] = None
                sub_path['train_line'] = None
                sub_path['train_poly'] = None
                sub_path['time'] = di[path_index]['legs'][0]['steps'][sub_google_path]['duration']

                if str(di[path_index]['legs'][0]['steps'][sub_google_path]['travel_mode']) == "TRANSIT":
                    if "지하철" in di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name'] or "전철" in di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name']:
                        sub_path['type'] = "train"
                        sub_path['train_start_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat']
                        sub_path['train_start_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']
                        sub_path['train_end_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lat']
                        sub_path['train_end_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lng']
                        sub_path['train_line'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['short_name']
                        sub_path['train_poly'] = di[path_index]['legs'][0]['steps'][sub_google_path]['polyline']['points']
                        sub_path['color'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['color']
                        sub_path['departure'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['departure_stop']['name']
                        sub_path['arrival'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['arrival_stop']['name']
                    elif "버스" in di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name'] and "고속버스" not in di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name']:
                        sub_path['type'] = "bus"
                        sub_path['bus_start_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat']
                        sub_path['bus_start_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']
                        sub_path['bus_end_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lat']
                        sub_path['bus_end_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lng']
                        sub_path['bus_poly'] = di[path_index]['legs'][0]['steps'][sub_google_path]['polyline']['points']
                        sub_path['color'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['color']
                        sub_path['departure'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['departure_stop']['name']
                        sub_path['arrival'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['arrival_stop']['name']
                        if 'short_name' in di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']:
                            sub_path['bus_line'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['short_name']
                        else:
                            sub_path['bus_line'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name']
                        sub_path['bus_area'] = di[path_index]['legs'][0]['steps'][sub_google_path]['transit_details']['line']['name'][:2]

                        info = Bus.objects.filter(area=sub_path['bus_area'], line=sub_path['bus_line'])
                        height = [0] * 3
                        info_size = 0
                        for obj in info:
                            info_size += 1
                            obj_dict = obj.as_dict()
                            height[obj_dict['height']] += 1
                        if info_size is 0:
                            sub_path['bus_height'] = 2
                        else:
                            sub_path['bus_height'] = arg_max(height)
                    else:
                        # 나중에 다시 봐야됨 (버스, 지하철 아닌 경우)
                        continue
                else:
                    sub_path['type'] = "walk"
                    sub_path['walk_start_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat']
                    sub_path['walk_start_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']
                    sub_path['walk_end_x'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lat']
                    sub_path['walk_end_y'] = di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lng']
                    sub_path['walk_seq'] = None

                    headers = {'Accept': "application/json",
                               # 'Content-Type': "application/json; charset=UTF-8",
                               'appKey': tmap_api_key,
                               'Accept-Language': "ko",
                               }
                    # 우리 (x, y)와 T-MAP(x, y) 순서 다름
                    body = {'startX': str(di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']),
                            'startY': str(di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat']),
                            'endX': str(di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lng']),
                            'endY': str(di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lat']),
                            'startName': "안뇽",
                            'endName': "잘가",
                            'searchOption': 30
                            }
                    add = True
                    if sub_google_path < len(di[path_index]['legs'][0]['steps']) - 1:
                        if "지하철" in di[path_index]['legs'][0]['steps'][sub_google_path + 1]['transit_details']['line']['name'] or "전철" in di[path_index]['legs'][0]['steps'][sub_google_path + 1]['transit_details']['line']['name']:
                            if "서울" in di[path_index]['legs'][0]['steps'][sub_google_path + 1]['transit_details']['line']['name']:
                                elevator = Elevator.objects.filter()
                                for obj in elevator:
                                    ele_dict = obj.as_dict()
                                    if ele_dict['station'] in di[path_index]['legs'][0]['steps'][sub_google_path + 1]['transit_details']['departure_stop']['name']:
                                        add = False
                                        body = {'startX': str(di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']),
                                                'startY': str(di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat']),
                                                'endX': str(ele_dict['y_axis']),
                                                'endY': str(ele_dict['x_axis']),
                                                'startName': "안뇽",
                                                'endName': "잘가",
                                                'searchOption': 30
                                                }
                                        sub_path['walk_sub'] = ele_dict['description']

                    r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))

                    for i in range(4):
                        if str(r) != "<Response [200]>":
                            print(r)
                            r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
                        else:
                            break
                    road_seq = [[di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lat'], di[path_index]['legs'][0]['steps'][sub_google_path]['start_location']['lng']]]
                    for element in r.json()['features']:
                        if element['geometry']['type'] == 'LineString':
                            # print(element['geometry']['coordinates'])
                            for point in element['geometry']['coordinates']:
                                road_point = [point[1], point[0]] # 좌표계 변환
                                if road_point not in road_seq:
                                    road_seq.append(road_point)
                    if add:
                        road_seq.append([di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lat'], di[path_index]['legs'][0]['steps'][sub_google_path]['end_location']['lng']])
                    roads = []
                    walk_seq = []
                    for i in range(len(road_seq) - 1):
                        road = [road_seq[i], road_seq[i + 1]]
                        roads.append(road)

                    for road in roads:
                        road_info = {
                            'start_x': road[0][0],
                            'start_y': road[0][1],
                            'end_x': road[1][0],
                            'end_y': road[1][1],
                        }
                        avg_point = [(road[0][0] + road[1][0]) / 2, (road[0][1] + road[1][1]) / 2]
                        k = 0.0002 # 도로 폭 상수 (2k)
                        walk_vgis = Fragment.objects.filter(middle_x__range=(avg_point[0] - k * 10, avg_point[0] + k * 10), middle_y__range=(avg_point[1] - k * 10, avg_point[1] + k * 10))
                        vgi_roads = []
                        count = 0
                        for obj in walk_vgis:
                            count += 1
                            obj_dict = obj.as_dict()
                            vgi_road = [[obj_dict['start_x'], obj_dict['start_y'], obj_dict['slope']], [obj_dict['end_x'], obj_dict['end_y'], obj_dict['slope']]]
                            vgi_roads.append(vgi_road)
                        if count >= 1:
                            cur_slope = check_area(road, vgi_roads, k)
                        else:
                            cur_slope = 3
                        road_info['slope'] = cur_slope
                        walk_seq.append(road_info)
                    sub_path['walk_seq'] = walk_seq

                sub_path_list.append(sub_path)
            path['path'] = sub_path_list
            path_list.append(path)

        # WALK ONLY PATH -----------------------------------------------------------------------------
        headers = {'Accept': "application/json",
                   # 'Content-Type': "application/json; charset=UTF-8",
                   'appKey': tmap_api_key,
                   'Accept-Language': "ko",
                   }
        # 우리 (x, y)와 T-MAP(x, y) 순서 다름
        body = {'startX': str(rq_data['start_y_axis']),
                'startY': str(rq_data['start_x_axis']),
                'endX': str(rq_data['end_y_axis']),
                'endY': str(rq_data['end_x_axis']),
                'startName': "안뇽",
                'endName': "잘가",
                'searchOption': 30
                }
        r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
        for i in range(4):
            if str(r) != "<Response [200]>" and str(r) != "<Response [204]>" and str(r) != "<Response [500]>":
                print(r)
                r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
            else:
                break
        if str(r) == "<Response [200]>":
            path = {}
            sub_path_list = []
            sub_path = {}

            road_seq = [[float(rq_data['start_x_axis']), float(rq_data['start_y_axis'])]]
            for element in r.json()['features']:
                if element['geometry']['type'] == 'LineString':
                    # print(element['geometry']['coordinates'])
                    for point in element['geometry']['coordinates']:
                        road_point = [point[1], point[0]]  # 좌표계 변환
                        if road_point not in road_seq:
                            road_seq.append(road_point)
            road_seq.append([float(rq_data['end_x_axis']), float(rq_data['end_y_axis'])])

            roads = []
            walk_seq = []
            for i in range(len(road_seq) - 1):
                road = [road_seq[i], road_seq[i + 1]]
                roads.append(road)

            for road in roads:
                road_info = {
                    'start_x': float(road[0][0]),
                    'start_y': float(road[0][1]),
                    'end_x': float(road[1][0]),
                    'end_y': float(road[1][1]),
                }
                avg_point = [(float(road[0][0]) + float(road[1][0])) / 2, (float(road[0][1]) + float(road[1][1])) / 2]
                k = 0.0002  # 도로 폭 상수 (2k)
                walk_vgis = Fragment.objects.filter(middle_x__range=(avg_point[0] - k * 10, avg_point[0] + k * 10),
                                                    middle_y__range=(avg_point[1] - k * 10, avg_point[1] + k * 10))
                vgi_roads = []
                count = 0
                for obj in walk_vgis:
                    count += 1
                    obj_dict = obj.as_dict()
                    vgi_road = [[obj_dict['start_x'], obj_dict['start_y'], obj_dict['slope']],
                                [obj_dict['end_x'], obj_dict['end_y'], obj_dict['slope']]]
                    vgi_roads.append(vgi_road)
                if count >= 1:
                    cur_slope = check_area(road, vgi_roads, k)
                else:
                    cur_slope = 3
                road_info['slope'] = cur_slope
                walk_seq.append(road_info)
            sub_path['walk_seq'] = walk_seq

            # Front의 요청에 의한 포멧팅
            sub_path['type'] = 'walk'
            sub_path['time'] = None
            sub_path['color'] = None

            # Walk 필드
            sub_path['walk_start_x'] = rq_data['start_x_axis']
            sub_path['walk_start_y'] = rq_data['start_y_axis']
            sub_path['walk_end_x'] = rq_data['end_x_axis']
            sub_path['walk_end_y'] = rq_data['end_y_axis']

            # Bus 필드
            sub_path['bus_start_x'] = None
            sub_path['bus_start_y'] = None
            sub_path['bus_end_x'] = None
            sub_path['bus_end_y'] = None
            sub_path['bus_line'] = None
            sub_path['bus_area'] = None
            sub_path['bus_height'] = None

            # Train 필드
            sub_path['train_start_x'] = None
            sub_path['train_start_y'] = None
            sub_path['train_end_x'] = None
            sub_path['train_end_y'] = None
            sub_path['train_line'] = None

            sub_path_list.append(sub_path)
            path['path'] = sub_path_list
            path_list.append(path)
        paths['paths'] = path_list

        print("time :", time.time() - start)
        return JsonResponse(paths)


class RoadSaveView(generics.ListCreateAPIView):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)
        db_data = {}
        db_data['user'] = request.user.pk

        # Saving Basic VGI Information
        road_str = ""
        road_list = []
        for point in request.data['coordinate']:
            point_list = []
            road_str += str(point['x_axis'])
            point_list.append(float(point['x_axis']))
            road_str += " "
            road_str += str(point['y_axis'])
            point_list.append(float(point['y_axis']))
            road_str += " "
            road_list.append(point_list)
        db_data['road'] = road_str
        db_data['slope'] = rq_data['slope']
        serializer = self.get_serializer(data=db_data)
        serializer.is_valid(raise_exception=True)
        # perform_create overriding 귀찮아서 그냥 Create
        obj = Road.objects.create(
            road=road_str,
            slope=rq_data['slope'],
        )

        # Saving Fragments
        for i in range(len(road_list) - 1):
            Fragment.objects.create(
                road=obj,
                start_x=road_list[i][0],
                start_y=road_list[i][1],
                end_x=road_list[i + 1][0],
                end_y=road_list[i + 1][1],
                middle_x=((road_list[i][0] + road_list[i + 1][0]) / 2),
                middle_y=((road_list[i][1] + road_list[i + 1][1]) / 2),
                slope=rq_data['slope'],
            )

        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED)


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

        for i in range(10):
            if str(r) != "<Response [200]>":
                print(r)
                r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
                break
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
        return JsonResponse(ret_dict)


class CurPoseSaveView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Record.objects.all()
    serializer_class = CurPoseSerializer

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)

        rq_data['user'] = request.user.pk
        rq_data['time'] = datetime.datetime.now()

        serializer = self.get_serializer(data=rq_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class GetPositionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)

        limit = datetime.datetime.now() - datetime.timedelta(hours=rq_data['time'])
        info = Record.objects.filter(user_id=request.user.pk)

        res_list = []

        for obj in info:
            obj_dict = obj.as_dict()
            if obj_dict['time'] > limit:
                res_list.append(obj_dict)

        pos = dict()
        pos['locations'] = res_list
        return JsonResponse(pos)


class GetFragmentsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        print(rq_data)

        info = Fragment.objects.filter(Q(start_x__range=(float(rq_data['lsx']), float(rq_data['rnx'])), start_y__range=(float(rq_data['lsy']), float(rq_data['rny']))) | Q(end_x__range=(float(rq_data['lsx']), float(rq_data['rnx'])), end_y__range=(float(rq_data['lsy']), float(rq_data['rny']))))

        index = 0
        fragmet_list = []
        cord_dict = {}
        fragment_set = set()
        for obj in info:
            obj_dict = obj.as_dict()
            obj_cord = (obj_dict['start_x'], obj_dict['start_y'], obj_dict['end_x'], obj_dict['end_y'])
            if obj_cord in fragment_set:
                key = str(obj_dict['start_x']) + str(obj_dict['start_y']) + str(obj_dict['end_x']) + str(obj_dict['end_y'])
                fragment_index = cord_dict[key]
                fragmet_list[fragment_index].updateValue(obj_dict['slope'])
            else:
                fragment_set.add(obj_cord)
                key = str(obj_dict['start_x']) + str(obj_dict['start_y']) + str(obj_dict['end_x']) + str(obj_dict['end_y'])
                cord_dict[key] = index
                index += 1
                newFragment = FragmentClass(obj_dict['start_x'], obj_dict['start_y'], obj_dict['end_x'], obj_dict['end_y'], obj_dict['slope'])
                fragmet_list.append(newFragment)

        ret_list = []
        for f in fragmet_list:
            ret_list.append(f.getAsDict())
        fragment = dict()
        fragment['fragments'] = ret_list
        return JsonResponse(fragment)


class GetInfoByNameView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        info = Location.objects.filter()

        index = 0
        marker_list = []
        cord_dict = {}
        marker_set = set()
        for obj in info:
            obj_dict = obj.as_dict()
            add = []
            rq_data['name'] = spacebar_clear(rq_data['name'])
            if obj_dict['location_name'] in rq_data['name'] or rq_data['name'] in obj_dict['location_name']:
                obj_cord = (obj_dict['x_axis'], obj_dict['y_axis'])
                if obj_cord in marker_set:
                    key = str(obj_cord[0]) + " " + str(obj_cord[1])
                    marker_index = cord_dict[key]
                    marker_list[marker_index].updataValue(obj_dict['slope'], obj_dict['auto_door'], obj_dict['elevator'], obj_dict['toilet'])
                else:
                    add.append(obj_dict['location_address'])
                    marker_set.add(obj_cord)
                    key = str(obj_cord[0]) + " " + str(obj_cord[1])
                    cord_dict[key] = index
                    index += 1
                    newMarker = MarkerClass(obj_cord[0], obj_cord[1], obj_dict['slope'], obj_dict['auto_door'], obj_dict['elevator'], obj_dict['toilet'], obj_dict['location_name'])
                    marker_list.append(newMarker)

        ret_list = []
        m_index = 0
        for m in marker_list:
            # j = json.dumps(d)
            # j = j[1:-1]
            temp_m = m.getAsDict()
            temp_m['address'] = bracket_clear(add[m_index])
            ret_list.append(temp_m)
            m_index += 1
        markers = dict()
        markers['markers'] = ret_list
        return JsonResponse(markers)


class ElevatorSaveView(generics.ListCreateAPIView):
    serializer_class = ElevatorSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)

        serializer = self.get_serializer(data=rq_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class HelpSaveView(generics.ListCreateAPIView):
    serializer_class = HelpSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rq_data = dict(request.data)

        serializer = self.get_serializer(data=rq_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)


class GetHelpView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        rq_data = dict(request.data)
        info = Help.objects.filter()

        min_val = 9999999999
        min_obj = None

        for obj in info:
            obj_dict = obj.as_dict()
            val = sqrt((obj_dict['x_axis'] - rq_data['x']) ** 2 + (obj_dict['y_axis'] - rq_data['y']) ** 2)
            if val <= min_val:
                min_val = val
                min_obj = obj_dict

        return JsonResponse(min_obj)


class GetRank(APIView):
    serializer_class = BusSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        rq_data = dict(request.data)

        user_info = User.objects.filter()

        user_list = []
        for obj in user_info:
            obj_dict = obj.as_dict()
            user_list.append(UserRankClass(obj_dict['id'], obj_dict['email']))

        for usr in user_list:
            l = Location.objects.filter(user_id=usr.id)
            usr.add_point(len(l) * 5)
            b = Bus.objects.filter(user_id=usr.id)
            usr.add_point(len(b) * 2)
            r = Road.objects.filter(user_id=usr.id)
            usr.add_point(len(r) * 10)
        user_list = sorted(user_list, key=operator.attrgetter('point'), reverse=True)
        user_dict_list = []
        rank = 1
        for usr in user_list:
            temp = usr.as_dict()
            temp['rank'] = rank
            user_dict_list.append(temp)
            rank += 1
        ret_dict = {
            'ranking': user_dict_list[:9]
        }
        for i in range(len(user_list)):
            if user_list[i].id is request.user.pk:
                ret_dict['my_rank'] = user_dict_list[i]

        return JsonResponse(ret_dict)