# 识别配置文件中的语法错误，学习batfish的测试代码
import json
import os

import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *


def save_syntax_line(root_dir:str,filename: str, issue_lines: list, output_file: str):
    try:
        # 读取报错文件
        with open(os.path.join(root_dir, filename), 'r') as file:
            # 读取所有行
            lines = file.readlines()
            with open(output_file, 'a') as output:
                for line_number in issue_lines:
                    error_line = lines[line_number - 1].strip()
                    error_message = f"{filename}[{line_number}]:{error_line}\n"
                    output.write(error_message)
    except Exception as e:
        print(f"Error: {e}")
    return

def create_issue_file(file_path:str, issue_prompt:str):
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as file:
                file.write(issue_prompt+'\n')
                print(f"File '{file_path}' created successfully.")
        except Exception as e:
            print(f"Error: {e}")
    return

syntax_issue_output = "output/syntax_issues"
bf = Session(host="localhost")
CHANGE1_DIR = 'networks/forward_change/junos'
CHANGE1_NAME = 'junOs'
syntax_issue_output_file = os.path.join(syntax_issue_output, CHANGE1_NAME+".txt")
create_issue_file(syntax_issue_output_file,"There are some syntax error for the device:")

bf.init_snapshot(CHANGE1_DIR, name=CHANGE1_NAME, overwrite=True)
issues = bf.q.initIssues().answer(snapshot='junOs').frame()  # 检查快照问题
issues = issues[issues['Details'].apply(lambda x: "This syntax is unrecognized" in x)]['Source_Lines'].tolist()
for line in issues:
    line = line[0]
    filename = line.filename  # str
    lines = line.lines  # list
    save_syntax_line(CHANGE1_DIR, filename, lines, syntax_issue_output_file)


print('over')
