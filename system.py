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

def check_login(email, password):
    userAcc = UserDb.query.filter_by(email=email).first()
    if password != userAcc.password:
        return "invalid password", None, None
    else:
        return "approved", userAcc.userId, userAcc.accountType

# ADD LOGIC TO CHECK FOR DUPLICATE EMAIL
def create_acc(newName, newEmail, newPassword, accType):
    uuid = uuid4()
    new_acc = UserDb(userId = str(uuid),
                     email = newEmail,
                     name = newName,
                     password = newPassword,
                     accountType = int(accType))
    try:
        db.session.add(new_acc)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
    
def get_all_stores():
    return UserDb.query.filter_by(accountType=STORE).all()

def get_customer_orders(customerId):
    orders = OrderDb.query.filter_by(customerId=customerId).all()
    storeNames = {}
    for order in orders:
        userId = order.storeId
        if userId not in storeNames:
            newName = UserDb.query.filter_by(userId=userId).first().name
            storeNames[userId] = newName
    return storeNames, orders

def get_store_orders(storeId):
    orders = OrderDb.query.filter_by(storeId=storeId).all()
    customerNames = {}
    for order in orders:
        userId = order.customerId
        if userId not in customerNames:
            newName = UserDb.query.filter_by(userId=userId).first().name
            customerNames[userId] = newName
    incoming = OrderDb.query.filter_by(storeId=storeId,
                                      status=ORDER_SENT).all()
    preparing = OrderDb.query.filter_by(storeId=storeId,
                                       status=ORDER_RECEIVED or
                                            ROBOT_DISPATCHED).all()
    delivery = OrderDb.query.filter_by(storeId=storeId,
                                      status=AT_STORE_HUB or
                                            BETWEEN_HUBS or
                                            AT_DEST_HUB or
                                            ARRIVED).all()
    return customerNames, incoming, preparing, delivery

def get_vendor_details(userId):
    #this should return the entire row
    return UserDb.query.filter_by(accountType=STORE,
                                userId=userId).all()
    
def create_order(userId, storeId):
    orderId = uuid4()
    new_order = OrderDb(orderId=str(orderId),
                        customerId=userId,
                        storeId=storeId,
                        orderDetails="Something Cool",
                        status=ORDER_SENT)
    try:
        db.session.add(new_order)
        db.session.commit()
        return False
    except Exception as e:
        print(e)
        return True
    
def get_order(orderId):
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

def set_order_status(storeId, orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)

    if order_to_update.storeId == storeId:
        try:
            order_to_update.status = status
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    return False