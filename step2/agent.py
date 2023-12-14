# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/22 11:30
@Auth ： xiaolongtuan
@File ：agent.py
"""
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from utils.config_retrieval import config_retrieval

config_list = config_list_from_json(
    env_or_file="../OAI_CONFIG_LIST.json",
    filter_dict={
        "model": {
            "gpt-4"
        }
    }
)
functions = [
    {
        "name": "config_retrieval",
        "description": "Retrieve the code in the target device's configuration file and call this function when you need to check and modify the configuration file of an existing device",
        # "检索目标设备的配置文件中的代码，当你需要检查并修改已有设备的配置文件时可以调用该函数",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The device name of the target retrieval device, such as 'as1border1'"
                    # "目标检索设备的设备名，例如'as1border1'",
                },
                "line_number": {
                    "type": "integer",
                    "description": "Line number. If you need to retrieve only one line of the configuration file, carry this parameter. The function will return only the code for that line"
                    # "行号，如果只需要检索配置文件的某一行，请携带该参数，函数将只返回该行代码",
                }
            },
            "required": ["file"]
        },
    }
]
# network:str, file:str, line_number=None
llm_config = {
    "functions": functions,
    "config_list": config_list,
    "timeout": 120,
}

assistant = AssistantAgent(
    name="network_engineer",
    system_message="Network configuration engineers generate network configuration files based on user requirements and modify the configuration files based on verification feedback",
    # "网络配置工程师，根据用户需求生成网络配置文件，并根据验证反馈修改配置文件",
    llm_config=llm_config)
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=20,
    function_map={
        "config_retrieval": config_retrieval
    })

with open("../networks/forward_change_base.md", 'r') as file:
    message = file.read()
user_proxy.initiate_chat(assistant, message=message)
