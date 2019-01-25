from sqlalchemy import Column, String, Integer, Float, Date, create_engine, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


Base = declarative_base()

class NewHouseByArea(Base):
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


#
load_dotenv()
engine = create_engine(os.getenv('DATABASE_URI', 'sqlite:///:memory:'))
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# newhouse = NewHouseByArea(thedate='2019-2-2', region='福田区', area_level='90平方米以下', deal_count=1234, area=90, price=42000, total_price=350)
# session.add(newhouse)
# session.commit()
# session.close()
