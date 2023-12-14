# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/23 21:21
@Auth ： xiaolongtuan
@File ：GPT4_agent.py
"""
from openai import OpenAI
import json
from utils.config_retrieval import *
from utils.user_interact import get_input
from init import client
from utils.load_tools import load_tools
from utils.text_process import load_require, load_summery
from utils.image_process import load_image
from utils.load_policy import recognize_policy, check_module, check_syntax, read_policy_file
from networks.summery import make_temp_summery
import re


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


def run_conversation_gen(model: str, require_path: str, network_root: str, tools: [], device_list: [], human_in=True):
    require = load_require(require_path)
    system = load_require("../networks/gen_system.txt")
    tools = load_tools(tools)
    messages = []
    messages.append({"role": "system",
                     "content": system}),
    messages.append({"role": "user",
                     "content": require})
    device_index = 0
    while True:
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
            "role":"user",
            "content":policy_str
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
    print(run_conversation_gen(model="gpt-4-1106-preview",
                               require_path="../networks/topologic/4.txt",
                               network_root="simple_gen",
                               tools=["utils/toolsjson/config_update.json"],
                               device_list=["leaf1", "spine1", "spine2", "core1", "core2", "border1", "border2"]))

    # 修改配置文件
    print(run_conversation_change(model="gpt-4-1106-preview",
                                  require_path="../utils/test/policy_test1.txt",
                                  network_root="simple_gen",
                                  tools=["utils/toolsjson/config_update.json"]))
