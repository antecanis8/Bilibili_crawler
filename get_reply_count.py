import requests
import re
import wbi
import json
import os
url = "https://api.bilibili.com/x/v2/reply/count"

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


def get_reply_count(oid,type):

    img_key, sub_key = wbi.getWbiKeys()
    signed_params = wbi.encWbi(
    params={
        'oid': oid,
        'type': type
    },
    img_key=img_key,
    sub_key=sub_key
    )
    response = requests.request("GET", url, params=signed_params, headers=headers)
    content=response.text
    reply_count_regx = '{"count":(.*?)}'
    reply_count = re.findall(reply_count_regx, content)[0]
    return reply_count




