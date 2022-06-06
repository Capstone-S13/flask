from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
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

SIGNUP_BLUEPRINT = Blueprint('signup_blueprint', __name__)

# Sign Up Page
@SIGNUP_BLUEPRINT.route('/signup')
def signup():
    
    return render_template('signup.html')

@SIGNUP_BLUEPRINT.route('/signup', methods=['POST'])
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