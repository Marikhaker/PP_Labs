### models.py ###
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, ARRAY, Boolean, DateTime, ForeignKey, Table

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    roomId = Column(Integer)
    userId = Column(Integer)
    # sqlalchemy doesnt have composed types so i just used 2 parameters separately
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default='Placed') # Placed/Approved
    complete = Column(Boolean, default=False)


    def __repr__(self):
        return "<Order(id={}, roomId={}, userId={}, self.start_date={}, self.end_date={})>" \
            .format(self.id, self.roomId, self.userId, self.start_date, self.end_date)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, default='Grand House')

    category_id = Column(Integer)

    start_date = Column(ARRAY(DateTime)) # Didn't know how to connect order start/end dates to array of dates in room
    end_date = Column(ARRAY(DateTime))   # So here are just arrays

    def __repr__(self):
        return "<Room(id={}, category_id={}, name='{}')>" \
            .format(self.id, self.name, self.category_id)

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


