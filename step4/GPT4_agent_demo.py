# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/23 21:21
@Auth ： xiaolongtuan
@File ：GPT4_agent.py
"""
from openai import OpenAI
import json

from step4.pojo.NetworkDes import json_2_NetworkDes
from step4.polish_require import polish_bgp, polish_ospf
from utils.config_retrieval import *
from utils.user_interact import get_input
from init import client
from utils.load_tools import load_tools
from utils.text_process import load_require, load_summery
from utils.image_process import load_image
from utils.load_policy import recognize_policy, check_module, check_syntax, read_policy_file
from networks.summery import make_temp_summery
import re

# 未配置验证器

system_gen_prompt_path = "step4/system_prompt/gen_system.txt"
require_templete_path = "step4/system_prompt/require_templete.txt"
high_require_templete_path = "step4/system_prompt/high_require_templete.txt"
BGP_recog_system_path = "step4/system_prompt/BGP_recognize.txt"
OSPF_recog_system_path = "step4/system_prompt/OSPF_recognize.txt"


def extract_and_parse_json(input_string):
    pattern = r'\{.*?\}'
    matches = re.findall(pattern, input_string, re.DOTALL)

    result = []
    for match in matches:
        try:
            json_data = json.loads(match)
            result.append(json_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return result


def get_polished_str(high_require_prompt):
    polished_policys = []
    str = recognize_policy(client=client, policy_str=high_require_prompt,
                           system_prompt_path=BGP_recog_system_path)
    bgp_policys = str.get("result")
    for bgp_req_dic in bgp_policys:
        polished_str = polish_bgp(bgp_req_dic)
        if polished_str:
            polished_policys.append(polished_str)
    str = recognize_policy(client=client, policy_str=high_require_prompt,
                           system_prompt_path=OSPF_recog_system_path)
    ospf_policys = str.get("result")
    for ospf_req_dic in ospf_policys:
        polished_str = polish_ospf(ospf_req_dic)
        if polished_str:
            polished_policys.append(polished_str)
    polished_str = "\n".join(polished_policys)
    return polished_str


def gpt_service(model: str, messages, tools, network_root):  # gpt调用工具并更新
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=False
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:

        available_functions = {
            "config_update": config_update,
            "config_retrieval": config_retrieval
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            try:
                function_args = json.loads(tool_call.function.arguments)
                function_args['network_root'] = network_root
            except json.decoder.JSONDecodeError as e:
                print(f"JSON decoding error: {e}:{tool_call.function.arguments}")
                raise Exception("解析json参数错误")
            print(f"调用函数{function_name}({function_args})")
            function_response = function_to_call(**function_args)
            print(f"执行结果：{function_response}")
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
    else:
        print(f"GPT:{response_message.content}")
        messages.append({
            "role": "assistant",
            "content": response_message.content
        })
        results = extract_and_parse_json(response_message.content)
        for result in results:
            file = result['file']
            config = result['config']
            function_response = config_update(network_root=network_root, file=file, config=config)
            messages.append(
                {
                    "role": "user",
                    "content": function_response,
                }
            )
    return


def make_require_without_configsummury(net_des, temp_path, network_root):
    '''
    :param net_des: 网络描述对象，包含了高级需求
    :param temp_path: 存储require_without_configsummury的临时路径，便于用户查看
    :param network_root: 网络配置文件夹目录
    :return:
    '''
    device_types = net_des.get_all_type_of_devices()
    device_types_str = ""  # 1
    for key in list(device_types.keys()):
        type_str = ",".join(device_types.get(key))
        device_types_str += (key + ": " + type_str + "\n")

    AS_list_str = ",".join(list(net_des.AS.keys()))  # 2
    AS_acount_str = str(net_des.AS_count)  # 3
    AS_and_device_str = ""  # 4
    for AS in list(net_des.AS.values()):
        AS_devices = list(AS.devices.keys())
        AS_and_device_str_i = AS.AS_name + "包含设备:" + ",".join(AS_devices) + "\n"
        AS_and_device_str += AS_and_device_str_i

    edges_str = ",".join(["[" + edge[0] + "," + edge[1] + "]"
                          for edge in net_des.edge_list])  # 5

    high_require = net_des.high_require
    with (open(high_require_templete_path, 'r') as high_require_templete_file):
        high_require_templete = high_require_templete_file.read()
        high_require_prompt = high_require_templete.format(device_types_str, AS_list_str, AS_acount_str,
                                                                       AS_and_device_str, edges_str, high_require)
    polished_policys = get_polished_str(high_require_prompt)

    with open(require_templete_path, 'r') as require_templete_file:
        require_templete = require_templete_file.read()
        require_without_configsummury = require_templete.format(device_types_str, AS_list_str, AS_acount_str,
                                                                AS_and_device_str, edges_str, polished_policys, "{}")
        with open(temp_path, 'w') as write_file:
            write_file.write(require_without_configsummury)

        return require_without_configsummury


def update_require_str(require_without_configsummury, network_root):
    # 生成summery
    config_summery = make_temp_summery(network_root, os.path.join(network_root, "temp_summery.txt"))
    require = require_without_configsummury.format(config_summery)
    return require


def run_conversation_gen(model: str, require_temp_path: str, network_root: str, tools: [], net_dec_json_path: str,
                         human_in=True):
    '''
    :param model: GPT使用模型
    :param require_temp_path: 存储require临时路径
    :param network_root: 网络配置文件夹路径
    :param tools: 工具集
    :param net_dec_json_path: 网络描述文件路径
    :param human_in: 是否人工参与交互
    :return:
    '''
    network = json_2_NetworkDes(net_dec_json_path)  # 网络描述对象
    device_list = network.get_all_device()

    require_without_configsummury = make_require_without_configsummury(network, require_temp_path,
                                                                       network_root)  # require_without_configsummury用于更新summery
    system = load_require(system_gen_prompt_path)
    tools = load_tools(tools)

    device_index = 0
    while True:
        messages = []
        messages.append({"role": "system",
                         "content": system}),
        require = update_require_str(require_without_configsummury, network_root)
        messages.append({"role": "user",
                         "content": require})

        if device_index < len(device_list):
            device = device_list[device_index]
            device_index += 1
            messages.append({
                "role": "user",
                "content": f"生成设备{device}的配置文件"
            })
        else:
            break

        gpt_service(model=model, messages=messages, tools=tools, network_root=network_root)
        if human_in:
            user_input = get_input()
            if user_input == "exit":
                break
            messages.append({
                "role": "user", "content": user_input
            })
    return "已生成全部配置文件"


def run_conversation_change(model: str, require_path: str, network_root: str, tools: [], human_in=True):
    tools = load_tools(tools)
    system = load_require("../networks/change_system.txt")
    policy_str = read_policy_file(require_path)
    print(f"原始需求:\n{policy_str}")
    policy_dic = recognize_policy(client=client, file_path=require_path)
    syntax_flag, syntax_feedback = check_syntax(network=network_root)
    while not syntax_flag:
        print(f"配置语法不合格：\n{syntax_feedback}")
        if human_in:
            user_input = get_input()
            if user_input == "exit":
                break
        messages = []
        messages.append({
            "role": "system",
            "content": system
        }),
        messages.append({
            "role": "user",
            "content": policy_str
        })
        summert_path = make_temp_summery(network=network_root)
        summery = load_summery(summert_path)
        messages.append({
            "role": "user",
            "content": summery
        })
        messages.append({
            "role": "user",
            "content": syntax_feedback
        })
        if human_in:
            messages.append({
                "role": "user",
                "content": user_input
            })
        gpt_service(model=model, messages=messages, tools=tools, network_root=network_root)

        syntax_flag, syntax_feedback = check_syntax(network=network_root)

    flag, feedback = check_module(network=network_root, policy_dic=policy_dic)
    while not flag:
        print(f"策略未全部满足:\n{feedback}")
        if human_in:
            user_input = get_input()
            if user_input == "exit":
                break
        messages = []
        messages.append({
            "role": "system",
            "content": system
        }),
        summert_path = make_temp_summery(network=network_root)
        summery = load_summery(summert_path)
        messages.append({
            "role": "user",
            "content": summery
        })
        messages.append({
            "role": "user",
            "content": feedback
        })
        if human_in:
            messages.append({
                "role": "user",
                "content": user_input
            })
        gpt_service(model=model, messages=messages, tools=tools, network_root=network_root)
        flag, feedback = check_module(network=network_root, policy_dic=policy_dic)
    return "当前配置已满足全部策略需求"


if __name__ == '__main__':
    # 先生成完整配置文件
    print(
        run_conversation_gen(model="gpt-4-1106-preview", require_temp_path="step4/network_config/network_1/require.txt",
                             network_root="step4/network_config/network_1",
                             tools=["utils/toolsjson/config_update.json"],
                             net_dec_json_path='step4/network_config/network_1/network_1.json',
                             human_in=True)
        )

    # # 修改配置文件
    # print(run_conversation_change(model="gpt-4-1106-preview",
    #                               require_path="../utils/test/policy_test1.txt",
    #                               network_root="simple_gen",
    #                               tools=["utils/toolsjson/config_update.json"]))
