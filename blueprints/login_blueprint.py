from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
# from flask_login import LoginManager, login_user
# from flask_login_multi.login_manager import LoginManager
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

LOGIN_BLUEPRINT = Blueprint('login_blueprint', __name__)

# Login Page
@LOGIN_BLUEPRINT.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        loginApprove, userId, accType = system.check_login(request.form['email'], request.form['password'])

        if loginApprove == "approved":
            # check account type (customer or store)
            # push to different home pages
            # cache details somewhere?
            # login_user(UserDb)
            if accType == CUSTOMER:
                return redirect('/customer/{}/landing'.format(userId))
            else:
                return redirect('/store/{}/landing'.format(userId))
        else:
            error = loginApprove
            
    return render_template('login.html', error=error)

# Sign Up Page
@LOGIN_BLUEPRINT.route('/signup', methods=['GET', 'POST'])
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