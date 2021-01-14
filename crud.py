### crud.py ###

from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine
# make a session
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base, Order, Room, User, Category, Tag, tag_room_association
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

tag1 = Tag(
    id = 1
)
tag2 = Tag(
    id = 2,
    name = "test tag2"
)

category1 = Category(
    id = 1,
    name = "test category1"
)

room1 = Room(
    id = 1,
    start_date = [datetime(2020, 12, 14)],
    end_date = [datetime(2020, 12, 15)],
    category_id = 1,
    #tags_id = [1,2],
    #tags_id = [tag1.id]
)

room2 = Room(
    id = 2,
    category_id = 1,
    name = "Test room2"
)

tr_association1 = tag_room_association(
    tag_id = 1,
    room_id = 1
)
tr_association2 = tag_room_association(
    tag_id = 1,
    room_id = 2
)

user1 = User(
    id = 1,
    username = "user1",
    reserved_rooms = [1]
)

order1 = Order(
    id = 1,
    roomId = 1,
    userId = 1,
    start_date = datetime(2020, 12, 14),
    end_date = datetime(2020,12,15)
    #status = 'Placed',
    #complete = False
)

order2 = Order(
    id = 2,
    roomId = 2,
    userId = 1,
    start_date = datetime(2020, 12, 16),
    end_date = datetime(2020,12,18)
    #status = 'Placed',
    #complete = False
)

order3 = Order(
    id = 3,
    roomId = 2,
    userId = 1,
    start_date = datetime(2020, 12, 20),
    end_date = datetime(2020,12,22)
    #status = 'Placed',
    #complete = False
)

# with engine.connect() as connection:
#     connection.execute(
#          orders.insert(),
#          data=[1,2,3]
#     )

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

#recreate_database()
s.add(tag1)
s.add(tag2)
s.add(category1)
s.add(user1)
s.add(room1)
s.add(room2)
s.add(tr_association1)
s.add(tr_association2)
s.add(order1)
s.add(order2)
s.add(order3)

s.commit()

s.close()