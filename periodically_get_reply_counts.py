import get_reply_count
import get_video_aid
import time
import schedule
import csv

all_counts = []
oid=get_video_aid.get_video_aid('')
type=1
with open('./counts.csv', mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['抓取时间', '评论数'])
    writer.writerows(all_counts)


def run_your_program():  
    count=get_reply_count.get_reply_count(oid,type)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    all_counts.append([count,current_time])
    with open('./counts.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(all_counts)
    all_counts.clear()


schedule.every(10).seconds.do(run_your_program)  
  
if __name__ == "__main__":  
    while True:  
        schedule.run_pending()  
        time.sleep(1)