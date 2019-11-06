from math import sqrt

def bracket_clear(string):
    if string.startswith('\"'):
        string = string[1:]
    if string.endswith('\"'):
        string = string[:-1]
    return string


class MarkerClass:
    # Variables
    x = 0.0
    y = 0.0
    data_size = 1
    slope_sum = 0
    auto_door = 0
    elevator = 0
    toilet = 0

    # Functions
    def __init__(self, x, y, slope, auto_door, elevator, toilet, name):
        self.location_name = ""
        self.x = x
        self.y = y
        self.slope_sum += slope
        if auto_door:
            self.auto_door += 1
        if elevator:
            self.elevator += 1
        if toilet:
            self.toilet += 1
        self.location_name = bracket_clear(name)


    def isSame(self, x, y):
        if self.x == x and self.y == y:
            return True
        return False

    def updataValue(self, slope, auto_door, elevator, toilet):
        self.data_size += 1
        self.slope_sum += slope
        if auto_door:
            self.auto_door += 1
        if elevator:
            self.elevator += 1
        if toilet:
            self.toilet += 1

    def getValue(self):
        if self.auto_door >= int(self.data_size) / 2:
            auto_door_return = True
        else:
            auto_door_return = False

        if self.elevator >= int(self.data_size) / 2:
            elevator_return = True
        else:
            elevator_return = False

        if self.toilet >= int(self.data_size) / 2:
            toilet_return = True
        else:
            toilet_return = False

        return self.slope_sum / self.data_size, auto_door_return, elevator_return, toilet_return

    def getAsDict(self):
        if self.auto_door >= int(self.data_size) / 2:
            auto_door_return = True
        else:
            auto_door_return = False

        if self.elevator >= int(self.data_size) / 2:
            elevator_return = True
        else:
            elevator_return = False

        if self.toilet >= int(self.data_size) / 2:
            toilet_return = True
        else:
            toilet_return = False

        return_dict = {"location_name": self.location_name,
                       "x_axis": self.x,
                       "y_axis": self.y,
                       "slope": round(self.slope_sum / float(self.data_size)),
                       "auto_door": auto_door_return,
                       "elevator": elevator_return,
                       "toilet": toilet_return
                       }

        return return_dict


def arg_max(l):
    max_index = 0
    max = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i];
            max_index = i

    return max_index


def tri_area(points):
    a = sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
    b = sqrt((points[1][0] - points[2][0])**2 + (points[1][1] - points[2][1])**2)
    c = sqrt((points[0][0] - points[2][0])**2 + (points[0][1] - points[2][1])**2)
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


def pl_len(road, point):
    if road[0][0] != road[1][0]:
        a = (road[0][1] - road[1][1]) / (road[0][0] - road[1][0])
        b = road[0][1] - a * road[0][0]
        # ax - y + b = 0
        return abs(a * point[0] + (-1.0) * point[1] + b) / (sqrt(a**2 + (-1.0)**2))
    else:
        return abs(point[0] - road[0][0])


def find_foot(road, x1, y1):
    if road[0][0] != road[1][0]:
        a = (road[0][1] - road[1][1]) / (road[0][0] - road[1][0])
        b = -1.0
        c = road[0][1] - a * road[0][0]
        temp = (-1 * (a * x1 + b * y1 + c) / (a * a + b * b))
        x = temp * a + x1
        y = temp * b + y1
    else:
        x = road[0][0]
        y = y1
    return x, y

def is_bound(a, b, c):
    if a > b:
        if b <= c <= a:
            return True
        return False
    else:
        if a <= c <= b:
            return True
        return False


# road example : [[1, 2], [3, 4]]
def check_area(road, vgi_roads, k):
    info = [0] * 3
    for vgi_road in vgi_roads:
        for point in vgi_road:
            fpoint = find_foot(road, point[0], point[1])
            if pl_len(road, point) <= k and is_bound(road[0][0], road[1][0], fpoint[0]) and is_bound(road[0][1], road[1][1], fpoint[1]):
                info[point[2]] += 1
                break
    print(info)
    if info[0] + info[1] + info[2] > 0:
        return arg_max(info)
    else:
        return 3


# 테스트
vgi_roads = [[[2, 0.5, 2], [3, 2, 2]], [[7, 4, 3], [9, 5, 3]], [[1, 0.5, 1], [3, 2, 1]], [[0.4, 0.7, 2], [0.4, 0.8, 2]]]
road = [[0, 0], [5, 0]]
check_area(road, vgi_roads, 1)


