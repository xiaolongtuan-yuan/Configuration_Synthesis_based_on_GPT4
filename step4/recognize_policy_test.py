# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/12 13:38
@Auth ： xiaolongtuan
@File ：recognize_policy_test.py
"""
from utils.load_policy import recognize_policy
from step4.polish_require import polish_bgp, polish_ospf
from init import client

if __name__ == '__main__':
    polished_policys = []
    str = recognize_policy(client=client, file_path="test_data/ospf_text.txt", system_prompt_path="system_prompt/BGP_recognize.txt")
    bgp_policys = str.get("result")
    for bgp_req_dic in bgp_policys:
        polished_str = polish_bgp(bgp_req_dic)
        if polished_str:
            polished_policys.append(polished_str)
    str = recognize_policy(client=client,file_path="test_data/ospf_text.txt",system_prompt_path="system_prompt/OSPF_recognize.txt")
    ospf_policys = str.get("result")
    for ospf_req_dic in ospf_policys:
        polished_str = polish_ospf(ospf_req_dic)
        if polished_str:
            polished_policys.append(polished_str)
    print("\n".join(polished_policys))
