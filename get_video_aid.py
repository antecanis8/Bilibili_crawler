import requests
import re
import json

with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        cookies_str = config['cookies_str']
        DedeUserID_regx = 'DedeUserID=(.*?);'
        DedeUserID = re.findall(DedeUserID_regx, cookies_str)[0]
        buvid3_regx = 'buvid3=(.*?);'
        buvid3 = re.findall(buvid3_regx, cookies_str)[0]
        sessdata_regx = 'SESSDATA=(.*?);'
        sessdata = re.findall(sessdata_regx, cookies_str)[0]
        bili_jct_regx = 'bili_jct=(.*?);'
        bili_jct = re.findall(bili_jct_regx, cookies_str)[0]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
cookies = {
    'DedeUserID': DedeUserID,
    'buvid3': buvid3,
    'SESSDATA':sessdata,
    'bili_jct':bili_jct
}

def get_video_aid(bv):
    url = f'https://www.bilibili.com/video/{bv}'
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    content = html.text
    aid_regx = '"aid":(.*?),"bvid":"{}"'.format(bv)
    video_aid = re.findall(aid_regx, content)[0]
    return video_aid

# print(get_video_aid('BV1YM411k7FE'))