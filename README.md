# ShenzhenHouseInfoCrawler
主要包含2个方面的功能：
- 抓取数据，每天从[深圳房地产信息网](http://ris.szpl.gov.cn/default.aspx)中抓取深圳每日的[一手](http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=0)、[二手](http://ris.szpl.gov.cn/credit/showcjgs/esfcjgs.aspx)房成交信息，深圳的每日新放出的[二手房源信息](http://ris.szpl.gov.cn/bol/essource.aspx)，深圳的[新房预售信息](http://ris.szpl.gov.cn/bol/)等。抓取的数据存储在Postgresql数据数据库中，可以使用script.sql来创建数据库中对应的表；
- 数据分析，用pandas、matplotlib对这些数据做各种维度的统计分析；
