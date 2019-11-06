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

# def is_in_box(box, point):


