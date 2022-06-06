# from base import app
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

STORE_BLUEPRINT = Blueprint('store_blueprint', __name__)

# Store Landing Page
@STORE_BLUEPRINT.route('/<string:userId>/landing')
def storeLandingPage(userId):
    customerNames, incoming, preparing, delivery = system.get_store_orders(userId)
    print(customerNames)
    print(incoming)
    print(preparing)
    return render_template("storeLanding.html",
                           storeId=userId,
                           customerNames = customerNames,
                           incoming=incoming,
                           preparing=preparing,
                           delivery=delivery)

# Store Update Order Status
@STORE_BLUEPRINT.route('/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
def order(userId, orderId):
    
    if request.method == "POST":
        print(request.form['order_button'])
        updateStatus = system.set_order_status(userId, orderId, int(request.form['order_button']))
        print(updateStatus)
        if updateStatus == "success":
            print("ORDER UPDATED!!")
            return redirect("/{}/landing".format(userId))
    print("There was an error updating order status")
    return redirect("/{}/landing".format(userId))


# Store Viewing Single Order Page
# @STORE_BLUEPRINT.route(/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
# def order(userId, orderId):
#     order = system.get_order(userId, orderId)
#     return render_template("order.html", order=order, userId=userId)
########################### Create Order HTML #########################################

# Store Reject Order
# @STORE_BLUEPRINT.route('/<string:userId>/order/<string:orderId>/delete')
# def reject(userId, orderId):
#     deleteStatus = system.delete_order(userId, orderId)
    
    # if order_to_delete.storeId == userId:
    #     try:
    #         OrderDb.session.delete(order_to_delete)
    #         OrderDb.session.commit()
    #         return redirect("/{}/landing".format(userId))
    #     except:
    #         return "There was an error deleting the order"
    # else:
    #     return "Order does not belong to user"
    # return render_template("storeLanding.html")

# Update Order (Status)
@STORE_BLUEPRINT.route('/<string:userId>/order/<string:orderId>/<int:status>')
def set_status(userId, orderId, status):
    statusUpdateStatus = system.set_order_status(userId, orderId, status)
    
    if statusUpdateStatus == "success":
        return redirect('/{}/landing'.format(userId))
    else:
        return statusUpdateStatus

# Vendor Settings Page
@STORE_BLUEPRINT.route('/<string:userId>/settings', methods=['POST', 'GET'])
def storeSettings(userId):
    user = system.get_vendor_details(userId)
    print(user.keys())
    return render_template("storeSettings.html", user=user, vendorId=userId)