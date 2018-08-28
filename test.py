import schedule
import time
from src.utils import utils


def job1():
    utils.print('job1')
    counter = 0
    while True:
        time.sleep(1)
        counter+=1
        if counter > 120:
            break

def job2():
    utils.print('job2')


schedule.every(1).second.do(job1)
#schedule.every(5).seconds.do(job2)
schedule.every().day.at('22:56').do(job2)

while True:
    schedule.run_pending()
    time.sleep(1)
