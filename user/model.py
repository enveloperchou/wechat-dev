from sqlalchemy import Column, create_engine, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class USER(Base):
	__tablename__ = 'user'

	uid = Column(String(), primary_key=True)
	nick_name = Column(String())
	avatar_url = Column(String())
	gender = Column(Integer())
	provice = Column(String())
	city = Column(String())
	country = Column(String())


engine = create_engine('mysql+mysqlconnector://root:iwanttest235@#%@10.9.142.53:3306/test')
DBSession = sessionmaker(bind=engine)
