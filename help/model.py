from sqlalchemy import Column, create_engine, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HELP(Base):
	__tablename__ = 'help'

	id = Column(Integer(), primary_key=True)
	type = Column(String())
	title = Column(String())
	description = Column(String())
	offer = Column(String())
	time = Column(Integer())

engine = create_engine('mysql+mysqlconnector://root:iwanttest235@#%@10.9.142.53:3306/test')
DBSession = sessionmaker(bind=engine)
