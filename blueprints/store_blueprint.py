# from base import app
from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
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
@STORE_BLUEPRINT.route('/landing')
@login_required
def storeLandingPage():
    customerNames, incoming, preparing, delivery = system.get_store_orders(current_user.id)
    print(customerNames)
    print(incoming)
    print(preparing)
    print(delivery)
    return render_template("storeLanding.html",
                           storeId=current_user.id,
                           customerNames = customerNames,
                           incoming=incoming,
                           preparing=preparing,
                           delivery=delivery)

# Store Update Order Status
@STORE_BLUEPRINT.route('/order/<string:orderId>', methods=['GET', 'POST'])
@login_required
def order(orderId):
    if request.method == "POST":
        print(request.form['order_button'])
        updateStatus = system.set_order_status(current_user.id, orderId, int(request.form['order_button']))
        print(updateStatus)
        if updateStatus == "success":
            print("ORDER UPDATED!!")
            return redirect("/store/landing")
    print("There was an error updating order status")
    return redirect("/store/landing")


# Store Viewing Single Order Page
# @STORE_BLUEPRINT.route(/<string:current_user.id>/order/<string:orderId>', methods=['POST', 'GET'])
# @login_required
# def order(orderId):
#     order = system.get_order(current_user.id, orderId)
#     return render_template("order.html", order=order, current_user.id=current_user.id)


# Vendor Settings Page
@STORE_BLUEPRINT.route('/settings', methods=['GET', 'POST'])
@login_required
def storeSettings():
    user = system.get_vendor_details(current_user.id)
    
    if request.method == 'POST':
        # do something
        pass    
    
    return render_template("storeSettings.html", user=user, vendorId=current_user.id)