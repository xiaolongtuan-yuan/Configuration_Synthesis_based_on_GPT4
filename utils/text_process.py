# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/30 10:16
@Auth ： xiaolongtuan
@File ：text_process.py
"""


def load_require(require_path):
    with open(require_path, 'r') as f:
        require = f.read()
        return require


def load_summery(summery_path):
    with open(summery_path, 'r') as f:
        summery = f.read()
        return summery
