# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/12 20:53
@Auth ： xiaolongtuan
@File ：polish_require.py
"""
from utils.load_policy import recognize_policy

# 润色BGP拆解的需求
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
1. check_waypoint(start,end,waypoint)：流量从start节点转发到end节点，流量在网络中会经过waypoint节点
2. check_reachable(start,end)：从start节点的流量能够到达end节点
3. check_avoidance(start,end,avoidance): 流量从start节点转发到end节点，流量需要避开avoidance节点
'''
bgp_policy_templete = {
    "check_waypoint": {
        "true": {
            "0": "使用BGP协议保证流量能直接从{}转发到{}，流量不经过其他AS",
            "1": "使用BGP协议保证流量从{}转发到{}，流量在网络中会依次经过{}"
        },
        "false": ""  # 没有假谓词
    },
    "check_reachable": {
        "true": "使用BGP协议保证流量能够从{}到达{}",
        "false": "使用BGP协议保证流量不能从{}到达{}"
    },
    "check_avoidance": {
        "true": "使用BGP协议保证流量从{}到达{}的路径中需要避开{}",
        "false": ""  # 没有假谓词
    }
}


def polish_bgp(bgp_req_dic):  # 测试通过
    policy = bgp_req_dic.get("policy")
    parameter = bgp_req_dic.get('parameter')
    start = parameter.get("start")
    end = parameter.get("end")
    is_true = bgp_req_dic.get("bool")

    if policy == "check_waypoint":
        waypoint = parameter.get("waypoint")
        if is_true:
            if len(waypoint) == 0:
                policy_str = bgp_policy_templete.get("check_waypoint").get("true").get('0').format(start, end)
            else:
                waypoint_str = "、".join(waypoint)
                policy_str = bgp_policy_templete.get("check_waypoint").get("true").get('1').format(start, end,
                                                                                                   waypoint_str)
        else:
            raise Exception("GPT解析错误，不存在为假的check_waypoint谓词")
    if policy == "check_reachable":
        if is_true:
            policy_str = bgp_policy_templete.get("check_reachable").get("true").format(start, end)
        else:
            policy_str = bgp_policy_templete.get("check_reachable").get("false").format(start, end)
    if policy == "check_avoidance":
        avoidance = parameter.get("avoidance")
        if is_true:
            policy_str = bgp_policy_templete.get("check_avoidance").get("true").format(start, end, avoidance)
        else:
            raise Exception("GPT解析错误，不存在为假的check_avoidance谓词")

    return policy_str


'''
1. check_waypoint(start,end,waypoint)：流量从start节点转发到end节点，流量在网络中需要依次经过waypoint节点列表
2. check_reachable(start,end)：从start节点的流量能够到达end节点
3. check_avoidance(start,end,avoidance): 流量从start节点转发到end节点，流量需要避开avoidance节点
static_route(start,end, waypoint): 从start出发以end节点作为终点的流量包，按照静态路由依次经过waypoint_list列表中的节点
'''
ospf_policy_templete = {
    "check_waypoint": {
        "true": {
            "0": "在{}内部使用OSPF协议保证流量直接从{}转发到{}，流量在不经过其他设备",
            "1": "在{}内部使用OSPF协议保证流量从{}转发到{}，流量在网络中会依次经过{}",
        },
        "false": ""  # 没有假谓词
    },
    "check_reachable": {
        "true": "在{}内部使用OSPF协议保证流量能够在{}与{}间转发",
        "false": "在{}内部使用OSPF协议保证{}与{}间没有流量转发"
    },
    "check_avoidance": {
        "true": "在{}内部使用OSPF协议保证流量从{}到达{}的路径中需要避开{}",
        "false": ""  # 没有假谓词
    },
    "static_route": {
        "true": "在{}内部使用静态路由保证从{}出发以{}作为终点的流量包，按照静态路由依次经过{}中的节点",
        "false": ""
    }
}


def polish_ospf(ospf_req_dic):
    policy = ospf_req_dic.get("policy")
    AS_name = ospf_req_dic.get("AS_name")
    parameter = ospf_req_dic.get('parameter')
    start = parameter.get("start")
    end = parameter.get("end")
    is_true = ospf_req_dic.get("bool")
    type = ospf_req_dic.get('type')

    if type.lower() == 'ospf':
        if policy == "check_waypoint":
            waypoint = parameter.get("waypoint")
            if is_true:
                if len(waypoint) == 0:
                    policy_str = ospf_policy_templete.get("check_waypoint").get("true").get('0').format(AS_name, start,
                                                                                                        end)
                else:
                    waypoint_str = "、".join(waypoint)
                    policy_str = ospf_policy_templete.get("check_waypoint").get("true").get('1').format(AS_name, start,
                                                                                                        end,
                                                                                                        waypoint_str)
            else:
                raise Exception("GPT解析错误，不存在为假的check_waypoint谓词")
        if policy == "check_reachable":
            if is_true:
                policy_str = ospf_policy_templete.get("check_reachable").get("true").format(AS_name, start, end)
            else:
                policy_str = ospf_policy_templete.get("check_reachable").get("false").format(AS_name, start, end)
        if policy == "check_avoidance":
            avoidance = parameter.get("avoidance")
            if is_true:
                policy_str = ospf_policy_templete.get("check_avoidance").get("true").format(AS_name, start, end,
                                                                                            avoidance)
            else:
                raise Exception("GPT解析错误，不存在为假的check_avoidance谓词")
    elif type.lower() == 'static':
        if policy == "static_route":
            waypoint = parameter.get("waypoint")
            waypoint_str = "、".join(waypoint)
            if is_true:
                policy_str = ospf_policy_templete.get("static_route").get("true").format(AS_name, start, end,
                                                                                         waypoint_str)
            else:
                raise Exception("GPT解析错误，不存在为假的static_route谓词")
        else:
            raise Exception("GPT解析静态路由需求错误")
    else:
        return
    return policy_str

