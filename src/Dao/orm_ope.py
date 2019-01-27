from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime as dt
import src.Dao.orm as orm #把上面orm中定义好的东西拿来用


SessionType = scoped_session(sessionmaker(bind=orm.engine))
#这里引入了scoped_session，相比于直接的sessionmaker，scoped_session返回的对象构造出来的对话对象是全局唯一的，不同的对话对象实例都指向一个对象引用    。
def GetSession():
    return SessionType()

from contextlib import contextmanager
###contextlib的用法可以看相关的那篇，这里不多说了###
@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def insert_item(item):
    try:
        with session_scope() as session:
            session.add(item)
        return True
    except Exception as e:
        print('{} write item ({}) failed, unknown error: {}'.format(dt.now(), item, e))
        return False

def insert_new_house_list(houseList):
    try:
        for house in houseList:
            insert_item(house)
        return True
    except Exception as e:
        print('{}insert new house list failed, unknown error: {}'.format(dt.now(), e))
        return False
