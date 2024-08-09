import requests
import re
import wbi
import json
url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail"

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

def get_dynamic(id):

    img_key, sub_key = wbi.getWbiKeys()
    signed_params = wbi.encWbi(
    params={
        'id': id
    },
    img_key=img_key,
    sub_key=sub_key
    )
    response = requests.request("GET", url, params=signed_params, headers=headers)
    content=response.text
    aid_regx = '"comment_id_str":"(.*?)"'
    dynamic_oid = re.findall(aid_regx, content)[0]
    aid_regx = '"comment_type":(.*?),'
    dynamic_type = re.findall(aid_regx, content)[0]
    return dynamic_oid,dynamic_type




# print(get_dynamic('963510844121940006'))
