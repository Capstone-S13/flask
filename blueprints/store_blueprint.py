# from base import app
from . import STORE_BLUEPRINT
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
<<<<<<<< HEAD:blueprints/store_blueprint.py
from datetime import datetime
import system as system
========
import application.system as system
>>>>>>>> ec20b0dbc267e97964075e15918374dde319feca:application/store/views.py

# Account Type
CUSTOMER = 0
STORE = 1

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

############################
#### Store Landing Page ####
############################

@STORE_BLUEPRINT.route('/landing')
@login_required
def landing():
    customerNames, incoming, preparing, delivery = system.get_store_orders(current_user.id)
<<<<<<<< HEAD:blueprints/store_blueprint.py
    # print(customerNames)
    # print(incoming)
    # print(preparing)
    # print(delivery)
    return render_template("storeLanding.html",
========
    print(customerNames)
    print(incoming)
    print(preparing)
    print(delivery)
    return render_template("store/storeLanding.html",
>>>>>>>> ec20b0dbc267e97964075e15918374dde319feca:application/store/views.py
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
        print(request.form["order_button"])
        error = system.set_order_status(current_user.id,
                                        orderId,
                                        request.form['order_button'])
        if error:
            print("There was an error updating order status")
            print(error)
            return redirect(url_for('store.landing'))
        print("ORDER UPDATED!!")
        return redirect(url_for('store.landing'))

# Store Viewing Single Order Page
# @STORE_BLUEPRINT.route(/<string:current_user.id>/order/<string:orderId>', methods=['POST', 'GET'])
# @login_required
# def order(orderId):
#     order = system.get_order(current_user.id, orderId)
#     return render_template("order.html", order=order, current_user.id=current_user.id)

#############################
#### Store Settings Page ####
#############################

@STORE_BLUEPRINT.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        error = system.update_user(current_user.id,
                                    request.form["name"],
                                    request.form["email"],
                                    request.form["postalCode"],
                                    request.form["unit"])
        if error:
            print("error updating user details")
            return render_template("store/storeSettings.html", user=current_user)
        print("Details Updated")
        return redirect(url_for('store.landing'))
    return render_template("store/storeSettings.html", user=current_user)