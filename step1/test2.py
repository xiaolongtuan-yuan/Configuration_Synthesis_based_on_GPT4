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
  filename = f"output/gpt_{timestamp_str}.txt"

  with open(filename, 'w') as file:
    file.write(content)

with open("../networks/forward_change_base.md", 'r') as file:
    config = file.read()


require = """
以上是现有网络中所有设备的配置文件，请修改配置文件的内容，使得网络流量不经过core1，同时不改变网络端到端的连通性
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
