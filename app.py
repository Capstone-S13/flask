from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
import system

# Account Type
CUSTOMER = 0
STORE = 1

# Customer Landing Tab
CUSTOMER_SHOPS = 0
CUSTOMER_DELIVERY = 1

# Store Landing Tab
STORE_INCOMING = 0
STORE_PREPARING = 1
STORE_DELIVERY = 2

# Order Statuses
ORDER_RECEIVED = 0
ROBOT_DISPATCHED = 1
AT_STORE_HUB = 2
BETWEEN_HUBS = 3
AT_DEST_HUB = 4
ARRIVED = 5
DELIVERED = 6
CANCELLED = 7
FAILED = 8

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
dbBind = {'order': 'sqlite:///order.db',
          'ingress': 'sqlite:///ingress.db'}
app.config['SQLALCHEMY_BINDS'] = dbBind
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserDb(db.Model):
    userId = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    buildingName = db.Column(db.String(50), nullable=False)
    unitNumber = db.Column(db.String(200), nullable=False)
    accountType = db.Column(db.Integer, nullable=False)
    
class OrderDb(db.Model):
    __bind_key__ = 'order'
    orderId = db.Column(db.String(50), primary_key=True)
    customerId = db.Column(db.String(50), nullable=False)
    storeId = db.Column(db.String(50), nullable=False)
    orderDetails = db.Column(db.String(1000), nullable=False) # do we need this since we just doing 1 item per store
    status = db.Column(db.Integer, nullable=False)
    robotID = db.Column(db.String(50))

class IngressDb(db.Model):
    __bind_key__ = 'ingress'
    postalCode = db.Column(db.Integer, primary_key=True)
    ingressPoint = db.Column(db.String(200), nullable=False)
    
# Login Page
@app.route('/', methods = ['GET', 'POST'])
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

# Customer Landing Page
@app.route('/customer/<string:userId>/landing/<int:landingTab>', methods=['GET'])
def customerLandingPage(userId, landingTab):
    browse = UserDb.filter_by(accountType=STORE) # system.get_all_stores()
    orders = OrderDb.filter_by(customerId=userId) # system.get_orders(userId)
    return render_template("customerLanding.html", browse=browse, orders=orders, landingTab=landingTab)

# Customer Creating Order
@app.route('/customer/<string:userId>/create/<string:storeId>')
def create(userId, storeId):
    # system.create_order(userId, storeId)
    orderId = uuid4()
    new_order = OrderDb(orderId=orderId, customerId=userId, storeId=storeId, status=ORDER_RECEIVED)
    
    try:
        OrderDb.session.add(new_order)
        OrderDb.session.commit()
        return redirect("/customer/{}/landing/{}".format(userId, CUSTOMER_SHOPS))
    except:
        return "There was an error creating the order"

# Customer Viewing Single Order
@app.route('/customer/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
# def order(userId, orderId):
#     order = OrderDb.query.get_or_404(orderId)
#     return render_template("order.html", order=order, userId=userId)

# Customer Delete Order
@app.route('/customer/<string:userId>/order/<string:orderId>/delete')
# def delete(userId, orderId):
#     order_to_delete = OrderDb.query.get_or_404(orderId)
    
#     if order_to_delete.customerId == userId:
#         try:
#             OrderDb.session.delete(order_to_delete)
#             OrderDb.session.commit()
#             return redirect("/customer/{}/landing/{}".format(userId, CUSTOMER_DELIVERY))
#         except:
#             return "There was an error deleting the order"
#     else:
#         return "Order does not belong to user"

# Customer Retrieve Order RobotId (refresh button?)
@app.route('/customer/<string:userId>/order/<string:orderId>/robotId')

# Customer Retrieve Order Status (refresh button?)
@app.route('/customer/<string:userId>/order/<string:orderId>/status')



# Store Landing Page
@app.route('/store/<string:userId>/landing/<int:landingTab>')
def storeLandingPage(userId, landingTab):    
    orders = OrderDb.filter_by(storeId=userId)
    return render_template("storeLanding.html", orders=orders, landingTab=landingTab)

# Store Viewing Single Order Page
@app.route('/store/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
def order(userId, orderId):
    order = OrderDb.query.get_or_404(orderId)
    return render_template("order.html", order=order, userId=userId)
########################### Create Order HTML #########################################

# Store Reject Order
@app.route('/store/<string:userId>/order/<string:orderId>/delete')
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

# Update Order (Status)
@app.route('/store/<string:userId>/order/<string:orderId>/<int:status>')
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
    
    
if __name__== "__main__":
    app.run(debug=True)