from . import CUSTOMER_BLUEPRINT
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
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

###############################
#### Customer Landing Page ####
###############################

@CUSTOMER_BLUEPRINT.route('/landing', methods=['GET'])
@login_required
def landing():
    stores = system.get_all_stores()
    storeNames, delivery, waypoints = system.get_customer_orders(current_user.id)

    print(delivery)
    return render_template("customer/customerLanding.html",
                           customerId=current_user.id,
                           stores = stores,
                           storeNames=storeNames,
                           delivery=delivery,
                           waypoints = waypoints)

# Customer Creating Order
@CUSTOMER_BLUEPRINT.route('/create/<string:storeId>')
@login_required
def create(storeId):
    error = system.create_order(current_user.id, storeId)
    if error:
        return "There was an error creating the order"
    else:
        print("ORDER CREATED!!")
        # flash("order successfully created", 'info')
        return redirect(url_for('customer.landing'))
        

@CUSTOMER_BLUEPRINT.route('/order/<string:orderId>', methods=['GET', 'POST'])
@login_required
def order(orderId):
    if request.method == "POST":
        new_status = request.form["order_button"]
        print(new_status)
        error = system.set_order_status(current_user.id,
                                        orderId,
                                        new_status)
        if error:
            print("There was an error updating order status")
            print(error)
            return redirect(url_for('customer.landing'))
        print("ORDER UPDATED!!")
        return redirect(url_for('customer.landing'))

@CUSTOMER_BLUEPRINT.route('/order/waypoint/<string:orderId>', methods=['POST'])
@login_required
def set_waypoint(orderId):
    if request.method == "POST":
        new_waypoint = request.form["waypoint_button"]
        print(new_waypoint)
        system.set_new_waypoint(orderId, new_waypoint)
        return redirect(url_for('customer.landing'))
    return redirect(url_for('customer.landing'))

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

################################
#### Customer Settings Page ####
################################

@CUSTOMER_BLUEPRINT.route('/settings', methods=['GET', 'POST'])
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
            return render_template("customer/customerSettings.html", user=current_user)
        print("Details Updated")
        return redirect(url_for('customer.landing'))
    return render_template("customer/customerSettings.html", user=current_user)