# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/30 10:14
@Auth ： xiaolongtuan
@File ：image_process.py
"""
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        try:
            return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"read and encode {image_path} error: {e}")

def load_image(image_path):
    base64_image = encode_image(image_path)
    return base64_image
