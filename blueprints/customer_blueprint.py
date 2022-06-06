from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
# from flask_login import LoginManager, login_user
# from flask_login_multi.login_manager import LoginManager
from datetime import datetime
import system

# Account Type
CUSTOMER = 0
STORE = 1

# Order Statuses
ORDER_SENT = 0
ORDER_RECEIVED = 1
ROBOT_DISPATCHED = 2
AT_STORE_HUB = 3
BETWEEN_HUBS = 4
AT_DEST_HUB = 5
ARRIVED = 6
DELIVERED = 7
CANCELLED = 8
FAILED = 9

CUSTOMER_BLUEPRINT = Blueprint('customer_blueprint', __name__)

# Customer Landing Page
@CUSTOMER_BLUEPRINT.route('/<string:userId>/landing', methods=['POST', 'GET'])
def customerLandingPage(userId):
    stores = system.get_all_stores()
    storeNames, delivery = system.get_customer_orders(userId)
    print(delivery)
    return render_template("customerLanding.html",
                           customerId=userId,
                           stores = stores,
                           storeNames=storeNames,
                           delivery=delivery)

# Customer Creating Order
@CUSTOMER_BLUEPRINT.route('/<string:userId>/create/<string:storeId>')
def create(userId, storeId):
    error = system.create_order(userId, storeId)
    if error:
        return "There was an error creating the order"
    else:
        print("ORDER CREATED!!")
        # flash("order successfully created", 'info')
        return redirect("/{}/landing".format(userId))
        

# Customer Viewing Single Order
@CUSTOMER_BLUEPRINT.route('/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
# def order(userId, orderId):
#     order = system.get_order(userId, orderId)
#     return render_template("order.html", order=order, userId=userId)

# Customer Delete Order
# look at delete_order in system
@CUSTOMER_BLUEPRINT.route('/<string:userId>/order/<string:orderId>/delete')
def delete(userId, orderId):
    deleteStatus = system.delete_order(userId, orderId)
    # flash('order deleted', 'info')
    
    # if order_to_delete.customerId == userId:
    #     try:
    #         OrderDb.session.delete(order_to_delete)
    #         OrderDb.session.commit()
    #         return redirect("/{}/landing/{}".format(userId, CUSTOMER_DELIVERY))
    #     except:
    #         return "There was an error deleting the order"
    # else:
    #     return "Order does not belong to user"
    return

# Customer Retrieve Order RobotId (refresh button?)
# @CUSTOMER_BLUEPRINT.route('/<string:userId>/order/<string:orderId>/robotId')

# Customer Retrieve Order Status (refresh button?)
# @CUSTOMER_BLUEPRINT.route('/<string:userId>/order/<string:orderId>/status')

# Customer Settings Page
@CUSTOMER_BLUEPRINT.route('/<string:userId>/settings', methods=['POST', 'GET'])
def customerSettings(userId):
    return render_template("customerSettings.html")