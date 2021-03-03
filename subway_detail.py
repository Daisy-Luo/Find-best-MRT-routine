# -*-  coding: utf-8 -*-
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def get_subway_list(id, city):
    url = "http://map.amap.com/service/subway?_1579413847829&srhdata=%s_drw_%s.json" % (id, city)
    mrt_detail_json = json.loads(requests.get(url=url).content.decode('utf-8'))

    mrt_line_name = []
    mrt_station_name_en = []
    mrt_station_name_ch = []
    mrt_station_latlong = []
    mrt_station_poiid = []

    for line in mrt_detail_json['l']:
        for st in line['st']:
            mrt_line_name.append(line['kn'])
            mrt_station_name_en.append(st['sp'])
            mrt_station_name_ch.append(st['n'])
            mrt_station_latlong.append((float(st['sl'].split(',')[0]), float(st['sl'].split(',')[1])))
            mrt_station_poiid.append(st['poiid'])

    mrt_list = pd.DataFrame()
    mrt_list['mrt_line'] = mrt_line_name
    mrt_list['mrt_sta_name_ch'] = mrt_station_name_ch
    mrt_list['mrt_sta_name_en'] = mrt_station_name_en
    mrt_list['mrt_sta_latlong'] = mrt_station_latlong
    mrt_list['mrt_sta_poiid'] = mrt_station_poiid
    # print(mrt_list)
    return mrt_list


def get_mrt_latlong_info(mrt_list):
    mrt_dictionary = {}
    for i in range(len(mrt_list)):
        mrt_dictionary[mrt_list.iloc[i,1]] = mrt_list.iloc[i, 3]
    return mrt_dictionary


def draw_graph_1(mrt_dictionary):
    mrt_graph = nx.Graph()
    mrt_graph.add_nodes_from(list(mrt_dictionary.keys()))
    nx.draw(mrt_graph, mrt_dictionary, with_labels=True, node_size = 2, font_size=5)
    plt.show()


def draw_graph_2(mrt_latlong, mrt_connections):
    graph = nx.Graph(mrt_connections)
    nx.draw(graph, mrt_latlong, with_labels=True, node_size = 2, font_size=5)
    plt.show()


def get_mrt_connect_station(mrt_list):
    mrt_list['connection'] = [list() for x in range(len(mrt_list))]
    for i in range(len(mrt_list)-1):
        if mrt_list.loc[len(mrt_list)-1 - i,'mrt_line'] == mrt_list.loc[len(mrt_list)-1 - (i+1), 'mrt_line']:
            mrt_list.loc[len(mrt_list)-1 - i, 'connection'].append(mrt_list.loc[len(mrt_list)-1 - (i+1), 'mrt_sta_name_ch'])

    for i in range(len(mrt_list)-1):
        if mrt_list.loc[i,'mrt_line'] == mrt_list.loc[i+1, 'mrt_line']:
            mrt_list.loc[i, 'connection'].append(mrt_list.loc[i+1, 'mrt_sta_name_ch'])
    # print(mrt_list[['mrt_line', 'mrt_sta_name_ch', 'connection']])
    for i in range(len(mrt_list)):
        for j in range(len(mrt_list)):
            if mrt_list.loc[i, 'mrt_sta_name_ch'] == mrt_list.loc[j, 'mrt_sta_name_ch'] and (i != j):
                for item in mrt_list.loc[j, 'connection']:
                    mrt_list.loc[i, 'connection'].append(item)

    # for i in range(len(mrt_list)):
    #     print(mrt_list.loc[i,['mrt_line', 'mrt_sta_name_ch', 'connection']])
    mrt_list['connection'] = mrt_list['connection'].apply(lambda x: list(set(x)))
    mrt_connections = {}
    for i in range(len(mrt_list)):
        mrt_connections[mrt_list.iloc[i,1]] = mrt_list.iloc[i,5]

    return mrt_connections


if __name__ == '__main__':
    mrt_list = get_subway_list(1100, 'beijing')
    # for i in range(len(mrt_list)):
    #     for j in range(i+1, len(mrt_list)):
    #         if mrt_list.loc[i, 'mrt_sta_latlong'] == mrt_list.loc[j, 'mrt_sta_latlong']:
    #             print(mrt_list.loc[i, ['mrt_line', 'mrt_sta_name_ch', 'mrt_sta_latlong']])
    #             print(mrt_list.loc[j, ['mrt_line', 'mrt_sta_name_ch', 'mrt_sta_latlong']])
    mrt_connections = get_mrt_connect_station(mrt_list)
    mrt_laglong_info = get_mrt_latlong_info(mrt_list)
    draw_graph_2(mrt_latlong=mrt_laglong_info, mrt_connections=mrt_connections)

