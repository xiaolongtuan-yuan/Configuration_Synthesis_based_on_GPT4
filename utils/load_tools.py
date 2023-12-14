# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/30 10:09
@Auth ： xiaolongtuan
@File ：load_tools.py
"""
import json


def load_tools(tool_paths:[]):
    tools = []
    for path in tool_paths:
        with open(path,'r') as tool_f:
            tool_str = tool_f.read()
            tool = json.loads(tool_str)
            tools.append(tool)
    return tools