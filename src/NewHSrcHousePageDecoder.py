from src.utils import  utils
from bs4 import BeautifulSoup
import re

class NewHSrcHousePageDecoder:
    '''
    解析一个房屋页面的信息
    '''
    @classmethod
    def decode(cls, page_node):
        '''
        id serial not null,
        building_name character varying(255), --几栋
        branch character varying(10),   --座号
        house_type character varying(255),
        contact_code character varying(255),
        price double precision,
        floor integer,
        room_num character varying(50),
        usage character varying(50),
        build_area double precision,
        inside_area double precision,
        share_area double precision,
        :param page_node:
        :return:
        '''
        tr_nodes = page_node.find_all('tr', class_='a1')
        house_info = {}
        try:
            for tr_node in tr_nodes:
                temp_house = cls.__decode_one_row(tr_node)
                house_info.update(temp_house)
            return house_info
        except Exception as e:
            utils.print('解析房屋页面信息时发生错误， error: {}'.format( str(e)))
            return None

    @classmethod
    def __decode_one_row(cls, row_node):
        column_nodes = row_node.find_all('td')
        if len(column_nodes) < 2:
            return {}
        first_column_text = utils.remove_blank_char(column_nodes[0].text)
        if first_column_text == '项目楼栋情况':
            return cls.__decode_project_buiding_branch_row(column_nodes)
        elif first_column_text == '合同号':
            return cls.__decode_contact_and_price(column_nodes)
        elif first_column_text == '楼层':
            return cls.__decode_floor_roomnum_usage(column_nodes)
        elif first_column_text == '建筑面积':
            return cls.__decode_area(column_nodes)
        else:
            return {}

    @classmethod
    def __decode_project_buiding_branch_row(cls, column_nodes):
        house = {}
        if utils.remove_blank_char(column_nodes[0].text) == '项目楼栋情况':
            house['building_name'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '座号':
            house['branch'] = utils.remove_blank_char(column_nodes[3].text)
        if utils.remove_blank_char(column_nodes[4].text) == '户型':
            house['house_type'] = utils.remove_blank_char(column_nodes[5].text)
        return house

    @classmethod
    def __decode_contact_and_price(cls, column_nodes):
        house = {}
        if utils.remove_blank_char(column_nodes[0].text) == '合同号':
            house['contact_code'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '备案价格':
            price_text = utils.remove_blank_char(column_nodes[3].text)
            #58800元 / 平方米(按建筑面积计)
            price = re.findall(r'(\d+)元', price_text)
            house['price'] = 0
            if len(price) > 0:
                house['price'] = price[0]
        return house

    @classmethod
    def __decode_floor_roomnum_usage(cls, column_nodes):
        house = {}
        if utils.remove_blank_char(column_nodes[0].text) == '楼层':
            house['floor'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '房号':
            house['room_num'] = utils.remove_blank_char(column_nodes[3].text)
        if utils.remove_blank_char(column_nodes[4].text) == '用途':
            house['usage'] = utils.remove_blank_char(column_nodes[5].text)
        return house

    @classmethod
    def __decode_area(cls, column_nodes):
        house = {}
        if utils.remove_blank_char(column_nodes[0].text) == '建筑面积':
            house['build_area'] = utils.get_num(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '户内面积':
            house['inside_area'] = utils.get_num(column_nodes[3].text)
        if utils.remove_blank_char(column_nodes[4].text) == '分摊面积':
            house['share_area'] = utils.get_num(column_nodes[5].text)
        return house
