import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime as dt
from src.DbInterface import DbInterface
from src.CrawlerBase import CrawlerBase
from src.utils import utils
class NewHouseDealInfoCrawler(CrawlerBase):
    '''
    爬取深圳市每天的新房成交信息
    '''
    __url = 'http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=0'

    def crawl(self):
        '''
        url=
        要创建3个表来存储相关数据：按照户型、面积和类型分别存储
        然后，对于每种类型，要分别爬取全市、南山、福田、罗湖、盐田、保安、龙岗 七个区域的数据
        :return:
        '''
        utils.print('---开始抓取深圳新房成交数据---')
        for area in self.areas:
            self.__query_one_area(area)


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
            self.form_data['ctl00$ContentPlaceHolder1$scriptManager1'] = fromdata['ctl00$ContentPlaceHolder1$scriptManager1']
            self.form_data['__EVENTTARGET'] = fromdata['__EVENTTARGET']
            r = utils.request_with_retry(self.__url, self.form_data)

        s = BeautifulSoup(r.text, 'lxml')
        self.extract_formdata_from_newpage(s)
        self.__extract_info_from_page_into_db(s, area_name)


    def __extract_info_from_page_into_db(self, pageNode, area_name):
        typeNode = pageNode.find('tr', id='TrClientList1')
        if typeNode is not None:
            house_list = self.__extact_by_type(typeNode, area_name)
            if len(house_list) > 0:
                DbInterface.write_newhouse_bytype(house_list)

        areaNode = pageNode.find('tr', id='TrClientList5')
        if areaNode is not None:
            house_list = self.__extract_by_area(areaNode, area_name)
            if len(house_list) > 0:
                DbInterface.write_newhouse_byarea(house_list)

        useNode = pageNode.find('tr', id='TrClientList2')
        if useNode is not None:
            house_list = self.__extract_by_use(useNode, area_name)
            if len(house_list) > 0:
                DbInterface.write_newhouse_byuse(house_list)

    def __get_num(self, text):
        nums = re.findall(r'\d+\.?\d+', text)
        if len(nums)>0:
            return nums[0]
        else:
            return 0


    def __extact_by_type(self, node, area_name):
        '''
        提取了所有按照类型划分的数据
        :param node:
        :return:
        '''
        utils.print('提取按照户型分类的数据...')
        table = node.find('table')
        if table is None:
            utils.print('没有找到按照户型分类的数据')
            return []

        row_node_list = table.find_all('tr')
        i = 0
        house_list = []
        for row in row_node_list:
            if i == 0:
                i += 1
                continue
            columns = row.find_all('td')
            if len(columns)<6:
                continue
            house = {}
            house['region']=area_name
            house['house_type'] = columns[0].text
            house['deal_count'] = columns[1].text
            house['area'] = area = utils.get_num(columns[2].text)
            house['price'] = utils.get_num(columns[3].text)
            house['availableforsalecount'] = utils.get_num(columns[4].text)
            house['availableforsalearea'] = utils.get_num(columns[5].text)

            house_list.append(house)
            i+=1
        return house_list

    def __extract_by_area(self, node, area_name):
        '''
        按照面积的大小分类
        :param node:
        :param area_name:
        :return:
        '''
        utils.print('提取按照面积分类的数据...')
        table = node.find('table')
        if table is None:
            utils.print('没有找到按照面积分类的数据')
            return []

        row_node_list = table.find_all('tr')
        i = 0
        house_list = []
        for row in row_node_list:
            if i == 0:
                i += 1
                continue
            columns = row.find_all('td')
            if len(columns)<5:
                continue
            house = {}
            house['region'] = area_name
            house['area_level'] = columns[0].text
            house['deal_count'] = columns[1].text
            house['area'] = area = utils.get_num(columns[2].text)
            house['price'] = utils.get_num(columns[3].text)
            house['total_price'] = utils.get_num(columns[4].text)
            house_list.append(house)
            i += 1
        return house_list

    def __extract_by_use(self, node, area_name):
        utils.print('提取按照用途分类的数据...')
        table = node.find('table')
        if table is None:
            utils.print('没有找到按照用户分类的数据')
            return []

        row_node_list = table.find_all('tr')
        i = 0
        house_list = []
        for row in row_node_list:
            if i == 0:
                i += 1
                continue
            columns = row.find_all('td')
            if len(columns)<6:
                continue
            house = {}
            house['region']=area_name
            house['use_type'] = columns[0].text
            house['deal_count'] = columns[1].text
            house['area'] = area = utils.get_num(columns[2].text)
            house['price'] = utils.get_num(columns[3].text)
            house['availableforsalecount'] = utils.get_num(columns[4].text)
            house['availableforsalearea'] = utils.get_num(columns[5].text)
            house_list.append(house)
            i += 1
        return house_list

