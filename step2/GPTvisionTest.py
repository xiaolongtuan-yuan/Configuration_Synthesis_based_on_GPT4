# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/28 15:22
@Auth ： xiaolongtuan
@File ：GPTvisionTest.py
"""
import json

from init import OPENAI_API_KEY
import base64
import requests


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "../networks/topologic/differential-forwarding-network.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPENAI_API_KEY}"
}
with open("../networks/topologic/3.txt", 'r') as f:
  require = f.read()
  print(require)
payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": require
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
content = json.loads(response.content.decode('utf-8'))
print(content['choices'][0]['message']['content'])