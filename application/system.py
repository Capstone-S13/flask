import ipaddress
from tkinter import E
from sqlalchemy import true
import requests

from werkzeug.security import generate_password_hash, check_password_hash
from application.models import db, UserDb, OrderDb, IngressDb, TaskDb
# from application import maps
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

INGRESS_POINT = "Ingress Point"
EGRESS_POINT = "Egress Point"

# RMF Ports
INTERNAL_PORT = "7171" 
EXTERNAL_PORT = "7878"

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
WAITING_FOR_PARCEL = "Waiting for Parcel"
STORING_IN_STORE_HUB = "Storing in Store Hub"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
DELIVERING_TO_DOORSTEP = "Delivering to Doorstep"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

# statuses = {"Order Sent": 0,
#             "Order Received": 1,
#             "Robot Dispatched": 2,
#             "Storing in Store Hub": 3,
#             "At Store Hub": 4,
#             "Between Hubs": 5,
#             "At Destination Hub": 6,
#             "Delivering to Doorstep": 7,
#             "Arrived": 8,
#             "Delivered": 9,
#             "Cancelled": 10,
#             "Failed": 11}
# statuses[status]
# list(statuses)[2]

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

#################
#### USER DB ####
#################

def check_login(email, password):
    userAcc = UserDb.query.filter_by(email=email).first()
    
    if not userAcc or not check_password_hash(userAcc.password, password):
        return "invalid login", None

    else:
        return "approved", userAcc

def get_user(id):
    return UserDb.query.get_or_404(id)

# ADD LOGIC TO CHECK FOR DUPLICATE EMAIL
def create_acc(newName, newEmail, newPassword, newPostalCode, newUnitNumber, accType):
    user = UserDb.query.filter_by(email=newEmail).first()
    if user:
        return "User already exist!"
    
    uuid = uuid4()
    new_acc = UserDb(id = str(uuid),
                     email = newEmail,
                     name = newName,
                     password = generate_password_hash(newPassword, method='sha256'), # password hashing
                     postalCode = newPostalCode,
                     unitNumber = newUnitNumber,
                     accountType = int(accType))
    try:
        db.session.add(new_acc)
        db.session.commit()
        return False
    except Exception as e:
        print(e)
        return e
    
def get_all_stores():
    return UserDb.query.filter_by(accountType=STORE).all()

def get_vendor_details(id):
    #this should return the entire row
    user =  UserDb.query.filter_by(accountType=STORE,
                                id=id).all()
    userDetails = {}
    for details in user:
        id = details.id
        if id not in userDetails:
            newName = UserDb.query.filter_by(id=id).first().name
            userDetails[id] = newName
    return userDetails

def update_user(id, name, email, postalCode, unitNumber):
    user_to_update = UserDb.query.get_or_404(id)
    emailCheck = UserDb.query.filter_by(email=email).first()
    if emailCheck and user_to_update!=emailCheck:
        return "Email already exist"
    try:
        user_to_update.name = name
        user_to_update.email = email
        user_to_update.postalCode = postalCode
        user_to_update.unitNumber = unitNumber
        db.session.commit()
        return False
    except Exception as e:
        print(e)
        return e

##################
#### ORDER DB ####
##################

def create_order(id, storeId):
    orderId = uuid4()
    customer = UserDb.query.get_or_404(id)
    store = UserDb.query.get_or_404(storeId)

    new_order = OrderDb(orderId=str(orderId),
                        customerId=id,
                        customerPostalCode=customer.postalCode,
                        customerUnitNumber=customer.unitNumber,
                        storeId=storeId,
                        storePostalCode=store.postalCode,
                        storeUnitNumber=store.unitNumber,
                        orderDetails="Something Cool",
                        status=ORDER_SENT)
    try:
        db.session.add(new_order)
        db.session.commit()
        
        return False
    except Exception as e:
        print(e)
        return e

def get_order(orderId):
    return OrderDb.query.get_or_404(orderId)

def get_customer_orders(customerId):
    orders = OrderDb.query.filter_by(customerId=customerId).all()
    storeNames = {}
    order_waypoints = {}
    for order in orders:
        id = order.storeId
        if id not in storeNames:
            newName = UserDb.query.filter_by(id=id).first().name
            storeNames[id] = newName
        if order.status == DELIVERING_TO_DOORSTEP:
            waypoints = get_all_waypoints(order.customerPostalCode)
            order_waypoints[order.orderId] = waypoints
    return storeNames, orders, order_waypoints

def get_store_orders(storeId):
    orders = OrderDb.query.filter_by(storeId=storeId).all()
    customerNames = {}
    # print(orders)
    for order in orders:
        # print(order)
        id = order.customerId
        if id not in customerNames:
            newName = UserDb.query.filter_by(id=id).first().name
            customerNames[id] = newName
    incoming = OrderDb.query.filter_by(storeId=storeId,
                                      status=ORDER_SENT).all()
    preparing = OrderDb.query.filter_by(storeId=storeId,
                                       status=ORDER_RECEIVED).all()
    delivery = OrderDb.query.filter_by(storeId=storeId).\
                            filter(OrderDb.status!=ORDER_SENT).\
                            filter(OrderDb.status!=ORDER_RECEIVED).all()
    return customerNames, incoming, preparing, delivery

# change order status first then when the other party acknowlege then delete?
def delete_order(id, orderId):
    order_to_delete = OrderDb.query.get_or_404(orderId)
    if order_to_delete.storeId == id:
        try:
            db.session.delete(order_to_delete)
            db.session.commit()
            return "success"
        except:
            return "There was an error deleting the order"
    else:
        return "Order does not belong to user"

def set_order_status(userId, orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)

    if order_to_update.storeId == userId or order_to_update.customerId == userId:
        try:
            order_to_update.status = status
            db.session.commit()
            
            # Store request for parcel to be picked up
            if status == ROBOT_DISPATCHED:
                print(status)
                buildingName = get_ingress_point(order_to_update.storePostalCode)
                waypoint = get_waypoint(order_to_update.storePostalCode, order_to_update.storeUnitNumber)
                taskId = create_task(orderId)
                ipAddr, port = get_ip_route(order_to_update.storePostalCode)
                print(ipAddr, port)
                # test_json('10.12.192.185', '7171', taskId, "vovi_city", "pantry", 'nil', TASK_GO_TO_UNIT, 'nil')
                send_internal_task_rmf(ipAddr, port, taskId, buildingName, waypoint, 'nil', TASK_GO_TO_UNIT, 'nil')
            
            # Store put parcel in robot and sent it back to hub
            elif status == STORING_IN_STORE_HUB:
                curr_task = TaskDb.query.filter_by(orderId=orderId).first()
                update_task_status(curr_task.taskId, STATUS_TASK_COLLECTED_FROM_STORE)
                ipAddr, port = get_ip_route(order_to_update.storePostalCode)
                send_internal_task_rmf(ipAddr, port, curr_task.taskId, 'nil', 'nil', curr_task.robotId, TASK_DELIVER_TO_HUB, orderId)

            # Customer request for parcel to be delivered from destination hub
            elif status == DELIVERED:
                curr_task = TaskDb.query.filter_by(orderId=orderId).first()
                update_task_status(curr_task.taskId, STATUS_TASK_RECEIVED)
                ipAddr, port = get_ip_route(order_to_update.customerPostalCode)
                send_external_task_rmf(ipAddr, port, curr_task.taskId, 'lounge', 'nil', curr_task.robotId, TASK_GO_TO_UNIT, 'nil')
            #     buildingName = get_ingress_point(order_to_update.storePostalCode)
            #     waypoint = IngressDb.query.filter_by(postalCode=order_to_update.storePostalCode,
            #                                         unitNumber=order_to_update.storeUnitNumber).first()
            #     send_order_rmf(order_to_update.status, buildingName, waypoint)
            return False
        except Exception as e:
            print(e)
            return e
    return "Order does not belong to user!"

def robot_set_order_status(orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)
    try:
        order_to_update.status = status
        db.session.commit()
        return False
    except Exception as e:
            print(e)
            return e
    return "Order does not belong to user!"

####################
#### INGRESS DB ####
####################

def create_ingress(postalCode, unitNumber, waypointName):
    uuid = uuid4()
    new_ingress = IngressDb(ingressId=str(uuid),
                            postalCode=postalCode,
                            unitNumber=unitNumber,
                            waypoint=waypointName)
    try:
        db.session.add(new_ingress)
        db.session.commit()
        return False
    except Exception as e:
        print(e)
        return e

def get_all_waypoints(postalCode):
    data_lst = IngressDb.query.filter_by(postalCode=postalCode).all()
    waypoints = []
    for data in data_lst:
        if data.unitNumber != "Ingress Point":
            waypoints.append(data.waypoint)
    return waypoints

def get_waypoint(postalCode, unitNumber):
    ingress = IngressDb.query.filter_by(postalCode=postalCode,
                                        unitNumber=unitNumber).first()
    return ingress.waypoint

def get_ingress_point(postalCode):
    #returns building name
    ingress = IngressDb.query.filter_by(postalCode=postalCode, unitNumber=INGRESS_POINT).first()
    return ingress.waypoint
    
def get_egress_point(postalCode):
    egress = IngressDb.query.filter_by(postalCode=postalCode, unitNumber=EGRESS_POINT).first()
    return egress.waypoint

def get_ip_route(postalCode):
    ingress = IngressDb.query.filter_by(postalCode=postalCode, unitNumber=INGRESS_POINT).first()
    return ingress.ip, ingress.port

def get_map(postalCode):
    ingress = IngressDb.query.filter_by(postalCode=postalCode, unitNumber=INGRESS_POINT).first()
    return ingress.image, ingress.resolution, ingress.origin, ingress.negate, ingress.occupied_thresh, ingress.free_thresh, ingress.pgm

# def upload_maps(storePostalCode, customerPostalCode):
#     storeIngress = IngressDb.query.filter_by(postalCode=storePostalCode, unitNumber=INGRESS_POINT).first()
#     customerIngress = IngressDb.query.get_or_404(customerPostalCode)
#     storeyaml = maps.level_4_map.yaml
#     customeryaml = maps.level_4_map_2.yaml
#     try:
#         storeIngress.image = storeyaml.image
#         storeIngress.resolution = f'{storeyaml.resolution}'
#         storeIngress.origin = f'{storeyaml.origin}'
#         storeIngress.negate = storeyaml.negate
#         storeIngress.occupied_thresh = f'{storeyaml.occupied_thresh}'
#         storeIngress.free_thresh = f'{storeyaml.free_thresh}'
#         storeIngress.pgm = f'{maps.level_4_map.pgm}'
#     except Exception as e:
#         print(e)

def set_ip_port(postalCode, ip, port):
    ingress_to_update = IngressDb.query.filter_by(postalCode=postalCode, unitNumber=INGRESS_POINT).first()

#################
#### TASK DB ####
#################

def create_task(orderId):
    uuid = str(uuid4())
    new_task = TaskDb(taskId=uuid,
                    status = STATUS_TASK_COLLECTING_FROM_STORE,
                    orderId=orderId)
    try:
        db.session.add(new_task)
        db.session.commit()
        return uuid
    except Exception as e:
        print(e)
        return e

def get_task(taskId):
    return TaskDb.query.get_or_404(taskId)

# update task status
def update_task_status(taskId, status):
    task_to_update = TaskDb.query.get_or_404(taskId)
    try:
        task_to_update.status = status
        db.session.commit()
    except Exception as e:
        print(e)
        return e

# update robot id
def update_task_robot(taskId, robotId):
    task_to_update = TaskDb.query.get_or_404(taskId)
    try:
        task_to_update.robotId = robotId
        db.session.commit()
    except Exception as e:
        print(e)
        return e

def set_new_waypoint(orderId, new_waypoint):
    task_to_update = TaskDb.query.filter_by(orderId=orderId).first()
    order = get_order(orderId)
    if order.status == DELIVERING_TO_DOORSTEP:
        try:
            unitNumber = IngressDb.query.filter_by(postalCode=order.customerPostalCode,
                                                    waypoint=new_waypoint).first().unitNumber
            order.customerUnitNumber = unitNumber
            db.session.commit()
            ipAddr, port = get_ip_route(order.customerPostalCode)
            buildingName = get_ingress_point(order.customerPostalCode)
            # waypoint = get_waypoint(order.customerPostalCode, order.customerUnitNumber)
            send_external_task_rmf(ipAddr, port, task_to_update.taskId, buildingName, new_waypoint, task_to_update.robotId, TASK_GO_TO_UNIT, order.orderId)
        except Exception as e:
            print(e)
            return e
        

#############
#### RMF ####
#############

# def test_send_waypoint():
#     print("testing")
#     send_order_rmf(ROBOT_DISPATCHED, "vovi_city", "pantry", INTERNAL_PORT)

def test_json(ipAddr, port, taskId, buildingName, unit, robotId, task, orderId):
    print("testing has started")
    url = "http://172.23.31.173:5000/task-test"
    requests.post(url, json={
                            "task_id": taskId,                            
                            "address":
                                {
                                    'building_name':f'{buildingName}',
                                    'unit':f'{unit}'
                                },
                            "robot":
                                {
                                    "id":f'{robotId}'
                                },
                            "operation":
                                {
                                    "task": task
                                },
                            "order":
                                {
                                    "id": f'{orderId}',
                                    "company_name": "barg",
                                }
                            })

# "http://10.12.192.185:7171/internal-task"
def send_internal_task_rmf(ipAddr, port, taskId, buildingName, unit, robotId, task, orderId):
    url = f"http://{ipAddr}:" + port + "/internal-task"
    url = "http://172.23.31.173:80/internal-task"
    print(url)
    print(buildingName, unit)
    print(taskId)
    print(task)
    print(orderId)
    requests.post(url, json={
                            "task_id": taskId,                            
                            "destination":
                                {
                                    'building_name':f'{buildingName}',
                                    'unit':f'{unit}'
                                },
                            "robot":
                                {
                                    "id":f'{robotId}'
                                },
                            "operation":
                                {
                                    "task": task
                                },
                            "order":
                                {
                                    "id": f'{orderId}',
                                    "company_name": "barg",
                                }
                            })
    print("test finished")

# "http://10.12.192.185:7171/external-task"
def send_external_task_rmf(ipAddr, port, taskId, buildingName, unit, robotId, task, orderId):
    url = f"http://{ipAddr}:" + port + "/external-task"
    url = "http://172.23.31.173:80/external-task"
    requests.post(url, json={
                            "task_id": taskId,                            
                            "destination":
                                {
                                    'building_name':f'{buildingName}',
                                    'unit':f'{unit}'
                                },
                            "robot":
                                {
                                    "id":f'{robotId}'
                                },
                            "operation":
                                {
                                    "task": task
                                },
                            "order":
                                {
                                    "id": f'{orderId}',
                                    "company_name": "barg",
                                }
                            })
    print("test finished")

# "http://10.12.192.185:7171/receive-robot"
# def receive_robot(ipAddr, port, taskId, buildingName, unit, orderId, robotId, operation):
#     url = f"http://{ipAddr}:" + port + "/receive-robot"
#     requests.post(url, json={
#                             "task_id":f'{taskId}',
#                             "ingress_point":
#                                 {
#                                     'building_name':f'{buildingName}',
#                                     'unit':f'{unit}'
#                                 },
#                             "order":
#                                 {
#                                     'id':f'{orderId}',
#                                     'company_name':"barg"
#                                 },
#                             "robot":
#                                 {
#                                     'id':f'{robotId}'
#                                 },
#                             "operation":
#                                 {
#                                     'task':f'{operation}'
#                                 }
#                             })

# "http://10.12.192.185:7171/eject-robot"
def eject_robot(ipAddr, port, taskId, robotId, buildingName, unit, postalCode):
    url = f"http://{ipAddr}:" + port + "/eject-robot"
    url = "http://172.23.31.173:80/eject-robot"
    image, resolution, origin, negate, occupied_thresh, free_thresh, pgm = get_map(postalCode)
    origin = origin[1:-1].split(",")
    requests.post(url, json={
                            "task_id":f'{taskId}',
                            "robot":
                                {
                                    'robot':f'{robotId}'
                                },
                            "egress_point":
                                {
                                    'building_name':f'{buildingName}',
                                    'unit':f'{unit}'
                                },
                            "new_host":
                                {
                                    'ip':f'{ipAddr}',
                                    'port': port
                                },
                            "map":
                                {
                                    # 'image': "file_name.pgm",
                                    # 'resolution': 0.2,
                                    # 'origin': [0,1,2],
                                    # 'negate': 0,
                                    # 'occupied_thresh': 0.1,
                                    # 'free_thresh': 0.1,
                                    # 'pgm': 'pgm_string'
                                    'image': f'{image}',
                                    'resolution': float(resolution),
                                    'origin': [float(x) for x in origin],
                                    'negate': int(negate),
                                    'occupied_thresh': float(occupied_thresh),
                                    'free_thresh': float(free_thresh),
                                    'pgm': f'{pgm}'
                                },
                            "initial_pose": [0,1,2,3]
                            })
    
def get_response():
    url = "http://10.12.192.185:7171"
    requests.get(url)

##################
#### Setup DB ####
##################

def test_pgm():
    with open("./application/maps/level_4_map.pgm", "rb") as image:
        f = image.read()
        b = bytes(f)
    
    print(type(b))
    print(b)
    storePgm = ''
    for i in b:
        storePgm += str(i)

    # print(storePgm)

def create_starting_ingress():
    with open("./application/maps/level_4_map.pgm", "rb") as image:
        f = image.read()
        storePgm = bytes(f)

    with open("./application/maps/level_4_map_2.pgm", "rb") as image:
        f = image.read()
        customerPgm = bytes(f)

    store_ingress = IngressDb(ingressId = str(uuid4()),
                            postalCode = 123456,
                            unitNumber = INGRESS_POINT,
                            waypoint = "vovi_city",
                            ip = "10.12.192.185",
                            port = '7171',
                            image = 'level_4_map.pgm',
                            resolution = '0.050000',
                            origin = "[-32.457816, -23.565106, 0.000000]",
                            negate = 0,
                            occupied_thresh = '0.65',
                            free_thresh = '0.196',
                            pgm = storePgm
                            )
    customer_ingress = IngressDb(ingressId = str(uuid4()),
                            postalCode = 987654,
                            unitNumber = INGRESS_POINT,
                            waypoint = "vovi_city",
                            ip = "10.12.192.185",
                            port = '7171',
                            image = 'level_4_map_2.pgm',
                            resolution = '0.050000',
                            origin = "[-5.563073, -36.382617, 0.000000]",
                            negate = 0,
                            occupied_thresh = '0.65',
                            free_thresh = '0.196',
                            pgm = customerPgm
                            )
    try:
        db.session.add(store_ingress)
        db.session.add(customer_ingress)
        db.session.commit()
    except Exception as e:
        print(e)
        return e

    waypoints = [["01-01", "pantry"], ["01-02", "coe"], ["01-03", "supplies"], ["01-04", "hardware_2"], ["01-05", "lounge"]]
    for unit, waypoint in waypoints:
        new_ingress = IngressDb(ingressId = str(uuid4()),
                                postalCode = 123456,
                                unitNumber = unit,
                                waypoint = waypoint)
        try:
            db.session.add(new_ingress)
            db.session.commit()
        except Exception as e:
            print(e)
            return e

    for unit, waypoint in waypoints:
        new_ingress = IngressDb(ingressId = str(uuid4()),
                                postalCode = 987654,
                                unitNumber = unit,
                                waypoint = waypoint)
        try:
            db.session.add(new_ingress)
            db.session.commit()
        except Exception as e:
            print(e)
            return e