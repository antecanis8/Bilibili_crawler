import requests
import re
import wbi
import json
import os
url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail/reaction"
with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        cookies_str = config['cookies_str']
        sessdata_regx = 'SESSDATA=(.*?);'
        sessdata = re.findall(sessdata_regx, cookies_str)[0]
        bili_jct_regx = 'bili_jct=(.*?);'
        bili_jct = re.findall(bili_jct_regx, cookies_str)[0]


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Cookie':cookies_str,
    'SESSDATA':sessdata,
    'csrf':bili_jct
    }


def get_dynamic_like_count(BV):
    params={
        'id': BV
    }
    response = requests.request("GET", url, params=params, headers=headers)
    json_content = json.loads(response.text)
    like_count = json_content['data']['total']
    return like_count





