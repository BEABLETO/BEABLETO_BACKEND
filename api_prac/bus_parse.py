with open('parse.txt', 'rt', encoding='UTF8') as f:
    cur_bus = "0"
    line = f.readline()
    bus_list = []
    while line:
        if "tr id" in line:
            cur_bus = line[8:-3]
            bus_list.append(cur_bus)
        line = f.readline()
    for i in bus_list:
        print(i)
    f.close

# with open('parse.txt', 'rt', encoding='UTF8') as f:
#     cur_bus = "0"
#     line = f.readline()
#     bus_list = []
#     while line:
#         if "<th>" in line and len(line) < 10:
#             cur_bus = line[4:-1]
#             bus_list.append(cur_bus)
#         # if "저상버스" in line:
#         #     bus_list.remove(cur_bus)
#         line = f.readline()
#     for i in bus_list:
#         print(i)
#     f.close