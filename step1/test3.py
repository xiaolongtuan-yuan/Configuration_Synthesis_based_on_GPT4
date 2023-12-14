# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/15 11:11
@Auth ： xiaolongtuan
@File ：test1.py
"""
import getpass
import sys
import time
from collections import deque

from openai import OpenAI
from init import client

timestamp = int(time.time())
timestamp_str = str(timestamp)
filename = f"output/gpt_{timestamp_str}.txt"

with open(filename, 'w') as file:
    file.write("")


def write_file_with_content(role, content):
    with open(filename, "a") as file:
        file.write(f"{role}:\n{content}\n")

def get_input():
    user_input_lines = []
    print("请输入文本，输入 ':q' 结束:")
    while True:
        line = input()
        if line == ':q':
            break
        user_input_lines.append(line)

    user_input = '\n'.join(user_input_lines)
    return user_input


historys = deque(maxlen=8)
require = get_input()
while require:
    write_file_with_content("user", require)
    historys.append(
        {"role": "user", "content": require}
    )
    messages = []
    messages.append({"role": "system",
                     "content": "根据用户的需求和对网络的描述，生成满足需求的网络配置文件。必须给出完整的配置文件，不可以省略偷懒"})
    for history in historys:
        messages.append(history)
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    print(completion.choices[0].message.content)
    historys.append({
        "role": "assistant", "content": completion.choices[0].message.content
    })
    write_file_with_content("assistant", completion.choices[0].message.content)
    require = get_input()