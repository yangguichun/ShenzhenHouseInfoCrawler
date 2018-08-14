from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler
from src.OldHouseSourceCrawler import OldHouseSourceCrawler
from src.NewHouseSourceCrawler import NewHouseSourceCrawler
from src.utils import utils
import time
import schedule
import traceback

print('-----------程序启动--------------')
def query_job():
    try:
        utils.print('---------------开始轮询-------------------')
        # new = NewHouseDealInfoCrawler()
        # new.crawl()
        # old = OldHouseDealInfoCrawler()
        # old.crawl()
        # oldsource = OldHouseSourceCrawler()
        # oldsource.crawl()
        newsource = NewHouseSourceCrawler()
        newsource.crawl()
        utils.print('---------------结束轮询-------------------')
        print('')
    except Exception as e:
        utils.print('在轮询期间发生未知错误, {}'.format(str(e)))
        traceback.print_exc()

schedule.every().day.at('12:00').do(query_job)

query_job()
while True:
    schedule.run_pending()
    time.sleep(50)

utils.print('-----------程序退出----------------')
