from sqlalchemy import MetaData
from sqlalchemy import create_engine

metadata = MetaData()
engine = create_engine('mysql+pymysql://root:root@localhost/bookCatalouge?charset=utf8')

connection = engine.connect()

metadata.create_all(engine)
