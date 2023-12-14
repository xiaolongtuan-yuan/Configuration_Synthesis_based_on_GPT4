# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/12 19:46
@Auth ： xiaolongtuan
@File ：expand_bgp_req.py
"""

def expand(network_des, req): # 用于将只用AS号表示的参数替换为边界路由器，进行路由平面的检测
    '''
    {
      "policy": "check_reachable",
      "parameter": {
        "start": "AS2",
        "end": "AS3"
      },
      "bool": false,
      "type": "BGP"
    }
    '''
    if not req['type'].lower() not in ["bgp","static"]:
        return
    parameter = req['parameter']
    for key in parameter.keys():
        value = parameter.get(key)
        if value in network_des.AS.keys():
            borders = network_des.get_border_advice_of_AS(value)






