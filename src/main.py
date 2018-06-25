from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler
from src.OldHouseSourceCrawler import OldHouseSourceCrawler
import re

print('-----------start--------------')
new = NewHouseDealInfoCrawler()
new.crawl()
old = OldHouseDealInfoCrawler()
old.crawl()
# oldsource = OldHouseSourceCrawler(555)
# oldsource.crawl()
print('-----------end----------------')
