import psycopg2
from datetime import datetime as dt
from datetime import timedelta


class DbInterface:

    @classmethod
    def __write_house(self, house_list, sqlmaker, house_info_getter):
        '''
                将houseList 的信息写入到数据库中
                :param house_list:
                :return:
                '''
        conn = psycopg2.connect(database="loushi", user="postgres", password="pg", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        for house in house_list:
            try:
                # print(sql)
                cur.execute(sqlmaker(house))
                conn.commit()
            except Exception as err:
                print('{}write house({}) failed, unknown error: {}'.format(dt.now(), house_info_getter(house), err))
                conn.rollback()

        # conn.commit()
        conn.close()

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
        cls.__write_house(house_list, cls.__newhouse_bytype_sqlmaker, cls.__newhouse_bytype_infogetter);


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
        cls.__write_house(house_list, cls.__newhouse_byuse_sqlmaker, cls.__newhouse_byuse_infogetter)

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
        cls.__write_house(house_list, cls.__newhouse_byarea_sqlmaker, cls.__newhouse_byarea_sqlmaker)

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
        cls.__write_house(house_list, cls.__oldhouse_byuse_sqlmaker, cls.__oldhouse_byuse_infogetter)
