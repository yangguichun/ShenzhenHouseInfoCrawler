import psycopg2
from datetime import datetime as dt
from datetime import timedelta


class Daobase:
    '''
    数据库访问基础类
    '''
    @classmethod
    def get_connection(cls):
        return psycopg2.connect(database="loushi", user="postgres", password="00", host="127.0.0.1", port="5432")

    @classmethod
    def writelist(cls, item_list, sqlmaker, info_getter):
        '''
                将houseList 的信息写入到数据库中
                :param item_list:
                :return: 返回写成功了多少个
                '''
        succ_counter = 0
        conn = cls.get_connection()
        cur = conn.cursor()
        for house in item_list:
            try:
                # print(sql)
                sql = sqlmaker(house)
                if sql is not None:
                    cur.execute(sql)
                    conn.commit()
                    succ_counter += 1
            except Exception as err:
                print('{}write item ({}) failed, unknown error: {}, sql: {}'.format(dt.now(), info_getter(house), err, sql))
                conn.rollback()
        conn.close()
        return succ_counter

    @classmethod
    def writeoneitem(cls, item, sqlmaker, info_getter):
        '''
        将houseList 的信息写入到数据库中
        :param item_list:
        :return: 返回写成功了多少个
        '''
        succ_counter = 0
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # print(sql)
            sql = sqlmaker(item)
            cur.execute(sql)
            conn.commit()
            succ_counter =+ 1
        except Exception as err:
            print('{}write item ({}) failed, sql:{}, unknown error: {}'.format(dt.now(), info_getter(item),sql, err))
            conn.rollback()
        finally:
            conn.close()
        return succ_counter

    @classmethod
    def select(cls, sql):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # print(sql)
            cur.execute(sql)
            return cur.fetchall()
        except Exception as err:
            print('{}, execute sql {} failed, unknown error: {}'.format(dt.now(), sql, err))
            conn.rollback()
        finally:
            conn.close()

    @classmethod
    def update(cls, sql):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # print(sql)
            res = cur.execute(sql)
            conn.commit()
        except Exception as err:
            print('{}, execute sql {} failed, unknown error: {}'.format(dt.now(), sql, err))
            conn.rollback()
        finally:
            conn.close()


