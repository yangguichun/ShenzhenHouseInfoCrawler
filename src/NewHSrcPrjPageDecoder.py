from src.utils import utils
from src.Dao.NewHouseSourceDao import NewHouseSourceDao

class NewHSrcPrjPageDecoder:
    __url = 'http://ris.szpl.gov.cn/bol/'

    @classmethod
    def decode_and_write(cls, page_node, project_info):
        project_info = cls.__decode(page_node, project_info)
        # 写入的结果不做判断，只看一会能不能获取到id，能获取到就算成功
        NewHouseSourceDao.write_project(project_info)
        project_id = NewHouseSourceDao.get_project_id(project_info)

        if project_id  == 0:
            utils.print('获取项目Id失败, {}'.format(project_info['project_name']))
            return False
        project_info['id'] = project_id
        return True

    @classmethod
    def __decode(cls, page_node, project_info):
        row_nodes = page_node.find_all('tr', class_='a1')
        if len(row_nodes) == 0:
            return {}

        for row_node in row_nodes:
            row_info = cls.__decode_one_project_info_row(row_node)
            if len(row_info) == 0:
                continue
            project_info.update(row_info)

        building_table_node = page_node.find('table', id='DataList1')
        project_info.update(cls.__decode_building_list(building_table_node))
        return project_info

    @classmethod
    def __decode_building_list(cls, building_table_node):
        '''
        project_id integer NOT NULL,
        project_name character varying(255) NOT NULL,
        building_name character varying(255) NOT NULL,
        plan_license character varying(255) NOT NULL,
        build_license character varying(255) NOT NULL,
        :param building_table_node:
        :return:
        '''
        project = {}
        project['building_list'] = []
        if building_table_node is None:
            return project

        building_nodes = building_table_node.find_all('tr')
        if len(building_nodes) < 4:
            return project

        #删除前3行，这是一些表头信息
        del building_nodes[0]
        del building_nodes[0]
        del building_nodes[0]
        for building_node in building_nodes:
            column_nodes = building_node.find_all('td')
            if len(column_nodes) < 5:
                continue
            building = {}
            building['project_name'] = utils.remove_blank_char(column_nodes[0].text)
            building['building_name'] = utils.remove_blank_char(column_nodes[1].text)
            building['plan_license'] = utils.remove_blank_char(column_nodes[2].text)
            building['build_license'] = utils.remove_blank_char(column_nodes[3].text)
            link_node = column_nodes[4].find('a')
            if link_node is not None:
                building['url'] = '{}{}'.format(cls.__url, utils.remove_blank_char(link_node['href']))
            project['building_list'].append(building)
        return project


    @classmethod
    def __decode_one_project_info_row(cls, row_node):
        '''解析这行，如果有需要的信息，就将他转换为字典'''
        column_nodes = row_node.find_all('td')
        if len(column_nodes) < 2:
            return {}
        first_column_text = utils.remove_blank_char(column_nodes[0].text)
        if first_column_text == '项目名称':
            return cls.__decode_project_name_row(column_nodes)
        elif first_column_text == '宗地位置':
            return cls.__decode_address_row(column_nodes)
        elif first_column_text == '合同文号':
            return cls.__decode_contact_num_row(column_nodes)
        elif first_column_text == '房屋用途':
            return cls.__decode_house_usage_row(column_nodes)
        elif first_column_text == '土地用途':
            return cls.__decode_land_usage_row(column_nodes)
        elif first_column_text == '预售总套数':
            return cls.__decode_pre_sale_row(column_nodes)
        elif first_column_text == '现售总套数':
            return cls.__decode_now_sale_row(column_nodes)
        else:
            return {}

    @classmethod
    def __decode_project_name_row(cls, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '项目名称':
            project['project_name'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '宗地号':
            project['land_serial_num'] = utils.remove_blank_char(column_nodes[3].text)
        return project

    @classmethod
    def __decode_address_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '宗地位置':
            project['address'] = utils.remove_blank_char(column_nodes[1].text)
        return project

    @classmethod
    def __decode_contact_num_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '合同文号':
            project['land_contact_num'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '使用年限':
            yearstr = utils.remove_blank_char(column_nodes[3].text)
            project['land_years_limit'] = utils.get_num(yearstr)
        return project

    @classmethod
    def __decode_house_usage_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '房屋用途':
            project['house_useage'] = utils.remove_blank_char(column_nodes[1].text)
        return project

    @classmethod
    def __decode_land_usage_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '土地用途':
            project['land_usage'] = utils.remove_blank_char(column_nodes[1].text)
        return project

    @classmethod
    def __decode_pre_sale_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '预售总套数':
            project['pre_sale_count'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '预售总面积':
            area = utils.remove_blank_char(column_nodes[3].text)
            if len(area) == 0:
                area = 0
            project['pre_area'] = area
        return project

    @classmethod
    def __decode_now_sale_row(self, column_nodes):
        project = {}
        if utils.remove_blank_char(column_nodes[0].text) == '现售总套数':
            project['now_sale_count'] = utils.remove_blank_char(column_nodes[1].text)
        if utils.remove_blank_char(column_nodes[2].text) == '现售总面积':
            area = utils.remove_blank_char(column_nodes[3].text)
            if len(area) == 0:
                area = 0
            project['now_area'] = area
        return project
