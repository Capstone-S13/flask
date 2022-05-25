from sqlalchemy import true
from base import app
from models import db, UserDb, OrderDb, IngressDb
from uuid import uuid4

# Account Type
CUSTOMER = 0
STORE = 1

# Customer Landing Tab
CUSTOMER_SHOPS = 0
CUSTOMER_DELIVERY = 1

# Store Landing Tab
STORE_INCOMING = 0
STORE_PREPARING = 1
STORE_DELIVERY = 2

# Order Statuses
ORDER_RECEIVED = 0
ROBOT_DISPATCHED = 1
AT_STORE_HUB = 2
BETWEEN_HUBS = 3
AT_DEST_HUB = 4
ARRIVED = 5
DELIVERED = 6
CANCELLED = 7
FAILED = 8

def check_login(email, password):
    userAcc = UserDb.query.filter_by(email=email).first()
    if password != userAcc.password:
        return "invalid password", None, None
    else:
        return "approved", userAcc.userId, userAcc.accountType

def create_acc(newName, newEmail, newPassword, accType):
    uuid = uuid4()
    if accType == "0":
        newType = CUSTOMER
    else:
        newType = STORE
    new_acc = UserDb(userId = str(uuid), email = newEmail, name = newName, password = newPassword, accountType = int(accType))
    try:
        db.session.add(new_acc)
        db.session.commit()
        print(uuid, newEmail, newName, newPassword, accType)
        return True
    except Exception as e:
        print(e)  
        return False
    
def get_all_stores():
    return UserDb.query.filter_by(accountType=STORE)

def get_customer_orders(customerId):
    return OrderDb.query.filter_by(customerId=customerId)

def get_store_orders(storeId):
    return OrderDb.query.filter_by(storeId=storeId)
    
def create_order(userId, storeId):
    orderId = uuid4()
    new_order = OrderDb(orderId=orderId, customerId=userId, storeId=storeId, status=ORDER_RECEIVED)
    try:
        db.session.add(new_order)
        db.session.commit()
        return False
    except:
        return True
    
def get_order(userId, orderId):
    return OrderDb.query.get_or_404(orderId)

# change order status first then when the other party acknowlege then delete?
def delete_order(userId, orderId):
    order_to_delete = OrderDb.query.get_or_404(orderId)
    if order_to_delete.storeId == userId:
        try:
            db.session.delete(order_to_delete)
            db.session.commit()
            return "success"
        except:
            return "There was an error deleting the order"
    else:
        return "Order does not belong to user"
    return

def set_order_status(storeId, orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)

    if order_to_update.storeId == storeId:
        try:
            order_to_update.status = status
            db.session.commit()
            return "success"
        except:
            return "There was an error updating the order status"
    else:
        return "Order does not belong to user"
    
    return