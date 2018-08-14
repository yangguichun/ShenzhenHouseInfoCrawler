from src.Dao.Daobase import Daobase
from datetime import datetime as dt
from datetime import timedelta


class OldHouseDealInfoDao(Daobase):
    '''
    向数据库中写入二手房成交信息
    '''
    @classmethod
    def __oldhouse_byuse_sqlmaker(cls, house):
        columns = ['thedate', 'region', 'use_type','area', 'deal_count']
        sql = "insert into oldhousebyuse ({}) values('{}','{}','{}',{},{})".format(
            ','.join(columns), dt.now() + timedelta(-1), house['region'], house['use_type'],  house['area'], house['deal_count'])
        return sql

    @classmethod
    def __oldhouse_byuse_infogetter(cls, house):
        return '{}, {}'.format(house['region'], house['use_type'])

    @classmethod
    def write_oldhouse_byuse(cls, house_list):
        cls.writelist(house_list, cls.__oldhouse_byuse_sqlmaker, cls.__oldhouse_byuse_infogetter)
