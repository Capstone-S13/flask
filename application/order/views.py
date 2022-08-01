from . import ORDER_BLUEPRINT
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
# from flask_security import login_required, current_user
import application.system as system

# Account Type
CUSTOMER = 0
STORE = 1

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
WAITING_FOR_PARCEL = "Waiting for Parcel"
STORING_IN_STORE_HUB = "Storing in Store Hub"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
DELIVERING_TO_DOORSTEP = "Delivering to Doorstep"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

status_lst = ["Order Sent", "Order Received", "Robot Dispatched", "Waiting for Parcel", "Storing in Store Hub", "At Store Hub", "Between Hubs", "At Destination Hub", "Delivering to Doorstep", "Arrived", "Delivered", "Cancelled", "Failed"]

@ORDER_BLUEPRINT.route('/all')
def all_orders():
    all_orders = system.get_all_orders()
    return render_template("order/order.html", all_orders=all_orders)

@ORDER_BLUEPRINT.route('/<string:orderId>', methods=['GET', 'POST'])
def single_order(orderId):
    if request.method == "POST":
        system.robot_set_order_status(orderId, request.form['status_button'])
        return redirect(url_for('order.all_orders'))
    return render_template("order/single_order.html", orderId=orderId, status_lst=status_lst)