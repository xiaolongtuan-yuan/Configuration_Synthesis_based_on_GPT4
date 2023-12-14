# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/23 21:46
@Auth ： xiaolongtuan
@File ：user_interact.py
"""
def get_input():
    user_input_lines = []
    print("请输入文本，输入 ':q' 结束输入，输入'exit'结束问答:")
    while True:
        line = input()
        if line == ':q':
            break
        user_input_lines.append(line)

    user_input = '\n'.join(user_input_lines)
    return user_input
