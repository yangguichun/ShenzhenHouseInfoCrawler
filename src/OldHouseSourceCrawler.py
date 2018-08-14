from bs4 import BeautifulSoup
from src.Dao.OldHouseSourceDao import OldHouseSourceDao
from src.utils import utils
import re


class OldHouseSourceCrawler:
    def __init__(self, pageIndex = 1):
        self.__page_index = pageIndex
        pass

    __url = 'http://ris.szpl.gov.cn/bol/EsSource.aspx?targetpage={}&zone=&tep_name='
    __page_size = 20
    __total_count = 39782

    def crawl(self):
        utils.print('开始抓取二手房源数据...')
        pageindex = self.__page_index
        while True:
            try:
                if not self.__crawl_one_page(pageindex):
                    break
            except Exception as e:
                utils.print('抓取第{}页失败, {}'.format(pageindex, str(e)))
                continue

            if self.__total_count < self.__page_size * (pageindex - 1):
                break
            pageindex += 1

    def __get_total_count(self, node):
        '''
        从第一页的数据中提取总数
        :param node:
        :return:
        '''
        spans = node.find_all('span', class_='a1')
        if len(spans) != 2:
            utils.print('查找记录总数失败')
            return False
        nums = re.findall(r'\d+', spans[1].text)
        if len(nums) != 1:
            utils.print('从字符串 {} 提取记录总数失败'.format(spans[1].text))
            return
        self.__total_count = int(nums[0])
        return True


    def __crawl_one_page(self, pageindex):
        '''
        抓去一页的房屋信息
        :param pageindex:
        :return: 是否要继续查找下一页，如果当前页出错，或者查找的结果一个都没写进去，那就没必要再找下一页了
        '''
        utils.print('抓取第{}页...'.format(pageindex))
        url = self.__url.format(pageindex)
        r = utils.request_with_retry(url)
        s = BeautifulSoup(r.text, 'lxml')
        if pageindex == 1:
            if not self.__get_total_count(s):
                return False

        tablenode = s.find('table', id='DataGrid1')
        if tablenode is None:
            utils.print('查找表格失败')
            return False
        house_list = []

        house_nodes = tablenode.find_all('tr')
        for house_node in house_nodes:
            house_properties = house_node.find_all('td')
            if len(house_properties) <9:
                continue
            if house_properties[0].text == '项目名称':
                continue
            house = {}
            #columns = ['thedate', 'region', 'serial_num', 'project_name','area', 'use_type', 'code', 'agency_info']
            house['project_name'] = utils.remove_blank_char(house_properties[0].text)
            house['serial_num'] = house_properties[1].text
            house['region'] = utils.remove_blank_char(house_properties[2].text)
            house['area'] = house_properties[3].text
            house['use_type'] = house_properties[4].text
            house['code'] = house_properties[6].text
            house['agency_info'] = utils.remove_blank_char(house_properties[7].text)
            house['thedate'] = house_properties[8].text
            house_list.append(house)
        return OldHouseSourceDao.write_oldhouse_source(house_list) > 0
