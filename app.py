from flask import Flask ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import DATABASE_URI
from datetime import datetime

import traceback
import sys
#import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

######################################################################

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    roomId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    #reserved_dates = Column(ARRAY())
    # sqlalchemy doesnt have composed types so i just used 2 parameters separately
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String, default='Placed') # Placed/Approved
    complete = db.Column(db.Boolean, default=False)

    def __init__(self, id, roomId, userId, start_date, end_date, status = 'Placed', complete = False ):
        self.id = id
        self.roomId = roomId
        self.userId = userId
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.complete = complete

    # def add_user_room(self):
    #     current_user = User.query.filter_by(id=self.userId).first()
    #     rooms_list = current_user.reserved_rooms
    #     rooms_list.append(self.roomId)

    def __repr__(self):
        return "<Order(id={}, roomId={}, userId={}, self.start_date={}, self.end_date={})>" \
            .format(self.id, self.roomId, self.userId, self.start_date, self.end_date)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer)

    name = db.Column(db.String, default='Grand House')

    start_date = db.Column(db.ARRAY(db.DateTime)) # Didn't know how to connect order start/end dates to array of dates in room
    end_date = db.Column(db.ARRAY(db.DateTime))   # So here are just arrays

    def __init__(self, id, category_id, name):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.start_date = []
        self.end_date = []

        #self.start_date.append(start_date)
        #self.end_date.append(end_date)

        print("Check 2")

    def __repr__(self):
        return "<Room(id={}, category_id='{}', name='{}')>" \
            .format(self.id, self.category_id, self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    firstName = db.Column(db.String, default="annoname")
    lastName = db.Column(db.String, default="annoname")
    email = db.Column(db.String, default="annoname")
    phone = db.Column(db.String, default="12345678")
    password = db.Column(db.String, default="qwerty")
    userStatus = db.Column(db.Integer, default="2")
    reserved_rooms = db.Column(db.ARRAY(db.Integer)) # Id's of reserved rooms

    def __repr__(self):
        return "<User(id={}, username='{}', userStatus={})>" \
            .format(self.id, self.username, self.userStatus)

    def __init__(self, id, username, password, firstName = "annoname", lastName = "annoname", email = "annoname", phone = "12345678", userStatus = 2):
        self.id = id
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        # bcrypt.check_password_hash(pw_hash, 'hunter2')  # returns True
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.userStatus = userStatus
        self.reserved_rooms = []


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'firstName', 'lastName', 'email', 'phone', 'userStatus')

# Order Schema
class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'roomId', 'userId', 'start_date', 'end_date', 'status', 'complete')

# Room Schema
class RoomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category_id', 'name', 'start_date', 'end_date')


# Init schema for user
user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)


######################################################################
############## POST ##############
# Create a room
@app.route('/room', methods =['POST'])
def add_room():
    try:
        id = request.json['id']
        category_id = request.json['category_id']
        name = request.json['name']

        # EXAMPLE: 1997-07-16T19:20:30+02:00 -> 16.07.1997 19:20:30
        # OR
        # EXAMPLE: 1997-07-16T19:20:30Z
        # 2012-05-29T19:30:03.283Z
        #start_date = request.json['start_date']
        #datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%m/%d/%y")

        #end_date = request.json['end_date']

        new_room = Room(id, category_id, name)
        print("Check 1")

        db.session.add(new_room)
        #db.session.add(new_category)
        db.session.commit()

        # current_room = Room.query.filter_by(id=id).first()
        # current_start_date = current_room.start_date
        # current_start_date.append([datetime(2020, 12, 14)])
        #
        # current_room.end_date.appepnd(end_date)

        #return jsonify({'message': 'Public ad created successfully'}), 200
        return room_schema.jsonify(new_room), 200
    except Exception:
        db.session.rollback()
        print(traceback.format_exc())
        return jsonify({"message": "Enter all data."}), 400



def add_user_room(userId, roomId):
    current_user = User.query.filter_by(id=userId).first()
    rooms_list = current_user.reserved_rooms
    rooms_list.append(roomId)


@app.route('/order',methods=['POST'])
def add_order():
    try:
        id = request.json['id']
        roomId = request.json['roomId']
        userId = request.json['userId']
        start_date = request.json['start_date']
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_date = request.json['end_date']
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        status = request.json['status']
        complete = request.json['complete']

        new_order = Order(id, roomId, userId, start_date, end_date, status, complete)
        add_user_room(userId, roomId)

        current_room = Room.query.filter_by(id=roomId).first()
        print(current_room)
        current_room.start_date.append(start_date)
        current_room.end_date.append(end_date)

        # EXAMPLE: 1997-07-16T19:20:30+02:00 -> 16.07.1997 19:20:30
        # OR
        # EXAMPLE: 1997-07-16T19:20:30Z
        # 2012-05-29T19:30:03.283Z
        # datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%m/%d/%y")

        print(end_date)

        db.session.add(new_order)
        db.session.commit()

        #return jsonify({'message': 'Order created successfully'}), 200
        return order_schema.jsonify(new_order), 200
    except Exception:
        db.session.rollback()
        print(traceback.format_exc())
        return jsonify({"message": "Invalid input data"}),400

@app.route('/user',methods=['POST'])
def add_user():
    try:
        id = request.json['id']
        username = request.json['username']
        password = request.json['password']
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        phone = request.json['phone']
        userStatus = request.json['userStatus']

        new_user = User(id, username, password, firstName, lastName, email, phone, userStatus)

        db.session.add(new_user)
        db.session.commit()

        #return jsonify({'message': 'User created successfully'}), 200
        return user_schema.jsonify(new_user), 200

    except Exception:
        db.session.rollback()
        print(traceback.format_exc())
        return jsonify({"message": "Enter all data."}), 400

############## GET ##############
### ALL TABLE DATA ###
@app.route('/order',methods=['GET'])
def get_orders():
    try:
        all_orders = Order.query.all()
        result = orders_schema.dump(all_orders)

        return jsonify(result), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

@app.route('/room',methods=['GET'])
def get_rooms():
    try:
        all_rooms = Room.query.all()
        result = rooms_schema.dump(all_rooms)

        return jsonify(result), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

@app.route('/user',methods=['GET'])
def get_users():
    try:
        all_users = User.query.all()
        result = users_schema.dump(all_users)

        return jsonify(result), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

### SINGLE TABLE DATA ###
@app.route('/order/<id>',methods=['GET'])
def get_order(id):
    try:
        order = Order.query.get(id)
        return order_schema.jsonify(order), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

@app.route('/room/<id>',methods=['GET'])
def get_room(id):
    try:
        room = Room.query.get(id)
        return room_schema.jsonify(room)
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Get single user
@app.route('/user/<id>',methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        return user_schema.jsonify(user)
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

############## PUT ##############

@app.route('/room/<id>',methods=['PUT'])
def update_room(id):
    try:
        room = Room.query.get(id)

        room.name = request.json['name']
        room.status = request.json['status']

        db.session.commit()

        #return jsonify({"message":"Public ad ({}) updated successfully".format(publicad.title)}),200

        return room_schema.jsonify(room), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Invalid input"}),405


@app.route('/user/<id>',methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)

        user.username = request.json['username']
        password = request.json['password']
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.firstName = request.json['firstName']
        user.lastName = request.json['lastName']
        user.email = request.json['email']
        user.phone = request.json['phone']
        user.userStatus = request.json['userStatus']

        db.session.commit()
        return user_schema.jsonify(user), 200
        #return jsonify({'message':'User {} updated successfully'.format(user.fullname)}),200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"User not found"}),404

############## DELETE ##############

@app.route('/room/<id>',methods=['DELETE'])
def delete_room(id):
    try:
        room = Room.query.get(id)
        db.session.delete(room)
        db.session.commit()

        return jsonify({'message': 'Room with id({}) was deleted successfully'.format(room.id)}), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Room not found!"}), 404


@app.route('/order/<id>',methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get(id)
        userId = order.userId
        current_user = User.query.filter_by(id=userId).first()

        rooms_list = current_user.reserved_rooms
        rooms_list.remove(order.roomId)

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order with id({}) was deleted successfully'.format(order.id)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Order not found!"}), 404

@app.route('/user/<id>',methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User with id({}) deleted successfully'.format(user.id)}), 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "User not found!"}), 404


# Run Server
if __name__ == '__main__':
    app.run(debug=True)