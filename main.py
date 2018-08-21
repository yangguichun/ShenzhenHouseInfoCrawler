from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler
from src.OldHouseSourceCrawler import OldHouseSourceCrawler
from src.NewHouseSourceCrawler import NewHouseSourceCrawler
from src.NewHSrcProjectCrawler import NewHSrcProjectCrawler
from src.NewHouseMonitor import NewHouseMonitor
from src.utils import utils
import time
import schedule
import traceback
import os

utils.print('-----------程序启动--------------')
def query_job():
    try:
        utils.print('---------------开始轮询-------------------')
        # new_deal = NewHouseDealInfoCrawler()
        # new_deal.crawl()
        # old_deal = OldHouseDealInfoCrawler()
        # old_deal.crawl()
        # old_source = OldHouseSourceCrawler()
        # old_source.crawl()
        # new_source = NewHouseSourceCrawler()
        # new_source.crawl()
        # new_house_list_crawler = NewHSrcProjectCrawler()
        # new_house_list_crawler.crawl()
        utils.print('---------------结束轮询-------------------')
        print('')
    except Exception as e:
        utils.print('在轮询期间发生未知错误, {}'.format(str(e)))
        traceback.print_exc()

def monitor():
    monitor = NewHouseMonitor()
    monitor.run()

schedule.every().day.at('12:00').do(query_job)
schedule.every().hour.do(monitor)

monitor()
query_job()
while True:
    schedule.run_pending()
    time.sleep(50)

utils.print('-----------程序退出----------------')
