import re
from src.Dao.NewHouseSourceDao import NewHouseSourceDao
from src.utils import  utils
from bs4 import BeautifulSoup
from src.NewHSrcPrjPageDecoder import NewHSrcPrjPageDecoder
from src.NewHSrcBldPageDecoder import NewHSrcBldPageDecoder
from src.CrawlerBase import CrawlerBase


class NewHSrcOneProjectCrawler(CrawlerBase):
    '''
    从这里获取深圳的一手房源信息http://ris.szpl.gov.cn/bol/
    把每个预售的楼盘的所有信息都抓取下来，包括项目信息，几栋楼，几套房，每套房的信息等
    '''
    def crawl(self):
        project = NewHouseSourceDao.get_one_project()
        if project is None:
            utils.print('暂无项目可抓取...')
            return False
        self.__crawl_project_detail(project)
        return True

    def __crawl_project_detail(self, project_info):
        '''
        获取指定项目的详细信息，然后写入到数据库中
        :param url:
        :param project_info:  这个是从列表中获取的项目的简要信息
        :return:
        '''
        utils.print('读取项目{}页面'.format(project_info['project_name']))
        r = utils.request_with_retry(project_info['url'])
        if r is None:
            utils.print('读取项目: {} , 页面失败...'.format(project_info['project_name']))
            return False

        s = BeautifulSoup(r.text, 'lxml')
        if not NewHSrcPrjPageDecoder.decode_and_write(s, project_info):
            return False

        for building in project_info['building_list']:
            utils.print('读取 {} 的 {} 页面...'.format(project_info['project_name'], building['building_name']))
            building['project_id'] = project_info['id']
            building['is_crawled'] = False
            if NewHouseSourceDao.is_building_crawled(building) > 0:
                continue

            r = utils.request_with_retry(building['url'])
            if r is None:
                utils.print('读取项目 {} 的楼栋 {} 页面失败.'.format(project_info['project_name'], building['building_name']))
                continue

            html_node = BeautifulSoup(r.text, 'lxml')
            house_list = NewHSrcBldPageDecoder.decode(html_node, building['building_name'], project_info['project_name'])

            if NewHouseSourceDao.write_newhouse_building(building) == 0:
                continue
            building_id = NewHouseSourceDao.get_building_id(building)
            if building_id == 0:
                print('获取楼栋id失败，{}, {}'.format(project_info['project_name'], building['building_name']))
                continue
            for house in house_list:
                house['building_id'] = building_id

            NewHouseSourceDao.write_houselist(house_list)
            NewHouseSourceDao.update_building_state_to_crawled(building_id)

        NewHouseSourceDao.update_project_state_to_crawled(project_info['presale_license_num'])
