import get_reply_count
import get_dynamic_oid
import get_video_details
import get_dynamic_like_counts
import time
import schedule
import csv

all_counts = []
BV='1029575818492248073'
with open('./counts1029575818492248073.csv', mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['抓取时间', '评论数', '点赞数'])
    writer.writerows(all_counts)


oid,type=get_dynamic_oid.get_dynamic(BV)


def run_your_program():
    likes_count=get_dynamic_like_counts.get_dynamic_like_count(BV)
    reply_count=get_reply_count.get_reply_count(oid,type)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(current_time,reply_count,likes_count)
    all_counts.append([current_time,reply_count,likes_count])
    with open('./counts1029575818492248073.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(all_counts)
    all_counts.clear()


schedule.every(3).minutes.do(run_your_program)  
  
if __name__ == "__main__":  
    while True:  
        schedule.run_pending()  
        time.sleep(1)