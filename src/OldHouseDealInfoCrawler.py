from bs4 import BeautifulSoup
from datetime import datetime as dt
from src.DbInterface import DbInterface
from src.utils import utils
from src.CrawlerBase import CrawlerBase

class OldHouseDealInfoCrawler(CrawlerBase):
    '''
    爬取深圳市每天的新房成交信息
    '''
    __url = 'http://ris.szpl.gov.cn/credit/showcjgs/esfcjgs.aspx'

    def crawl(self):
        '''
        url=
        要创建3个表来存储相关数据：按照户型、面积和类型分别存储
        然后，对于每种类型，要分别爬取全市、南山、福田、罗湖、盐田、保安、龙岗 七个区域的数据
        :return:
        '''
        print('---开始抓取深圳二手房成交数据---')
        for area in self.areas:
            self.__query_one_area(area)

    def __extract_formdata_from_newpage(self, node):
        '''
        从新页面的html中提取fromdata数据，便于访问下一页
        :param node:
        :return:
        '''
        input_list = node.find_all('input')
        for input in input_list:
            if input['name'] == 'ctl00$ContentPlaceHolder1$radSelect':
                continue
            name = input['name']
            value = input['value']
            self.from_data[name] = value


    def __query_one_area(self, area_name):
        '''
        这个调用接口时，在fromdata中传递的参数不同
        返回的response也不同，第一行和最后一行不是html，不规范，要注意做兼容处理
        :param area_name:
        :return:
        '''
        print('{} query {} info...'.format(dt.now(), area_name))
        r = None
        if area_name == '全市':
            r = utils.request_with_retry(self.__url)
        else:
            fromdata = self.areas[area_name]
            self.from_data['ctl00$ContentPlaceHolder1$scriptManager1'] = fromdata['ctl00$ContentPlaceHolder1$scriptManager1']
            self.from_data['__EVENTTARGET'] = fromdata['__EVENTTARGET']
            r = utils.request_with_retry(self.__url, self.from_data)

        s = BeautifulSoup(r.text, 'lxml')
        self.__extract_formdata_from_newpage(s)
        self.__extract_info_from_page_into_db(s, area_name)

    def __extract_info_from_page_into_db(self, pageNode, area_name):
        useNode = pageNode.find('tr', id='TrClientList1')
        if useNode is not None:
            house_list = self.__extract_by_use(useNode, area_name)
            if len(house_list) > 0:
                DbInterface.write_oldhouse_byuse(house_list)

    def __extract_by_use(self, node, area_name):
        print('提取按照用途分类的数据...')
        table = node.find('table')
        if table is None:
            print('没有找到按照用户分类的数据')
            return []

        row_node_list = table.find_all('tr')
        i = 0
        house_list = []
        for row in row_node_list:
            if i == 0:
                i += 1
                continue
            columns = row.find_all('td')
            if len(columns)<3:
                continue
            house = {}
            house['region']=area_name
            house['use_type'] = columns[0].text
            house['deal_count'] = utils.get_num(columns[1].text)
            house['area'] = area = utils.get_num(columns[2].text)
            house_list.append(house)
            i += 1
        return house_list
