from sqlalchemy import Column,Table
from sqlalchemy import Integer,String
from pythonFiles import myConnection


BookCatalogue = Table('BookCatalogue',myConnection.metadata,
                      Column('id',Integer(),primary_key=True,autoincrement=True),
                      Column('user_id', Integer()),
                      Column('title',String(200)),
                      Column('author',String(200)),
                      Column('page_count',String(200)),
                      Column('average_rating',String(200)))
Users = Table('Users',myConnection.metadata,
              Column('id',Integer(),primary_key=True,autoincrement=True),
              Column('username',String(200)),
              Column('password',String(200)))