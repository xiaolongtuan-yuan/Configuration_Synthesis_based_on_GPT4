# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/12 19:48
@Auth ： xiaolongtuan
@File ：NetworkDes.py
"""
import json


class NetworkDes:
    def __init__(self, network_name: str, AS_count: int, AS_list: [], edges: [], high_require:str):
        self.network_name = network_name,
        self.AS_count = AS_count
        self.AS = {}
        self.high_require = high_require
        for AS in AS_list:
            self.AS[AS.AS_name] = AS

        self.edges = {}
        self.edge_list = edges
        for edge in edges:
            edge_l = self.edges.get(edge[0])
            if edge_l:
                edge_l.append(edge[1])
            else:
                edge_l = [edge[1]]
                self.edges[edge[0]] = edge_l

            edge_r = self.edges.get(edge[1])
            if edge_r:
                edge_r.append(edge[0])
            else:
                edge_r = [edge[0]]
                self.edges[edge[1]] = edge_r

    def get_advice_of_AS(self, AS_name):
        AS = self.AS.get(AS_name)
        if AS:
            return list(AS.devices.keys())
        else:
            raise Exception(f"不存在名为{AS_name}的AS")

    def get_border_advice_of_AS(self, AS_name):
        AS = self.AS.get(AS_name)
        if AS:
            borders = []
            devices = list(AS.devices.values())
            for device in devices:
                if device.device_type == "border":
                    borders.append(device.device_name)
            return borders
        else:
            raise Exception(f"不存在名为{AS_name}的AS")

    def get_all_device(self):
        devices = []
        for AS in list(self.AS.values()):
            devices += list(AS.devices.keys())
        return devices

    def get_all_type_of_devices(self):
        devices = {}
        devices['core'] = []
        devices['border']=[]
        devices['host']=[]
        for AS in list(self.AS.values()):
            for device in list(AS.devices.values()):
                devices.get(device.device_type).append(device.device_name)

        return devices



class AS:
    def __init__(self, AS_name: str, devices: []):
        self.AS_name = AS_name
        self.devices = {}
        for device in devices:
            self.devices[device.device_name] = device

    def get_device(self, device_name):
        return self.devices[device_name]


class Device:
    def __init__(self, device_id: int, device_name: str, device_type: str):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type # core,border,host


def json_2_NetworkDes(net_json_path):
    with open(net_json_path, 'r') as file:
        # 加载 JSON 数据
        net_dic = json.load(file)
    network_name = net_dic.get("network_name")
    AS_count = net_dic.get('AS_count')

    AS_dic_list = net_dic.get('AS')
    edges = net_dic.get('edges')
    high_require = net_dic.get('high_require')

    AS_list = []
    for AS_dic in AS_dic_list:
        AS_name = AS_dic.get("AS_name")
        devices = []
        devices_dic_list = AS_dic.get("devices")
        '''
        {
          "device_id": 1,
          "device_name": "AS1border1",
          "device_type": "border"
        },
        '''
        for device_dic in devices_dic_list:
            device_id = device_dic.get('device_id')
            device_name = device_dic.get('device_name')
            device_type = device_dic.get('device_type')
            device = Device(device_id, device_name, device_type)
            devices.append(device)

        as_obj = AS(AS_name, devices)
        AS_list.append(as_obj)

    network_des = NetworkDes(network_name=network_name, AS_count=AS_count, AS_list=AS_list, edges=edges,high_require=high_require)
    return network_des


if __name__ == '__main__':
    json_path = "../network_json/3AS_network.json"

    network = json_2_NetworkDes(json_path)
    print("1")
