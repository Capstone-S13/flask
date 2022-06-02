from base import app
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import system

# Account Type
CUSTOMER = 0
STORE = 1

# # Customer Landing Tab
# CUSTOMER_SHOPS = 0
# CUSTOMER_DELIVERY = 1

# # Store Landing Tab
# STORE_INCOMING = 0
# STORE_PREPARING = 1
# STORE_DELIVERY = 2

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

# Login Page
@app.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        loginApprove, userId, accType = system.check_login(request.form['email'], request.form['password'])

        if loginApprove == "approved":
            # check account type (customer or store)
            # push to different home pages
            # cache details somewhere?
            if accType == CUSTOMER:
                return redirect('/customer/{}/landing'.format(userId))
            else:
                return redirect('/store/{}/landing'.format(userId))
        else:
            error = loginApprove
            
    return render_template('login.html', error=error)

# Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        create_status = system.create_acc(request.form['name'], 
                                          request.form['email'], 
                                          request.form['password'], 
                                          request.form['accType'])
        if create_status:
            return redirect('/')
        else:
            return render_template('signup.html')
    return render_template('signup.html')


# Customer Landing Page
@app.route('/customer/<string:userId>/landing', methods=['POST', 'GET'])
def customerLandingPage(userId):
    stores = system.get_all_stores()
    orders = system.get_customer_orders(userId)
    return render_template("customerLanding.html",
                           customerId=userId,
                           stores=stores,
                           orders=orders)

# Customer Creating Order
@app.route('/customer/<string:userId>/create/<string:storeId>')
def create(userId, storeId):
    error = system.create_order(userId, storeId)
    if error:
        return "There was an error creating the order"
    else:
        print("ORDER CREATED!!")
        return redirect("/customer/{}/landing".format(userId))
        

# Customer Viewing Single Order
@app.route('/customer/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
# def order(userId, orderId):
#     order = system.get_order(userId, orderId)
#     return render_template("order.html", order=order, userId=userId)
# Customer Delete Order
# look at delete_order in system
@app.route('/customer/<string:userId>/order/<string:orderId>/delete')
def delete(userId, orderId):
    deleteStatus = system.delete_order(userId, orderId)
    
    # if order_to_delete.customerId == userId:
    #     try:
    #         OrderDb.session.delete(order_to_delete)
    #         OrderDb.session.commit()
    #         return redirect("/customer/{}/landing/{}".format(userId, CUSTOMER_DELIVERY))
    #     except:
    #         return "There was an error deleting the order"
    # else:
    #     return "Order does not belong to user"
    return

# Customer Retrieve Order RobotId (refresh button?)
@app.route('/customer/<string:userId>/order/<string:orderId>/robotId')

# Customer Retrieve Order Status (refresh button?)
@app.route('/customer/<string:userId>/order/<string:orderId>/status')

# Vendor Settings Page
@app.route('/customer/<string:userId>/settings', methods=['POST', 'GET'])
def customerSettings(userId):
    return render_template("customerSettings.html")


# Store Landing Page
@app.route('/store/<string:userId>/landing')
def storeLandingPage(userId):
    orders, incoming, preparing, delivery = system.get_store_orders(userId)
    # print(orders, incoming, preparing, delivery)
    print(incoming)
    return render_template("storeLanding.html",
                           storeId=userId,
                           incoming=incoming,
                           preparing=preparing,
                           delivery=delivery)

# Store Viewing Single Order Page
@app.route('/store/<string:userId>/order/<string:orderId>', methods=['POST', 'GET'])
# def order(userId, orderId):
#     order = system.get_order(userId, orderId)
#     return render_template("order.html", order=order, userId=userId)
########################### Create Order HTML #########################################

# Store Reject Order
@app.route('/store/<string:userId>/order/<string:orderId>/delete')
def reject(userId, orderId):
    deleteStatus = system.delete_order(userId, orderId)
    
    # if order_to_delete.storeId == userId:
    #     try:
    #         OrderDb.session.delete(order_to_delete)
    #         OrderDb.session.commit()
    #         return redirect("/store/{}/landing".format(userId))
    #     except:
    #         return "There was an error deleting the order"
    # else:
    #     return "Order does not belong to user"
    return render_template("storeLanding.html")

# Update Order (Status)
@app.route('/store/<string:userId>/order/<string:orderId>/<int:status>')
def set_status(userId, orderId, status):
    statusUpdateStatus = system.set_order_status(userId, orderId, status)
    
    if statusUpdateStatus == "success":
        return redirect('/store/{}/landing'.format(userId))
    else:
        return statusUpdateStatus

# Vendor Settings Page
@app.route('/store/<string:userId>/settings', methods=['POST', 'GET'])
def storeSettings(userId):
    return render_template("storeSettings.html")


# Logout
# @app.route("/logout")
# @login_required
# def logout():
#     base.flask_login.logout_user()
#     return redirect("/")
    

    
if __name__== "__main__":
    app.run(debug=True)