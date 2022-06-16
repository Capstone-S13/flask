from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from datetime import datetime
import application.system as system

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

CUSTOMER_BLUEPRINT = Blueprint('customer_blueprint', __name__)

# Customer Landing Page
@CUSTOMER_BLUEPRINT.route('/landing', methods=['GET'])
@login_required
def customerLandingPage():
    stores = system.get_all_stores()
    storeNames, delivery = system.get_customer_orders(current_user.id)
    return render_template("customerLanding.html",
                           customerId=current_user.id,
                           stores = stores,
                           storeNames=storeNames,
                           delivery=delivery)

# Customer Creating Order
@CUSTOMER_BLUEPRINT.route('/create/<string:storeId>')
@login_required
def create(storeId):
    status = system.create_order(current_user.id, storeId)
    if status:
        print("ORDER CREATED!!")
        # flash("order successfully created", 'info')
        return redirect("/customer/landing") 
    return "There was an error creating the order"
        

# Customer Viewing Single Order
# @CUSTOMER_BLUEPRINT.route('/order/<string:orderId>', methods=['POST', 'GET'])
# @login_required
# def order(orderId):
#     order = system.get_order(orderId)
#     return render_template("order.html", order=order, id=current_user.id)

# Customer Delete Order
# look at delete_order in system
# @CUSTOMER_BLUEPRINT.route('/order/<string:orderId>/delete')
# @login_required
# def delete(orderId):
#     deleteStatus = system.delete_order(current_user.id, orderId)
    # flash('order deleted', 'info')
    
    # if order_to_delete.customerId == current_user.id:
    #     try:
    #         OrderDb.session.delete(order_to_delete)
    #         OrderDb.session.commit()
    #         return redirect("/customer/landing")
    #     except:
    #         return "There was an error deleting the order"
    # else:
    #     return "Order does not belong to user"
    # return

# Customer Retrieve Order RobotId (refresh button?)
# @CUSTOMER_BLUEPRINT.route('/order/<string:orderId>/robotId')
# @login_required

# Customer Retrieve Order Status (refresh button?)
# @CUSTOMER_BLUEPRINT.route('/order/<string:orderId>/status')
# @login_required

# Customer Settings Page
@CUSTOMER_BLUEPRINT.route('/settings', methods=['GET', 'POST'])
@login_required
def customerSettings():
    if request.method == 'POST':
        userUpdateStatus = system.update_user(current_user.id,
                                                request.form["name"],
                                                request.form["email"],
                                                request.form["postalCode"],
                                                request.form["unit"])
        if userUpdateStatus:
            print("Details Updated")
            return redirect("/customer/landing")
        print("error updating user details")
        return render_template("customerSettings.html", user=current_user)
    return render_template("customerSettings.html", user=current_user)