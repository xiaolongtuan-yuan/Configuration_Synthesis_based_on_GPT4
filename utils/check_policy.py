# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/21 17:08
@Auth ： xiaolongtuan
@File ：check_policy.py
"""
from pybatfish.client.session import Session
import os
from pybatfish.datamodel import HeaderConstraints

base_path = "networks"
syntax_issue_output = "output/syntax_issues"
Success = ['ACCEPTED', 'DELIVERED_TO_SUBNEt', 'EXITS_NETWORK']


def init_session(network):
    bf = Session(host="localhost")
    CHANGE1_DIR = os.path.join(base_path, network)
    CHANGE1_NAME = network
    bf.init_snapshot(CHANGE1_DIR, name=CHANGE1_NAME, overwrite=True)
    return bf,CHANGE1_DIR

# 获得从r1到net1的转发流量, 筛选第一跳为r2的流量，若存在则为真
def check_fwd(network: str, r1: str, d1: str, r2: str):
    def filter(traces, r2):
        for trace in traces:
            if not trace.disposition in Success:
                continue
            else:
                if trace.hops[0].node == r2:
                    return True
        return False

    syntax_issue_output = "output/policy_issues"
    bf,_ = init_session(network)

    result = bf.q.traceroute(startLocation=f'@enter({r1})',
                             headers=HeaderConstraints(dstIps=d1)).answer().frame()
    result = result[result.apply(lambda trace: filter(trace['Traces'], r2), axis=1)]
    if result.size == 0:
        return False
    return True

# 获取所有以net为目的地的流量，筛选路径中同时存在r1和r2的流量，存在则为真
def check_reachable(network: str, r1: str, d1: str, r2: str):
    def filter(traces, r1, r2):
        for trace in traces:
            if not trace.disposition in Success:
                continue
            else:
                flag = 2
                for hop in trace.hops:
                    if hop.node in [r1, r2]:
                        flag -= 1
                if flag <= 0:
                    return True
        return False

    syntax_issue_output = "output/policy_issues"
    bf,_ = init_session(network)

    result = bf.q.traceroute(startLocation=f'@enter({r1})',
                             headers=HeaderConstraints(dstIps=d1)).answer().frame()
    result = result[result.apply(lambda trace: filter(trace['Traces'], r1, r2), axis=1)]
    if result.size == 0:
        return False
    return True

# 检查是否有流量能够从start到end
def check_connect(network:str, start, end):
    bf, _ = init_session(network)
    result = bf.q.traceroute(startLocation=f'@enter({start})',
                             headers=HeaderConstraints(dstIps=end)).answer().frame()
    if result.size > 0:
        return True
    else:
        return False

# 验证 !fwd(R1,N1,R2)&fwd(R1,N2,R2)，及连续经过r1，r2的流量不会同时流向n1和n2
def check_trafficIsolation(network, r1, r2, n1, n2):
    if not (check_fwd(network, r1, n1, r2) and check_reachable(network, r1, n2, r2)):
        return False
    return True

def check_syntax(network):
    def save_syntax_line(root_dir: str, filename: str, issue_lines: list, output_file: str,feedback):
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
                        feedback.append(error_message)
        except Exception as e:
            print(f"Error: {e}")
        return feedback

    def create_issue_file(file_path: str, issue_prompt: str):
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    file.write(issue_prompt + '\n')
                    print(f"File '{file_path}' created successfully.")
            except Exception as e:
                print(f"Error: {e}")
        return

    bf,CHANGE1_DIR = init_session(network)

    issues = bf.q.initIssues().answer(snapshot=network).frame()  # 检查快照问题
    feedback = []
    issues = issues[issues['Details'].apply(lambda x: "This syntax is unrecognized" in x)]['Source_Lines'].tolist()
    if len(issues) == 0:
        # 没有错误
        return True, ""

    syntax_issue_output_file = os.path.join(syntax_issue_output, network + ".txt")
    create_issue_file(syntax_issue_output_file, "There are some syntax error for the device:")
    for line in issues:
        line = line[0]
        filename = line.filename  # str
        lines = line.lines  # list
        save_syntax_line(CHANGE1_DIR, filename, lines, syntax_issue_output_file,feedback)
    return False, "配置文件存在语法错误:\n"+("\n".join(feedback))

if __name__ == "__main__":
    # networks = "forward_change_base"
    # r1 = "border1"
    # n1 = "spine1"
    # n2 = "spine2"
    # r2 = "core1"
    # # print(check_reachable(networks, r1, n1, r2))
    # print(check_trafficIsolation(networks, r1, n1, n2, r2))
    network = "simple_gen"
    check_syntax(network)
