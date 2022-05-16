from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

CUSTOMER = 0
STORE = 1

CUSTOMER_SHOPS = 0
CUSTOMER_DELIVERY = 1

STORE_INCOMING = 0
STORE_PREPARING = 1
STORE_DELIVERY = 2

ORDER_RECEIVED = 0
ROBOT_DISPATCHED = 1
AT_STORE_HUB = 2
BETWEEN_HUBS = 3
AT_LOCAL_HUB = 4
ARRIVED = 5
DELIVERED = 6
CANCELLED = 7
FAILED = 8

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# dbBind = {'order': 'sqlite:///order.db',
#           'ingress': 'sqlite:///ingress.db'}
# app.config['SQLALCHEMY_BINDS'] = dbBind

db = SQLAlchemy(app)

class UserDb(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    postalCode = db.Column(db.Integer, nullable=False)
    unitNumber = db.Column(db.String(200), nullable=False)
    accountType = db.Column(db.Integer, nullable=False)
    
class OrderDb(db.Model):
    __bind_key__ = 'order'
    orderId = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, nullable=False)
    storeId = db.Column(db.Integer, nullable=False)
    orderDetails = db.Column(db.String(1000), nullable=False) # do we need this since we just doing 1 item per store
    status = db.Column(db.Integer, nullable=False)
    robotID = db.Column(db.Integer)

class IngressDb(db.Model):
    __bind_key__ = 'ingress'
    postalCode = db.Column(db.Integer, primary_key=True)
    ingressPoint = db.Column(db.String(200), nullable=False)
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        userAcc = UserDb.query.get_or_404(request.form['email'])
        if request.form['password'] != userAcc.password:
            error = 'Invalid Password. Please try again.'
        else:
            # check account type (customer or store)
            # push to different home pages
            # cache details somewhere?
            if userAcc.accountType == CUSTOMER:
                return redirect('/customer/{}/landing/{}'.format(userAcc.userId, CUSTOMER_SHOPS))
            else:
                return redirect('/store/{}/landing/{}'.format(userAcc.userId, STORE_INCOMING))
    return render_template('login.html', error=error)

@app.route('/customer/<int:userId>/landing/<int:landingTab>', methods=['POST','GET'])
#customer landing page
def customerLandingPage(userId, landingTab):    
    browse = UserDb.filter_by(accountType=STORE)
    orders = OrderDb.filter_by(customerId=userId)
    return render_template("customerLanding.html", browse=browse, orders=orders, landingTab=landingTab)

@app.route('/customer/<int:userId>/create/<int:storeId>')
# creating order
def create(userId, storeId):
    orderId = uuid4().int
    new_order = OrderDb(orderId=orderId, customerId=userId, storeId=storeId, status=ORDER_RECEIVED)
    
    try:
        OrderDb.session.add(new_order)
        OrderDb.session.commit()
        return redirect("/customer/{}/landing/{}".format(userId, CUSTOMER_SHOPS))
    except:
        return "There was an error creating the order"

@app.route('/customer/<int:userId>/order/<int:orderId>', methods=['POST', 'GET'])
# viewing single order page
def order(userId, orderId):
    order = OrderDb.query.get_or_404(orderId)
    return render_template("order.html", order=order, userId=userId)
    
@app.route('/customer/<int:userId>/order/<int:orderId>/delete')
# delete order
def delete(userId, orderId):
    order_to_delete = OrderDb.query.get_or_404(orderId)
    
    if order_to_delete.customerId == userId:
        try:
            OrderDb.session.delete(order_to_delete)
            OrderDb.session.commit()
            return redirect("/customer/{}/landing/{}".format(userId, CUSTOMER_DELIVERY))
        except:
            return "There was an error deleting the order"
    else:
        return "Order does not belong to user"

@app.route('/customer/<int:userId>/order/<int:orderId>/robotId')
# retrieve order's robotId

@app.route('/customer/<int:userId>/order/<int:orderId>/status')
# retrieve order status



@app.route('/store/<int:userId>/landing/<int:landingTab>')
# store landing page
def storeLandingPage(userId, landingTab):    
    orders = OrderDb.filter_by(storeId=userId)
    return render_template("storeLanding.html", orders=orders, landingTab=landingTab)

@app.route('/store/<int:userId>/order/<int:orderId>', methods=['POST', 'GET'])
# viewing single order page
def order(userId, orderId):
    order = OrderDb.query.get_or_404(orderId)
    return render_template("order.html", order=order, userId=userId)

@app.route('/store/<int:userId>/order/<int:orderId>/delete')
# reject order
def delete(userId, orderId):
    order_to_delete = OrderDb.query.get_or_404(orderId)
    
    if order_to_delete.storeId == userId:
        try:
            OrderDb.session.delete(order_to_delete)
            OrderDb.session.commit()
            return redirect("/store/{}/landing/{}".format(userId, STORE_INCOMING))
        except:
            return "There was an error deleting the order"
    else:
        return "Order does not belong to user"

@app.route('/store/<int:userId>/order/<int:orderId>/<int:status>')
# update order (status)
def set_status(userId, orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)
    order_to_update.status = status
    
    if order_to_update.storeId == userId:
        try:
            OrderDb.session.commit()
            return redirect('/store/{}/landing/{}'.format(userId, STORE_INCOMING))
        except:
            return "There was an error updating the order status"
    else:
        return "Order does not belong to user"