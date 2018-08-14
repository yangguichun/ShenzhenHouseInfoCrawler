from src.utils import  utils
from bs4 import BeautifulSoup
from src.NewHSrcHousePageDecoder import NewHSrcHousePageDecoder
import time

class NewHSrcBldPageDecoder:
    '''
    提取楼栋页面的信息
    '''
    __url = 'http://ris.szpl.gov.cn/bol/'
    __project_name = ''
    __building_name = ''
    @classmethod
    def decode(cls, page_node, building_name, project_name):
        '''
        :param page_node:
        :return:  返回一个house_list
        '''
        cls.__project_name = project_name
        cls.__building_name = building_name
        branch_node = page_node.find('div', id='divShowBranch')
        branch_info = {}
        if branch_node is not None:
            branch_info = cls.__decode_branch_info(branch_node)

        house_list_node = cls.__get_house_list_node(page_node)
        house_list = []
        if house_list_node is not None:
            house_list = cls.__decode_house_list(house_list_node, branch_info['current'])

        for branch in branch_info['list']:
            r = utils.request_with_retry(branch['url'])
            html_node = BeautifulSoup(r.text, 'lxml')
            house_list_node = cls.__get_house_list_node(html_node)
            if house_list_node is not None:
                house_list.extend(cls.__decode_house_list(house_list_node, branch['name']))

        return house_list

    @classmethod
    def __get_house_list_node(cls, page_node):
        '''找到房间列表的根节点'''
        update_panel_node = page_node.find('div', id='updatepanel1')
        if update_panel_node is None:
            return None
        table_list = update_panel_node.find_all('table')
        if len(table_list) < 3:
            return None
        return table_list[2]

    @classmethod
    def __decode_branch_info(cls, branch_root_node):
        '''
        解析座号列表，获取当前座号，以及其他座号列表
        :param branch_root_node:
        :return:
        result['current'] = [A]座
        result['list]['url]
        '''
        branch_info = {}
        branch_info['list'] = []
        current_branch_node = branch_root_node.find('font')
        if current_branch_node is not None:
            branch_info['current'] = utils.remove_blank_char(current_branch_node.text)
        branch_nodes = branch_root_node.find_all('a')
        for branch_node in branch_nodes:
            branch = {}
            branch['url'] = '{}{}'.format(cls.__url, branch_node['href'])
            branch['name'] = utils.remove_blank_char(branch_node.text)
            branch_info['list'].append(branch)
        return branch_info

    @classmethod
    def __decode_house_list(cls, house_root_node, branch_name):
        '''从房间根节点中，解析出所有的房间列表'''
        floor_nodes = house_root_node.find_all('tr', class_='a1')
        house_list = []
        for floor_node in floor_nodes:
            one_floor_house_list = cls.__decode_floor(floor_node, branch_name)
            if len(one_floor_house_list) > 0:
                house_list.extend(one_floor_house_list)
        return house_list

    @classmethod
    def __decode_floor(cls, floor_node, branch_name):
        '''解析某一层的房间列表
        '''
        house_nodes = floor_node.find_all('td')
        house_list = []
        for house_node in house_nodes:
            house = cls.__decode_house(house_node, branch_name)
            if house is not None:
                house_list.append(house)
        return house_list

    @classmethod
    def __decode_house(cls, house_node, branch_name):
        '''
        :param house_node:
        :param branch_name:
        :return:
        '''
        div_nodes = house_node.find_all('div')
        if len(div_nodes) != 2:
            utils.print('获取房间信息失败： {}, {}'.format(branch_name, house_node.text))
            return None
        house = {}
        house['branch'] = branch_name
        house['room_num'] = utils.remove_blank_char(div_nodes[0].text)
        href_node = div_nodes[1].find('a')
        if href_node is None:
            utils.print('获取房间的连接信息失败, {}, {}'.format(branch_name, house_node.text))
            return None

        url = '{}{}'.format(cls.__url, href_node['href'])
        utils.print('读取房间 {} {} {} {}的信息...'.format(cls.__project_name, cls.__building_name, branch_name, house['room_num']))
        r = utils.request_with_retry(url)
        if r is None:
            utils.print('读取房屋{}的页面信息失败'.format(house['room_num']))
            return None

        html_node = BeautifulSoup(r.text, 'lxml')
        return NewHSrcHousePageDecoder.decode(html_node)
