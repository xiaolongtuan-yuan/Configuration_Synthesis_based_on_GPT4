# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/21 11:21
@Auth ： xiaolongtuan
@File ：config_retrieval.py
"""
import os.path

base_path = "networks"


# 检索配置文件
def config_retrieval(file: str, network_root: str, line_number=None):
    file_path = os.path.join(network_root, file)
    try:
        with open(file_path, "r") as f:
            if line_number == None:
                config = f.read()
                return config
            else:
                lines = f.readlines()
                config_line = lines[line_number - 1].strip()
                return config_line
    except Exception as e:
        print(f"Error: {e}")
        return ""


def config_update(network_root: str, file: str, config: str):
    file_path = os.path.join(network_root, file)
    try:
        with open(file_path, "w") as f:
            f.write(config)
            print(f"更新设备{file}配置成功")
            return f"更新设备{file}配置成功"
    except Exception as e:
        print(f"Error: {e}")
        return ""


if __name__ == "__main__":
    print(config_retrieval(file="core1"), network="configs/forward_change_junos")
