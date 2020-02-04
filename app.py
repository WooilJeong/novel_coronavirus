import schedule
import time
import os

def job():
    try:
        os.system('python update_dataset.py')
    except:
        os.system('python3 update_dataset.py')

# 5초에 한번씩 실행
# schedule.every(5).seconds.do(job)
# # 10분에 한번씩 실행
schedule.every(3).minutes.do(job)
# # 매 시간 실행
# schedule.every(12).hour.do(job)
# # 매일 10:30 에 실행
# schedule.every().day.at("10:30").do(job)
# # 매주 월요일 실행
# schedule.every().monday.do(job)
# # 매주 수요일 13:15 에 실행
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
