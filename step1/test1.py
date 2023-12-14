# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/15 11:11
@Auth ： xiaolongtuan
@File ：test1.py
"""
import time

from openai import OpenAI
from init import client


def create_file_with_timestamp(content):
  timestamp = int(time.time())
  timestamp_str = str(timestamp)
  filename = f"gpt_{timestamp_str}.txt"

  with open(filename, 'w') as file:
    file.write(content)

with open("/Users/zhangyuan/Desktop/学术/网络配置/network/test1/config/example.md",'r') as file:
    config = file.read()


require = """
请修改配置文件的内容，使得网络转发平面满足约束：
1.json. 从host1到达AS2必须经过AS2core1交换机
2. 从host2到达AS3不能经过AS2core1交换机
"""
completion = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "你被用于生成网络配置文件，根据用户的需求和对网络的描述，修改或生成满足需求的网络配置文件。"},
    {"role": "user", "content": config},
    {"role": "user", "content": require}
  ]
)

print(completion.choices[0].message.content)
create_file_with_timestamp(completion.choices[0].message.content)
