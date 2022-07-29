from flask import render_template, url_for, request, redirect, flash, current_app
from flask_login import login_user, login_required, logout_user
# from flask_security import login_user, login_required, logout_user

from . import AUTH_BLUEPRINT
import application.system as system

# Account Type
CUSTOMER = 0
STORE = 1

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
WAITING_FOR_PARCEL = "Waiting for Parcel"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
DELIVERING_TO_DOORSTEP = "Delivering to Doorstep"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

# statuses = {"Order Sent":0,
#             "Order Received":1,
#             "Robot Dispatched":2,
#             "At Store Hub":3,
#             "Between Hubs":4,
#             "At Destination Hub":5,
#             "Delivering to Doorstep":6,
#             "Arrived":7,
#             "Delivered":8,
#             "Cancelled":9,
#             "Failed":10}

# Task Operations
TASK_DELIVER_TO_HUB = 0
TASK_COLLECT_FROM_HUB = 1
TASK_GO_TO_UNIT = 2

# Task Statuses
STATUS_TASK_COLLECTING_FROM_STORE = 0
STATUS_TASK_WAITING_OUTSIDE_STORE = 1
STATUS_TASK_COLLECTED_FROM_STORE = 2
STATUS_TASK_REQUESTING_EXT_ROBOT = 3
STATUS_TASK_EXT_ROBOT_DISPATCHED = 4
STATUS_TASK_COLLECTING_FROM_STORE_HUB = 5
STATUS_TASK_SENT_TO_STORE_EGRESS = 6
STATUS_TASK_DELIVERING = 7
STATUS_TASK_RECEIVED = 8

####################
#### Login Page ####
####################

@AUTH_BLUEPRINT.route('/')
def login():
    return render_template('auth/login.html')

@AUTH_BLUEPRINT.route('/', methods=['POST'])
def login_post():
    if request.method == 'POST':
        loginApprove, user = system.check_login(request.form['email'], request.form['password'])

        if loginApprove == "approved":
            login_user(user)
            if user.accountType == CUSTOMER:
                return redirect(url_for('customer.landing'))
            else:
                return redirect(url_for('store.landing'))
        else:
            return redirect(url_for('auth.login'))

######################
#### Sign Up Page ####
######################

@AUTH_BLUEPRINT.route('/signup')
def signup():
    return render_template('auth/signup.html')

@AUTH_BLUEPRINT.route('/signup', methods=['POST'])
def signup_post():
    if request.method == 'POST':
        error = system.create_acc(request.form['name'], 
                                request.form['email'], 
                                request.form['password'],
                                request.form['postalCode'],
                                request.form['unit'], 
                                request.form['accType'])
        if error:
            print(error)
            return redirect(url_for('auth.signup'))
        return redirect(url_for('auth.login'))

################
#### Logout ####
################

@AUTH_BLUEPRINT.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))