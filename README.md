# ShenzhenHouseInfoCrawler
主要包含2个方面的功能：
- 抓取数据，每天从[深圳房地产信息网](http://ris.szpl.gov.cn/default.aspx)中抓取深圳每日的一手、二手房成交信息，深圳的每日新放出的二手房源信息，深圳的新房预售信息等。抓取的数据存储在Postgresql数据数据库中，可以使用script.sql来创建数据库中对应的表；
- 数据分析，用pandas、matplotlib对这些数据做各种维度的统计分析；
