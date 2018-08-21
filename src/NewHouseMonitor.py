import re
from src.Dao.NewHouseSourceDao import NewHouseSourceDao
from src.utils import  utils
from bs4 import BeautifulSoup
from src.CrawlerBase import CrawlerBase
from src.MailSender import MailSender


class NewHouseMonitor(CrawlerBase):
    '''
    从这里获取深圳的一手房源信息http://ris.szpl.gov.cn/bol/
    每小时检查一次，如果发现新项目，则记录下来，并通知相关人员
    '''
    __url = 'http://ris.szpl.gov.cn/bol/'

    def run(self):
        utils.print('正在读取项目列表...')
        r = utils.request_with_retry(self.__url)
        if r is None:
            utils.print('读取项目页面失败...')
            return
        html_node = BeautifulSoup(r.text, 'lxml')
        project_nodes = self.__get_project_nodes(html_node)
        for project_node in project_nodes:
            project = self.__convert_project_node_to_project(project_node)
            if project is None:
                continue
            project['is_crawled'] = False
            writedcount = NewHouseSourceDao.write_project_summary(project)
            if writedcount > 0:
                MailSender.send_alarm_message('深圳有新地产项目通过预售', str(project))


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
