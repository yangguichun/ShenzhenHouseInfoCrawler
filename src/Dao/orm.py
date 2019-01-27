from sqlalchemy import Column, String, Integer, Float, Date, Boolean, create_engine, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


Base = declarative_base()

class NewHouseByArea(Base):
    '''--新房成交信息，按面积划分的信息'''
    __tablename__ = 'newhousebyarea'
    thedate = Column(Date, nullable=False, primary_key=True)
    region = Column(String(255), nullable=False, primary_key=True)
    area_level = Column(String(255), nullable=False, primary_key=True)
    deal_count = Column(Integer)
    area = Column(Float)
    price = Column(Float)
    total_price = Column(Integer)
    #PrimaryKeyConstraint(name='newhousebyarea_primary_key')

    def __repr__(self):
        return '<type "NewHouseByArea">{}, {}, {}'.format(self.thedate, self.region, self.area_level)
    def __str__(self):
        return self.__repr__()


class NewHouseByType(Base):
    '''--新房成交信息，按类型划分'''
    __tablename__ = 'newhousebytype'
    thedate = Column(Date, nullable=False, primary_key=True)
    region = Column(String(255), nullable=False, primary_key=True)
    house_type = Column(String(255), nullable=False, primary_key=True)
    deal_count = Column(Integer)
    area = Column(Float)
    price = Column(Float)
    availableforsalecount = Column(Integer)
    availableforsalearea = Column(Integer)
    #PrimaryKeyConstraint(name='newhousebytype_primary_key')


    def __repr__(self):
        return '<type "NewHouseByType">{}, {}, {}'.format(self.thedate, self.region, self.house_type)
    def __str__(self):
        return self.__repr__()


class NewHouseByUse(Base):
    '''新房成交信息，按用途划分'''
    __tablename__ = 'newhousebyuse'
    thedate = Column(Date, nullable=False, primary_key=True)
    region = Column(String(255), nullable=False, primary_key=True)
    use_type = Column(String(255), nullable=False, primary_key=True)
    deal_count = Column(Integer)
    area = Column(Float)
    price = Column(Float)
    availableforsalecount = Column(Integer)
    availableforsalearea = Column(Integer)
    #PrimaryKeyConstraint('thedate', 'region', 'use_type', name='newhousebyuse_primary_key')

    def __repr__(self):
        return '<type "NewHouseByUse">{}, {}, {}'.format(self.thedate, self.region, self.use_type)

    def __str__(self):
        return self.__repr__()


class OldHouseSource(Base):
    '''二手房成交信息，按用途划分'''
    __tablename__ = 'oldhousesource'
    thedate = Column(Date, nullable=False)
    region = Column(String(255), nullable=False)
    serial_num = Column(String(255), nullable=False, primary_key=True)
    project_name = Column(String(255), nullable=False)
    area = Column(Float)
    use_type = Column(String(255))
    code = Column(String(30))
    agency_info = Column(String(255))

    def __str__(self):
        return '<type "OldHouseSource">{}, {}, {}'.format(self.thedate, self.region, self.serial_num)

class NewHouseSourceProject(Base):
    '''--新房的预售信息，项目信息'''
    __tablename__ = 'newhousesrc_project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    thedate = Column(Date)
    region = Column(String(255), nullable=False)
    project_name = Column(String(255), nullable=False)
    builder = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    house_usage = Column(String(255), nullable=False)
    land_usage = Column(String(255))
    land_years_limit = Column(Integer)
    land_serial_num = Column(String(255))
    presale_license_num = Column(String(255), nullable=False, unique=True)
    pre_sale_count = Column(Integer)
    pre_area = Column(Float)
    now_sale_count = Column(Integer)
    now_area = Column(Float)
    def __str__(self):
        return '<type "NewHouseSourceProject">{}, {}'.format(self.region, self.project_name)


class NewHouseSourceBuilding(Base):
    '''--新房预售信息，楼栋信息'''
    __tablename__ = 'newhousesrc_building'
    id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(Integer, nullable=False)
    project_name = Column(String(255), nullable=False)
    building_name = Column(String(255), nullable=False)
    plan_license = Column(String(255), nullable=False)
    build_license = Column(String(255), nullable=False)
    is_crawled = Column(Boolean, nullable=False)

    def __str__(self):
        return '<type "NewHouseSourceBuilding">{}, {}'.format(self.project_name, self.building_name)



class NewHouseSourceHouse(Base):
    '''-- 新房预售，每一套房屋的信息'''
    __talbename__ = 'newhousesrc_house'
    id = Column(Integer, autoincrement=True, primary_key=True)
    build_id = Column(Integer, nullable=False)
    building_name = Column(String(255))
    branch = Column(String(10))
    room_num = Column(String(255))
    floor = Column(String(255))
    house_type = Column(String(255))
    contact_code = Column(String(255))
    price = Column(Float)
    usage = Column(String(255))
    build_area = Column(Float)
    inside_area = Column(Float)
    share_area = Column(Float)

    def __str__(self):
        return '<type "NewHouseSourceHouse">{}, {}, {}'.format(self.building_name, self.branch, self.room_num)


class NewHouseSourceProjectSummary(Base):
    '''--项目的简要信息，判断是否有新项目，以后后续的各种爬虫，都是基于这个来的'''
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    thedate = Column(Date, nullable=False)
    region = Column(String(255))
    presale_license_num = Column(String(255))
    project_name = Column(String)
    builder = Column(String(255))
    url = Column(String(1024), nullable=False)
    is_crawled = Column(Boolean)

    def __str__(self):
        return '<type "NewHouseSourceProjectSummary">{}, {}'.format(self.thedate, self.project_name)



# class TestId(Base):
#     __tablename__ = 'test_id'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     thedate = Column(Date)
#     region = Column(String(255), nullable=False, unique=True)



load_dotenv()
engine = create_engine(os.getenv('DATABASE_URI', 'sqlite:///:memory:'))
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# newhouse = NewHouseByArea(thedate='2019-2-2', region='福田区', area_level='90平方米以下', deal_count=1234, area=90, price=42000, total_price=350)
# session.add(newhouse)
# session.commit()
# session.close()
