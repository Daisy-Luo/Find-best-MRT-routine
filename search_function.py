# -*- coding: utf-8 -*-

import math
from subway_detail import get_subway_list, get_mrt_connect_station, get_mrt_latlong_info

# ----------------------------- search functions --------------------

def search_BFS(graph, start, destination):
    pathes = [[start]]
    visited = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in visited:
            continue

        successors = graph[froniter]

        for city in successors:
            if city in path:
                continue

            new_path = path + [city]

            pathes.append(new_path)

            if city == destination:
                return new_path
        visited.add(froniter)

def search_DFS(graph, start, destination):
    pathes = [[start]]
    visited = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in visited:
            continue

        successors = graph[froniter]

        for city in successors:
            if city in path:
                continue

            new_path = path + [city]

            pathes = [new_path] + pathes

            if city == destination:
                return new_path
        visited.add(froniter)

def search_BFS_optimal(graph, start, destination, search_strategy):
    pathes = [[start]]
    visited = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in visited:
            continue
        if froniter == destination:
            return path
        successor = graph[froniter]

        for city in successor:
            if city in path:
                continue

            new_path = path + [city]
            pathes.append(new_path)

        pathes = search_strategy(pathes)
        visited.add(froniter)

        # if pathes and (destination == pathes[0][-1]):
        #     return pathes[0]
# ---------------------------------------------------------------------------

# ---------------------------------------- distance--------------------------
def sort_by_distance(pathes):
    def get_distance_of_path(path):
        distance = 0
        for i, j in enumerate(path[:-1]):
            distance += get_distance(path[i], path[i+1])
        return distance
    return sorted(pathes, key=get_distance_of_path)


def sort_by_transfer(pathes):    # 缺点，可能会选择到一条绕一大弯的路线，比如路线1在第二站换乘，路线2在第八站换乘，会有限选择第二条路线！！！！！
    # pathes, 遍历path[i] 和 path[i+2] 是不是同一条线，若不是，transfer 加1
    def get_transfer_of_path(path):
        path_line = []
        for sta in path:
            path_line.append(list(station_list[station_list['mrt_sta_name_ch'] == sta]['mrt_line']))
        transfer = 0
        for i in range(len(path_line) - 2):
            if not [j for j in path_line[i] if j in path_line[i + 2]]:
                # print('path:： ', path_line[i + 1], 'transfer to', path_line[i + 2])
                transfer += 1
        return transfer
    return sorted(pathes, key=get_transfer_of_path)




def get_distance(origin, destination):
    """
        Calculate the Haverisine distance.

        origin: tuple of float (lat, long)
        destination: tuple of float (lat, long)

        Return: distance_in_km: float
        """
    lat1, long1 = mrt_dictionary[origin]
    lat2, long2 = mrt_dictionary[destination]
    radius = 6371  # 地球半径为6,371 km

    dlat = math.radians(lat2 - lat1)
    dlong = math.radians(long2 - long1)

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlong / 2) * math.sin(dlong / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


# ---------------------------------------------------------------------------------------------
station_list = get_subway_list(1100, 'beijing')


mrt_connections = get_mrt_connect_station(station_list)
mrt_dictionary = get_mrt_latlong_info(station_list)

print(search_BFS_optimal(mrt_connections, start='北京西站', destination='北土城', search_strategy=sort_by_transfer))





