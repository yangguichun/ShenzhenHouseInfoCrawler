from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler
from src.OldHouseSourceCrawler import OldHouseSourceCrawler
from src.NewHSrcProjectCrawler import NewHSrcProjectCrawler
from src.NewHSrcOneProjectCrawler import NewHSrcOneProjectCrawler
from src.NewHouseMonitor import NewHouseMonitor
from src.Dao.NewHouseSourceDao import NewHouseSourceDao
from src.utils import utils
import time
import schedule
import traceback
import os


class NewHouseDetailQuerier:
    '''
    控制抓取房源的频率
    因为定时器每秒钟调用次该方法，为了避免在全部抓取完之后调用过于频繁，这里使用一些计数器来控制调用的频率
    '''
    __MAX_INTERVAL = 3600
    def __init__(self):
        self.__query_interval = 1
        self.__query_counter = 0
        self.__new_house_crawler = NewHSrcOneProjectCrawler()

    def query_one_project(self):
        '''
        每次抓取一个项目的信息，然后继续等待
        :return:
        '''
        self.__query_counter +=1
        if self.__query_counter < self.__query_interval:
            return

        self.__query_counter = 0
        if self.__new_house_crawler.crawl():
            # 如果抓取成功一次，说明有房源信息，则一会要接着抓
            __query_new_house_interval = 1
        else:
            self.__query_interval *= 2
            if self.__query_interval > self.__MAX_INTERVAL:
                __query_new_house_interval = self.__MAX_INTERVAL


class ShenzhenHouseCrawler:
    @classmethod
    def query_every_day_data(self):
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

    @classmethod
    def crawl_new_house_source_projects(self):
        if NewHouseSourceDao.get_one_project(None) is not None:
            utils.print('已经抓取过房源信息...')
            return
        new_house_source_crawler = NewHSrcProjectCrawler()
        new_house_source_crawler.crawl()

    @classmethod
    def query_and_mail_new_house_info(self):
        monitor = NewHouseMonitor()
        monitor.run()


utils.print('-----------程序启动--------------')

new_house_detail_querier =  NewHouseDetailQuerier()
def schedule_task():
    # 每秒钟检查一次是否有新房源要抓取
    schedule.every().second.do(new_house_detail_querier.query_one_project)
    # 每小时检查是否有新房通过预售
    schedule.every().hour.do(ShenzhenHouseCrawler.query_and_mail_new_house_info)
    # 每天12点抓取当天的 新房和二手房成交信息
    schedule.every().day.at('12:00').do(ShenzhenHouseCrawler.query_every_day_data)



schedule_task()
ShenzhenHouseCrawler.crawl_new_house_source_projects()
ShenzhenHouseCrawler.query_and_mail_new_house_info()
ShenzhenHouseCrawler.query_every_day_data()

while True:
    schedule.run_pending()
    time.sleep(1)

utils.print('-----------程序退出----------------')
