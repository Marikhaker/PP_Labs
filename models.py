### models.py ###
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, ARRAY, Boolean, DateTime, ForeignKey, Table

Base = declarative_base()

# tags_table = Table('room_tag_table', Base.metadata,
#     Column('room_id', Integer, ForeignKey('rooms.id')),
#     Column('tag_id', Integer, ForeignKey('tags.id'))
#     #Column('tag name', String, ForeignKey('tags.name'))
# )

class tag_room_association(Base):
    __tablename__ = 'tag_room_associations'
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    #extra_data = Column(String(50))
    tag_relation = relationship("Tag", back_populates="room_relation")
    room_relation = relationship("Room", back_populates="tag_relation")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    roomId = Column(Integer)
    userId = Column(Integer)
    #reserved_dates = Column(ARRAY())
    # sqlalchemy doesnt have composed types so i just used 2 parameters separately
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default='Placed') # Placed/Approved
    complete = Column(Boolean, default=False)

    # def __init__(self):
    #     super.__init__(__tablename__ = 'orders',
    #                    id=Column(Integer, primary_key=True),
    #                    roomId=Column(Integer),
    #                    userId = Column(Integer),
    #                    start_date = Column(DateTime),
    #                    end_date = Column(DateTime),
    #                    status = Column(String, default='Placed'),  # Placed/Approved
    #                    complete = Column(Boolean, default=False)
    #     )
    #     self.add_user_room(self)


    # def add_user_room(self):
    #     current_user = User.query.filter_by(id=self.userId).first()
    #     rooms_list = current_user.reserved_rooms
    #     rooms_list.append(self.roomId)

    def __repr__(self):
        return "<Order(id={}, roomId={}, userId={}, self.start_date={}, self.end_date={})>" \
            .format(self.id, self.roomId, self.userId, self.start_date, self.end_date)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category_relation = relationship("Category", uselist=False, back_populates="room_relation")#, default="Basic room")
    name = Column(String, default='Grand House')
    #tags_id = Column(ARRAY(Integer, ForeignKey('tags.id')))
    #tags_id = Column(Integer, ForeignKey('tags.id'))

    tag_relation = relationship("tag_room_association", back_populates="room_relation")#, default="Small")
    start_date = Column(ARRAY(DateTime)) # Didn't know how to connect order start/end dates to array of dates in room
    end_date = Column(ARRAY(DateTime))   # So here are just arrays

    def __repr__(self):
        return "<Room(id={}, category='{}', name='{}')>" \
            .format(self.id, self.category, self.name)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    firstName = Column(String, default="annoname")
    lastName = Column(String, default="annoname")
    email = Column(String, default="annoname")
    phone = Column(String, default="annoname")
    password = Column(String, default="qwerty")
    userStatus = Column(Integer, default="2")
    reserved_rooms = Column(ARRAY(Integer)) # Id's of reserved rooms

    def __repr__(self):
        return "<User(id={}, username='{}', userStatus={})>" \
            .format(self.id, self.username, self.userStatus)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    #room_id = Column(Integer, ForeignKey('rooms.id'))
    room_relation = relationship("Room", back_populates="category_relation")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, default="default tag")
    #room_id = Column(Integer, ForeignKey('rooms.id'))
    room_relation = relationship("tag_room_association", back_populates="tag_relation")

