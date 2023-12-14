# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/30 19:30
@Auth ： xiaolongtuan
@File ：network_verify.py
"""
from utils.check_policy import *

if __name__ == '__main__':
    network = "simple_gen"
    if check_syntax(network):
        print("未发现语法错误")
    if check_reachable(network=network,r1="border1",r2="core1",dis="host-db"):
        print("从border1到host-db的流量必须经过core1：成功")
    else:
        print("从border1到host-db的流量必须经过core1: 失败")

    if check_reachable(network=network,r1="border2",r2="core2",dis="host-db"):
        print("从border2到host-db的流量绕过core2: 失败")
    else:
        print("从border2到hostdb的流量绕过core2：成功")

    device_list = ["leaf1", "spine1", "spine2", "core1", "core2", "border1", "border2"]

    for device in device_list:
        if check_connect(network=network,start=device,end="host-db"):
            print(f"{device}----host_db: 可达")
        else:
            print(f"{device}----host_db: 不可达")

