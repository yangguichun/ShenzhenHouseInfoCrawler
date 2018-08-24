from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler
from src.OldHouseSourceCrawler import OldHouseSourceCrawler
from src.NewHouseSourceCrawler import NewHouseSourceCrawler
from src.NewHSrcProjectCrawler import NewHSrcProjectCrawler
from src.NewHSrcOneProjectCrawler import NewHSrcOneProjectCrawler
from src.NewHouseMonitor import NewHouseMonitor
from src.Dao.NewHouseSourceDao import NewHouseSourceDao
from src.utils import utils
import time
import schedule
import traceback
import os

utils.print('-----------程序启动--------------')

__query_new_house_interval = 1
__query_new_house_counter = 0
__new_house_crawler = NewHSrcOneProjectCrawler()
def query_new_house_detail():
    '''
    每次抓取一个项目的信息，然后继续等待
    :return:
    '''
    global __query_new_house_interval
    global __query_new_house_counter
    __query_new_house_counter +=1

    if __query_new_house_counter < __query_new_house_interval:
        return

    __query_new_house_counter = 0
    if __new_house_crawler.crawl():
        __query_new_house_interval = 1
    else:
        __query_new_house_interval *= 2
        if __query_new_house_interval > 3600:
            __query_new_house_interval = 3600


def query_job():
    try:
        utils.print('---------------开始轮询-------------------')
        new_deal = NewHouseDealInfoCrawler()
        new_deal.crawl()
        old_deal = OldHouseDealInfoCrawler()
        old_deal.crawl()
        old_source = OldHouseSourceCrawler()
        old_source.crawl()
        utils.print('---------------结束轮询-------------------')
        print('')
    except Exception as e:
        utils.print('在轮询期间发生未知错误, {}'.format(str(e)))
        traceback.print_exc()

def crawl_new_house_source_projects():
    if NewHouseSourceDao.get_one_project(None) is not None:
        utils.print('已经抓取过房源信息...')
        return
    new_house_source_crawler = NewHSrcProjectCrawler()
    new_house_source_crawler.crawl()


def monitor_new_house():
    monitor = NewHouseMonitor()
    monitor.run()

# 每秒钟检查一次
schedule.every().second.do(query_new_house_detail)
# 每小时
schedule.every().hour.do(monitor_new_house)
# 每天12点
schedule.every().day.at('12:00').do(query_job)


# 如果是第一次，则把这个开关打开
crawl_new_house_source_projects()
monitor_new_house()
query_job()

while True:
    schedule.run_pending()
    # 50秒检查一次
    time.sleep(1)

utils.print('-----------程序退出----------------')
