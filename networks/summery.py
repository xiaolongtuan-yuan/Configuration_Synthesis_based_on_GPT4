# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/15 16:17
@Auth ： xiaolongtuan
@File ：summery.py
"""
import os
def read_all_files_in_folder(network_root):
    # 初始化Markdown内容
    markdown_content = "已知网络中所有设备的配置文件如下:\n\n"

    # 遍历目标文件夹及其子文件夹
    for root, dirs, files in os.walk(network_root):
        for file_name in files:
            if "configs" in root or "hosts" in root:

                file_path = os.path.join(root, file_name)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                # 获取相对路径作为文件名
                relative_path = os.path.relpath(file_path, network_root)

                # 添加文件名和内容到Markdown内容
                markdown_content += f"## {relative_path}\n\n```\n{file_content}\n```\n\n"

    return markdown_content

def write_to_markdown(markdown_content, output_file):
    # 将Markdown内容写入文件
    with open(output_file, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)


def make_temp_summery(network_root, output_path):
    markdown_content = read_all_files_in_folder(network_root)
    write_to_markdown(markdown_content,output_path)
    return markdown_content


# 指定目标文件夹路径和输出Markdown文件路径
if __name__ == '__main__':
    target_folder = 'hard'
    output_markdown_file = 'hard_gen.md'

    # 读取所有文件并生成Markdown内容
    markdown_content = read_all_files_in_folder(target_folder)

    # 将Markdown内容写入文件
    write_to_markdown(markdown_content, output_markdown_file)