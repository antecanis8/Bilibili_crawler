from requests.packages.urllib3.util.retry import Retry
import time
import math
import sys
import requests
import csv
import json
import pytz
import datetime
from fake_useragent import UserAgent
import random
import get_video_aid
import get_dynamic_oid
import get_reply_count
import re
import wbi
from tqdm import tqdm
with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        # oid = config['oid']
        # type = config['type']
        cookies_str = config['cookies_str']
        sessdata_regx = 'SESSDATA=(.*?);'
        sessdata = re.findall(sessdata_regx, cookies_str)[0]
        bili_jct_regx = 'bili_jct=(.*?);'
        bili_jct = re.findall(bili_jct_regx, cookies_str)[0]
        ps = config['ps']
        file_path_1 = config['output_path']+"/"+config['BV']+"_1.csv"
        file_path_2 = config['output_path']+"/"+config['BV']+"_2.csv"
        file_path_3 = config['output_path']+"/"+config['BV']+"_all.csv"
        BV = config['BV']
        if(BV.startswith('BV')):
            oid = get_video_aid.get_video_aid(BV)
            type = 1
        else:
            oid,type=get_dynamic_oid.get_dynamic(BV)
        down = 1
        up=int(int(get_reply_count.get_reply_count(oid,type))/20)

# 重试次数限制
MAX_RETRIES = 5
# 重试间隔（秒）
RETRY_INTERVAL = 10
beijing_tz = pytz.timezone('Asia/Shanghai')#时间戳转换为北京时间
ua=UserAgent()#创立随机请求头
one_comments = []
all_comments = []#构造数据放在一起的容器  总共评论
all_2_comments = []#构造数据放在一起的容器 二级评论
comments_current = []
comments_current_2 = []
img_key, sub_key = wbi.getWbiKeys()

        # 将所有评论数据写入CSV文件
with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','二级评论条数','等级','uid','rpid',"BV","抓取时间"])
    writer.writerows(all_comments)
with open(file_path_2, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','二级评论条数,条数相同说明在同一个人下面','等级','uid','rpid',"BV","抓取时间"])
    writer.writerows(all_2_comments)
with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地', '二级评论条数', '等级', 'uid', 'rpid',"BV","抓取时间"])
    writer.writerows(all_comments)

with requests.Session() as session:
    retries = Retry(total=3,  # 最大重试次数，好像没有这个函数
                    backoff_factor=0.1,  # 间隔时间会乘以这个数
                    status_forcelist=[500, 502, 503, 504])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': cookies_str,
        'SESSDATA': sessdata,
        'csrf': bili_jct,
    }
    url_long = 'https://api.bilibili.com/x/v2/reply/main'
    url_reply = 'https://api.bilibili.com/x/v2/reply/reply'
    data = {
        'next': str(0),
        'type': type,
        'oid': oid,
        'mode': '2'
    }
    signed_data = wbi.encWbi(
    data,
    img_key=img_key,
    sub_key=sub_key
    )
    response = session.get(url_long, params=signed_data, headers=headers)
    if response.status_code == 200:
        if response.status_code == 200:
            json_data = response.json()
            if 'data' in json_data:
                if 'top_replies' in json_data['data'] and json_data['data']['top_replies'] not in (None, []):
                    top_replies = json_data['data']['top_replies']
                    print(f"本次爬取含有置顶评论")
                    print(response.url)
                    for reply in top_replies:
                        name = reply['member']['uname']
                        sex = reply['member']['sex']
                        ctime = reply['ctime']
                        dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        like = reply['like']
                        message = reply['content']['message']
                        location = reply['reply_control'].get('location', '未知')
                        location = location.replace('IP属地：', '') if location else location
                        current_level = reply['member']['level_info']['current_level']
                        mid = str(reply['member']['mid'])
                        rpid = str(reply['rpid'])
                        count = reply['rcount']
                        all_comments.append([name, sex, formatted_time, like, message, location,count,current_level,mid,rpid,BV,current_time])
                        with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
                            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                            writer.writerows(all_comments)
                        with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                            writer.writerows(all_comments)
                        all_comments.clear()
                        if count != 0:
                            print(f"在置顶评论中, 该条回复下面总共含有{count}个二级评论")
                            total_pages = math.ceil(float(count) / float(ps)) if count > 0 else 0
                            for page_pn in range(1, total_pages + 1):
                                data_2 = {
                                    'type': type,
                                    'oid': oid,
                                    'ps': ps,
                                    'pn': str(page_pn),
                                    'root': rpid
                                }
                                response = session.get(url_reply, params=data_2, headers=headers)
                                if response.status_code == 200:
                                    print(f"请求置顶评论状态码：200")
                                    json_data = response.json()
                                    if 'data' in json_data and 'replies' in json_data['data']:
                                        print(response.url)
                                        if not json_data['data']['replies']:
                                            print(f"该页replies为空，没有评论")
                                            continue
                                        for comment in json_data['data']['replies']:
                                            rpid = str(comment['rpid'])
                                            name = comment['member']['uname']
                                            sex = comment['member']['sex']
                                            ctime = comment['ctime']
                                            dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                                            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                            like = comment['like']
                                            message = comment['content']['message']
                                            location = comment['reply_control'].get('location', '未知')
                                            location = location.replace('IP属地：', '') if location else location
                                            current_level = comment['member']['level_info']['current_level']
                                            mid = str(comment['member']['mid'])
                                            all_2_comments.append([name, sex, formatted_time, like, message, location, count,current_level,mid,rpid,BV,current_time])
                                            with open(file_path_2, mode='a', newline='', encoding='utf-8-sig') as file:
                                                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                                writer.writerows(all_2_comments)
                                            with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                                                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                                writer.writerows(all_2_comments)
                                            all_2_comments.clear()
                                    else:
                                        print(f"不含有内容")
                                else:
                                    print(f"请求错误")
                else:
                    print("该视频/动态不含有置顶评论")
    pagination_str=''
    for page in tqdm(range(down, up + 1)):
        for retry in range(MAX_RETRIES):
            try:
                data = {
                    'type': type,
                    'oid': oid,
                    'ps': ps,
                    'mode': '2',
                    'pagination_str':pagination_str

                }
                signed_data = wbi.encWbi(
                    data,
                    img_key=img_key,
                    sub_key=sub_key
                )
                response = session.get(url_long, params=signed_data, headers=headers)
                if response.status_code == 200:
                    json_data = response.json()
                    if 'data' in json_data:
                        if 'replies' in json_data['data'] and json_data['data']['replies']:
                            print(response.url)
                            first_level_comment=json_data
                            for comment in json_data['data']['replies']:
                                count = comment['rcount']
                                rpid = str(comment['rpid'])
                                name = comment['member']['uname']
                                sex = comment['member']['sex']
                                ctime = comment['ctime']
                                dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                like = comment['like']
                                message = comment['content']['message']
                                location = comment['reply_control'].get('location', '未知')
                                location = location.replace('IP属地：', '') if location else location
                                current_level = comment['member']['level_info']['current_level']
                                mid = str(comment['member']['mid'])
                                all_comments.append([name, sex, formatted_time, like, message, location,count,current_level,mid,rpid,BV,current_time])

                                with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
                                    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                    writer.writerows(all_comments)
                                with open(file_path_3, mode='a', newline='', encoding='utf-8-sig') as file:
                                    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                    writer.writerows(all_comments)
                                all_comments.clear()
                                if count != 0:
                                    print(f"在第{page}页中第{rpid}含有二级评论, 该条回复下面总共含有{count}个二级评论")
                                    total_pages = math.ceil(float(count) / float(ps)) if count > 0 else 0
                                    for page_pn in range(1, total_pages + 1):
                                        data_2 = {
                                            'type': type,
                                            'oid': oid,
                                            'ps': ps,
                                            'pn': str(page_pn),
                                            'root': rpid
                                        }
                                        if page_pn == 0:
                                            continue
                                        response = session.get(url_reply, params=data_2, headers=headers)
                                        if response.status_code == 200:
                                            json_data = response.json()
                                            print(response.url)
                                            if 'data' in json_data and 'replies' in json_data['data']:
                                                if not json_data['data']['replies']:
                                                    print(f"该页replies为空，没有评论")
                                                    continue
                                                for comment in json_data['data']['replies']:
                                                    rpid = str(comment['rpid'])
                                                    name = comment['member']['uname']
                                                    sex = comment['member']['sex']
                                                    ctime = comment['ctime']
                                                    dt_object = datetime.datetime.fromtimestamp(ctime,datetime.timezone.utc)
                                                    formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                                                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                                    like = comment['like']
                                                    message = comment['content']['message']
                                                    location = comment['reply_control'].get('location', '未知')
                                                    location = location.replace('IP属地：', '') if location else location
                                                    current_level = comment['member']['level_info']['current_level']
                                                    mid = str(comment['member']['mid'])
                                                    all_2_comments.append([name, sex, formatted_time, like, message, location, count,current_level,mid,rpid,BV,current_time])
                                                    with open(file_path_2, mode='a', newline='',encoding='utf-8-sig') as file:
                                                        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                                        writer.writerows(all_2_comments)
                                                    with open(file_path_3, mode='a', newline='',encoding='utf-8-sig') as file:
                                                        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
                                                        writer.writerows(all_2_comments)
                                                    all_2_comments.clear()
                                        else:
                                            print(f"获取第{page_pn + 1}页失败。状态码: {response.status_code}")
                                    time.sleep(random.uniform(0.2, 0.3))
                            print(f"已经成功爬取第{page}页。")
                            if "next_offset" in first_level_comment["data"]["cursor"]["pagination_reply"] and first_level_comment["data"]["cursor"]["pagination_reply"]["next_offset"]:
                                next_offset = first_level_comment["data"]["cursor"]["pagination_reply"]["next_offset"]
                                pagination_str = '{"offset":"' + next_offset.replace('"', '\\"') + '"}'
                            else:
                                print(f"在页面 {page} 的JSON响应中缺少 'next_offset' 键。跳过此页。")
                                sys.exit()
                        else:

                            print(f"在页面 {page} 的JSON响应中缺少 'replies' 键。跳过此页。")
                            sys.exit()
                    else:
                        print(f"在页面 {page} 的JSON响应中缺少 'data' 键。跳过此页。")
                else:
                    print(f"获取页面 {page} 失败。状态码: {response.status_code}")

                time.sleep(random.uniform(0.2, 0.3))
                break
            except requests.exceptions.RequestException as e:
                print(f"连接失败: {e}")
                if retry < MAX_RETRIES - 1:
                    print(f"正在重试（剩余尝试次数：{MAX_RETRIES - retry - 1}）...")
                    time.sleep(RETRY_INTERVAL)
                else:
                    raise



