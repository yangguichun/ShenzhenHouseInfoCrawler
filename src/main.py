from src.NewHouseDealInfoCrawler import NewHouseDealInfoCrawler
from src.OldHouseDealInfoCrawler import OldHouseDealInfoCrawler

print('-----------start--------------')
new = NewHouseDealInfoCrawler()
new.crawl()
old = OldHouseDealInfoCrawler()
old.crawl()
print('-----------end----------------')
