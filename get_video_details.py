import requests
import re
import wbi
import json
import os
url = "https://api.bilibili.com/x/web-interface/view"

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


def get_video_details(bv):

    img_key, sub_key = wbi.getWbiKeys()
    signed_params = wbi.encWbi(
    params={
        'bvid': bv
    },
    img_key=img_key,
    sub_key=sub_key
    )
    response = requests.request("GET", url, params=signed_params, headers=headers)
    content=response.text
    # print(content)
    view_count_regx = '"view":(.*?),'
    view_count = re.findall(view_count_regx, content)[0]
    danmaku_count_regx = '"danmaku":(.*?),'
    danmaku_count = re.findall(danmaku_count_regx, content)[0]
    reply_count_regx = '"reply":(.*?),'
    reply_count = re.findall(reply_count_regx, content)[0]
    favorite_count_regx = '"favorite":(.*?),'
    favorite_count = re.findall(favorite_count_regx, content)[0]
    coin_count_regx = '"coin":(.*?),'
    coin_count = re.findall(coin_count_regx, content)[0]
    share_count_regx = '"share":(.*?),'
    share_count = re.findall(share_count_regx, content)[0]
    like_count_regx = '"like":(.*?),'
    like_count = re.findall(like_count_regx, content)[0]
    # print(view_count)
    # print(danmaku_count)
    # print(reply_count)
    # print(favorite_count)
    # print(coin_count)
    # print(share_count)
    # print(like_count)
    return view_count,danmaku_count,reply_count,favorite_count,coin_count,share_count,like_count




