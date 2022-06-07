from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from datetime import datetime
import system as system

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