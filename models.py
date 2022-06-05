from base import app
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy(app)

dbBind = {'order': 'sqlite:///order.db',
          'ingress': 'sqlite:///ingress.db'}
app.config['SQLALCHEMY_BINDS'] = dbBind

class UserDb(db.Model):
    userId = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # buildingName = db.Column(db.String(50), default=None)
    # unitNumber = db.Column(db.String(200), default=None)
    accountType = db.Column(db.Integer, nullable=False)
    
class OrderDb(db.Model):
    __bind_key__ = 'order'
    orderId = db.Column(db.String(50), primary_key=True)
    customerId = db.Column(db.String(50), nullable=False)
    storeId = db.Column(db.String(50), nullable=False)
    orderDetails = db.Column(db.String(1000), nullable=False) # do we need this since we just doing 1 item per store
    status = db.Column(db.Integer, nullable=False)
    robotID = db.Column(db.String(50))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

class IngressDb(db.Model):
    __bind_key__ = 'ingress'
    postalCode = db.Column(db.Integer, primary_key=True)
    ingressPoint = db.Column(db.String(200), nullable=False)
    
# db.create_all()