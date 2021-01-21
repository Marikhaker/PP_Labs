### crud.py ###

from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine
# make a session
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base, Order, Room, User
    #, orders_users_table
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
#Base.metadata.create_all(engine)
s = Session()

# book = Book(
#     title='Deep Learning',
#     author='Ian Goodfellow',
#     pages=775,
#     published=datetime(2016, 11, 18)
# )


# with engine.connect() as connection:
#     connection.execute(
#          orders.insert(),
#          data=[1,2,3]
#     )

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

Base.metadata.create_all(engine)
#recreate_database()
# s.add(tag1)
# s.add(tag2)
# s.add(category1)
# s.add(user1)
# s.add(room1)
# s.add(room2)
# s.add(tr_association1)
# s.add(tr_association2)
# s.add(order1)
# s.add(order2)
# s.add(order3)

s.commit()

s.close()