# ShenzhenHouseInfoCrawler
## 目的
- 分析深圳楼市趋势

## 主要功能
### 抓取数据
- 抓取深圳楼市数据，每天从[深圳房地产信息网](http://ris.szpl.gov.cn/default.aspx)中抓取以下信息
    - 每日的[一手房成交信息](http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=0)
    - 每日的[二手房成交信息](http://ris.szpl.gov.cn/credit/showcjgs/esfcjgs.aspx)
    - 每日的[新房预售信息](http://ris.szpl.gov.cn/bol/)
    - 历史的[二手房源信息](http://ris.szpl.gov.cn/bol/essource.aspx)
    - 历史的[预售信息](http://ris.szpl.gov.cn/bol/)
- 抓取的数据存储在Postgresql数据数据库中，可以使用script.sql来创建数据库中对应的表；

### 分析数据
- 长期运行，分析历史趋势，用pandas、matplotlib对这些数据做各种维度的统计分析

### 发现与通知
- 每天查询最新的预售信息，发现新的预售就及时邮件通知相关人员

## 依赖的库
- requests
- BeautifulSoap

## 如何使用
- 安装postgresql数据库
- 在postgresql内创建名字为loushi的数据库
- 在loushi内，使用script/script.sql创建对应的表
- 修改DbInterface.py中的数据库连接信息，设置正确的服务器地址和用户名密码
- 运行main.py

## 更新记录
- 20180814 
    - 支持抓取一手房源信息
    - 将main.py文件提取到根目录，便于pyinstaller生成exe文件
    - 使用scheduler调度库，每天中午查询一次，抓取相关一手、二手的房源和成交数据
