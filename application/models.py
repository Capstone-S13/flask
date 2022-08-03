# from base import app
from flask_sqlalchemy import SQLAlchemy
# from flask_security import UserMixin
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

dbBind = {'order': 'sqlite:///database/order.db',
          'ingress': 'sqlite:///database/ingress.db',
          'task': 'sqlite:///database/task.db',
          'robot': 'sqlite:///database/robot.db'}

class UserDb(UserMixin, db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    postalCode = db.Column(db.Integer, nullable=False)
    unitNumber = db.Column(db.String(50), nullable=False)
    accountType = db.Column(db.Integer, nullable=False)
    # active = db.Column(db.Boolean(), default=False)
    
class OrderDb(db.Model):
    __bind_key__ = 'order'
    orderId = db.Column(db.String(100), primary_key=True)
    customerId = db.Column(db.String(100), nullable=False)
    customerPostalCode = db.Column(db.Integer, nullable=False)
    customerUnitNumber = db.Column(db.String(50), nullable=False)
    storeId = db.Column(db.String(100), nullable=False)
    storePostalCode = db.Column(db.Integer, nullable=False)
    storeUnitNumber = db.Column(db.String(50), nullable=False)
    orderDetails = db.Column(db.String(1000), nullable=False) # do we need this since we just doing 1 item per store
    status = db.Column(db.String(100), nullable=False)
    robotID = db.Column(db.String(100))
    dateCreated = db.Column(db.DateTime, default=datetime.now)

class IngressDb(db.Model):
    __bind_key__ = 'ingress'
    ingressId = db.Column(db.String(100), primary_key=True)
    postalCode = db.Column(db.Integer, nullable=False)
    unitNumber = db.Column(db.String(50), nullable=False)
    waypoint = db.Column(db.String(200))
    # ip and port
    ip = db.Column(db.String(100))
    port = db.Column(db.String(20))
    # map
    image = db.Column(db.String(10000))
    resolution = db.Column(db.String(1000))
    origin = db.Column(db.String(10000))
    negate = db.Column(db.Integer)
    occupied_thresh = db.Column(db.String(1000))
    free_thresh = db.Column(db.String(1000))
    pgm = db.Column(db.String(1000000))

class TaskDb(db.Model):
    __bind_key__ = "task"
    taskId = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    orderId = db.Column(db.String(100), nullable=False)
    robotId = db.Column(db.String(100))

class RobotDb(db.Model):
    __bind_key__ = "robot"
    robotId = db.Column(db.String(100), primary_key=True)
    availability = db.Column(db.Integer, nullable=False)

# db.create_all()