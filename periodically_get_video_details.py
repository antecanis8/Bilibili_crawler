import get_reply_count
import get_video_aid
import get_video_details
import time
import schedule
import csv

all_counts = []
BV=''
with open('./counts.csv', mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['抓取时间', '播放量', '弹幕数', '评论数', '收藏数', '投币数', '分享数', '点赞数'])
    writer.writerows(all_counts)


def run_your_program():  
    view_count,danmaku_count,reply_count,favorite_count,coin_count,share_count,like_count=get_video_details.get_video_details(BV)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    all_counts.append([current_time,view_count,danmaku_count,reply_count,favorite_count,coin_count,share_count,like_count])
    with open('./counts.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(all_counts)
    all_counts.clear()


schedule.every(3).minutes.do(run_your_program)  
  
if __name__ == "__main__":  
    while True:  
        schedule.run_pending()  
        time.sleep(1)