from src.Dao.Daobase import Daobase
from datetime import datetime as dt
from datetime import timedelta


class NewHouseDealInfoDao(Daobase):
    '''
    向数据库中写入新房成交信息
    '''
    @classmethod
    def __newhouse_byuse_sqlmaker(cls, house):
        columns = ['thedate', 'region', 'use_type', 'deal_count', 'area', 'price', 'availableforsalecount',
                   'availableforsalearea']
        sql = "insert into newhousebyuse ({}) values('{}','{}','{}',{},{},{},{},{})".format(
            ','.join(columns),
            dt.now() + timedelta(-1), house['region'], house['use_type'], house['deal_count'], house['area'],
            house['price'], house['availableforsalecount'],
            house['availableforsalearea'])
        return sql

    @classmethod
    def __newhouse_byuse_infogetter(cls, house):
        return '{}, {}'.format(house['region'], house['use_type'])

    @classmethod
    def write_newhouse_byuse(cls, house_list):
        '''
        将houseList 的信息写入到数据库中
        :param house_list:
        :return:
        '''
        cls.writelist(house_list, cls.__newhouse_byuse_sqlmaker, cls.__newhouse_byuse_infogetter)


    @classmethod
    def __newhouse_byarea_sqlmaker(cls, house):
        columns = ['thedate', 'region', 'area_level', 'deal_count', 'area', 'price', 'total_price']
        sql = "insert into newhousebyarea ({}) values('{}','{}','{}',{},{},{},{})".format(
            ','.join(columns),
            dt.now() + timedelta(-1), house['region'], house['area_level'], house['deal_count'], house['area'],
            house['price'], house['total_price'])
        return sql

    @classmethod
    def __newhouse_byarea_infogetter(cls, house):
        return '{}, {}'.format(house['region'], house['area_level'])

    @classmethod
    def write_newhouse_byarea(cls, house_list):
        '''
        将houseList 的信息写入到数据库中
        :param house_list:
        :return:
        '''
        cls.writelist(house_list, cls.__newhouse_byarea_sqlmaker, cls.__newhouse_byarea_sqlmaker)

    @classmethod
    def __newhouse_bytype_sqlmaker(cls, house):
        columns = ['thedate', 'region', 'house_type', 'deal_count', 'area', 'price', 'availableforsalecount',
                   'availableforsalearea']
        sql = "insert into newhousebytype ({}) values('{}','{}','{}',{},{},{},{},{})".format(
            ','.join(columns),
            dt.now() + timedelta(-1), house['region'], house['house_type'], house['deal_count'], house['area'],
            house['price'], house['availableforsalecount'],
            house['availableforsalearea'])
        return sql

    @classmethod
    def __newhouse_bytype_infogetter(cls, house):
        return '{}, {}'.format(house['region'], house['house_type'])

    @classmethod
    def write_newhouse_bytype(cls, house_list):
        '''
        将houseList 的信息写入到数据库中
        :param house_list:
        :return:
        '''
        cls.writelist(house_list, cls.__newhouse_bytype_sqlmaker, cls.__newhouse_bytype_infogetter);

