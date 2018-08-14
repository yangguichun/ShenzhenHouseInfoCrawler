from src.Dao.Daobase import Daobase

class OldHouseSourceDao(Daobase):
    '''
    向数据库中写入二手房源信息
    '''
    @classmethod
    def __oldhouse_source_sqlmaker(cls, house):
        columns = ['thedate', 'region', 'serial_num', 'project_name','area', 'use_type','code', 'agency_info']
        sql = "insert into oldhousesource ({}) values('{}','{}','{}','{}',{},'{}','{}','{}')".format(
            ','.join(columns), house['thedate'], house['region'],house['serial_num'],house['project_name'],house['area'],house['use_type'], house['code'], house['agency_info'])
        return sql

    @classmethod
    def __oldhouse_source_infogetter(cls, house):
        return '{},{}'.format(house['project_name'], house['serial_num'])

    @classmethod
    def write_oldhouse_source(cls, house_list):
        return cls.writelist(house_list, cls.__oldhouse_source_sqlmaker, cls.__oldhouse_source_infogetter)
