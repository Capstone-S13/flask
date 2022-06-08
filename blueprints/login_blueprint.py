from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from datetime import datetime
import system as system

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

LOGIN_BLUEPRINT = Blueprint('login_blueprint', __name__)

# Login Page
@LOGIN_BLUEPRINT.route('/')
def login():
    
    return render_template('login.html')

@LOGIN_BLUEPRINT.route('/', methods=['POST'])
def login_post():
    error = None
    if request.method == 'POST':
        loginApprove, user = system.check_login(request.form['email'], request.form['password'])

        if loginApprove == "approved":
            login_user(user)
            if user.accountType == CUSTOMER:
                return redirect('/customer/landing')
            else:
                return redirect('/store/landing')
        else:
            return redirect('/')
        
# Sign Up Page
@LOGIN_BLUEPRINT.route('/signup')
def signup():
    
    return render_template('signup.html')

@LOGIN_BLUEPRINT.route('/signup', methods=['POST'])
def signup_post():
    if request.method == 'POST':
        create_status = system.create_acc(request.form['name'], 
                                          request.form['email'], 
                                          request.form['password'],
                                          request.form['postalCode'],
                                          request.form['unit'], 
                                          request.form['accType'])
        if create_status:
            return redirect('/')
        
        print(create_status)
        return render_template('signup.html')
        
@LOGIN_BLUEPRINT.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')