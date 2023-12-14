# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/4 13:21
@Auth ： xiaolongtuan
@File ：load_policy.py
"""
import json

'''
读取加载自然语言表述的高级约束
'''


def read_policy_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            file_str = file.read()
            # print(f"原始需求{file_str}")
            return file_str
    except Exception as e:
        print(f"read policy file error:{e}")


def recognize_policy(client, policy_str: str, system_prompt_path:str) -> str:
    messages = []
    with open(system_prompt_path, 'r') as system_file:
        system_prompt = system_file.read()
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    messages.append({
        "role": "user",
        "content": policy_str
    })
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=messages,
        stream=False
    )
    response_message = response.choices[0].message
    content = response_message.content
    print(content)
    policy_dic = json.loads(content)
    return policy_dic


from utils.check_policy import *


def check_module(network: str, policy_dic):
    check_res = []
    check_syntax(network=network)
    available_functions = {
        "check_fwd": {
            "func": check_fwd,
            "des": "流量从设备{r1}转发到目的地设备{d1}，其下一跳设备是{r2}"
        },
        "check_connect": {
            "func": check_connect,
            "des": "从{start}设备的流量能够到达{end}设备"
        },
        "check_reachable": {
            "func": check_reachable,
            "des": "流量从设备{r1}到目的地设备{d1}，途径{r2}设备"
        }
    }
    flag = True
    for item in policy_dic['result']:
        policy = item['policy']
        parameter = item['parameter']
        b = item['bool']
        check_func = available_functions[policy]['func']
        des_format = available_functions[policy]['des']
        bool_str = "为真" if b else "为假"
        if check_func(network=network,**parameter) == b:
            check_res.append("当前配置已满足约束：" + des_format.format(**parameter) + bool_str)
        else:
            flag = False
            check_res.append("当前配置未满足约束：" + des_format.format(**parameter) + bool_str)
    return flag,"\n".join(check_res)
