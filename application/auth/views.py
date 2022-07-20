from flask import render_template, url_for, request, redirect, flash, current_app
from flask_login import login_user, login_required, logout_user

from . import AUTH_BLUEPRINT
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
