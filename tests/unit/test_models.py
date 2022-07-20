from flask_sqlalchemy import SQLAlchemy
from application.models import UserDb, OrderDb, IngressDb
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from datetime import datetime

def test_new_user(new_user):
    assert new_user.id == "customerIdnuMber647"
    assert new_user.name == 'James Henderson'
    assert new_user.email == 'jhenderson@gmail.com'
    assert new_user.password != 'vEryS#cur3password'
    assert check_password_hash(new_user.password, 'vEryS#cur3password')
    assert new_user.postalCode == 'S123456'
    assert new_user.unitNumber == '#12-987'
    assert new_user.accountType == 0

def test_new_new_order(new_order):
    assert new_order.orderId == "orderIdnumber1346"
    assert new_order.customerId == "customerIdnuMber647"
    assert new_order.storeId == "storeIdnuMBer928"
    assert new_order.orderDetails == '1X Successful test'
    assert new_order.status == "Order Sent"
    assert new_order.robotID == "foodGrabRobot326"
    # assert new_order.dateCreated == timeNow
    
def test_new_ingress(new_ingress):
    assert new_ingress.postalCode == 123456
    assert new_ingress.ingressPoint == "Changi City Point"