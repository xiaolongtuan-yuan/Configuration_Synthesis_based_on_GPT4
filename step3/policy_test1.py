# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/4 14:17
@Auth ： xiaolongtuan
@File ：policy_test1.py
"""
from utils.load_policy import recognize_policy,check_module
from init import client
# if __name__ == '__main__':
#     print(recognize_policy(client=client,file_path="utils/test/policy_test1.txt"))

if __name__ == '__main__':
    network = "simple_gen"
    policy_dic = recognize_policy(client=client, file_path="../utils/test/policy_test2.txt")
    flag, messages = check_module(network=network,policy_dic=policy_dic)
    print(flag)
    print(messages)
