import re
from src.Dao.NewHouseSourceDao import NewHouseSourceDao
from src.utils import  utils
from bs4 import BeautifulSoup
from src.CrawlerBase import CrawlerBase


class NewHSrcProjectCrawler(CrawlerBase):
    '''
    从这里获取深圳的一手房源信息http://ris.szpl.gov.cn/bol/
    把每个预售的楼盘的所有信息都抓取下来，包括项目信息，几栋楼，几套房，每套房的信息等
    '''
    __url = 'http://ris.szpl.gov.cn/bol/'
    __total_page_count = 0
    __has_read_total_page_count = False

    def crawl(self, start_page = 1):
        #先读取第一页，获取上下文信息
        self.__crawl_one_page_project(1)
        page_index  = start_page
        while True:
            self.__crawl_one_page_project(page_index)
            if self.__total_page_count < page_index:
                break
            page_index += 1

    def __create_form_data(self, page_index):
        form_data = self.form_data
        form_data['__EVENTTARGET'] = 'AspNetPager1'
        form_data['__EVENTARGUMENT'] = page_index
        form_data['AspNetPager1_input'] = page_index -1
        form_data['tep_name'] = ''
        form_data['organ_name'] = ''
        form_data['site_address'] = ''
        return form_data

    def __crawl_one_page_project(self, page_index):
        r = None
        utils.print('正在读取第%d页项目列表...' % page_index)
        if page_index == 1:
            r = utils.request_with_retry(self.__url)
        else:
            r = utils.request_with_retry('{}index.aspx'.format(self.__url), self.__create_form_data(page_index))
        if r is None:
            utils.print('读取项目页面失败, page_index = {}'.format(page_index))
            return
        html_node = BeautifulSoup(r.text, 'lxml')
        self.extract_formdata_from_newpage(html_node)
        if page_index == 1:
            self.__get_total_count(html_node)

        project_nodes = self.__get_project_nodes(html_node)
        project_list = []
        for project_node in project_nodes:
            project = self.__convert_project_node_to_project(project_node)
            if project is None:
                continue
            project['is_crawled'] = False
            project_list.append(project)
        utils.print('解析出%d条项目信息' % len(project_list))
        writedcount = NewHouseSourceDao.write_project_summary_list(project_list)
        utils.print('写入数据库 %d 条记录' % writedcount)

    def __get_total_count(self, node):
        '''从node中读取总页数'''
        page_info_node = node.find('div', class_='PageInfo')
        if page_info_node is None:
            self.__total_page_count = 0
        page_info_text = page_info_node.text
        page_count = re.findall(r'总共(\d+)页', page_info_text)
        if len(page_count) > 0:
            count = int(page_count[0])
            self.__total_page_count = count

    def __get_project_nodes(self, node):
        '''从html中找出所有预售项目的行'''
        table_node = node.find('table', id='DataList1')
        if table_node is None:
            utils.print('获取项目列表表格失败...')
            return []
        sub_table_node = table_node.find('table')
        if sub_table_node is None:
            utils.print('获取项目列表子表格失败...')
            return []
        project_nodes = sub_table_node.find_all('tr')
        if len(project_nodes) < 3:
            return []

        #前两行是标题和空行
        del project_nodes[0]
        del project_nodes[0]
        return project_nodes


    def __convert_project_node_to_project(self, project_node):
        column_nodes = project_node.find_all('td')
        if len(column_nodes) < 6:
            return None
        project = {}
        project['presale_license_num'] = column_nodes[1].text
        project['project_name'] = column_nodes[2].text
        project_link_node = column_nodes[2].find('a')
        if project_link_node is not None:
            project['url'] = '{}{}'.format(self.__url, project_link_node['href'])
        project['builder'] = column_nodes[3].text
        project['region'] = column_nodes[4].text
        project['thedate'] = column_nodes[5].text
        return project
