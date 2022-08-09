from flask import render_template, url_for, request, redirect, flash, current_app
from flask_login import login_user, login_required, logout_user

from . import RMF_BLUEPRINT
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
STATUS_TASK_ARRIVED = 8
STATUS_TASK_RECEIVED = 9

#########################
#### RMF Task Status ####
#########################

@RMF_BLUEPRINT.route('/task-test', methods=['POST'])
def task_test():
    json_req = request.get_json()
    print(json_req)
    print(json_req['task_id'])
    print(json_req['address']['building_name'])
    print(json_req['address']['unit'])
    print(json_req['robot']['id'])
    print(json_req['operation']['task'])
    print(json_req['order']['id'])
    print(json_req['order']['company_name'])
    return json_req


# requests.post(url, json=event_data)
@RMF_BLUEPRINT.route('/task-status', methods=['POST'])
def task_status():
    
    json_req = request.get_json()
    print(json_req)
    if "status" in json_req:
        status = json_req["status"]
    if "task_id" in json_req:
        taskId = json_req["task_id"]
    if "robot" in json_req:
        robotId = json_req["robot"]["id"]

    task = system.get_task(taskId)
    order = system.get_order(task.orderId)
    print(f'task:{task.status}')
    print(f'status:{status}')
    # ipAddr, port = system.get_ip_route(order.storePostalCode)
    # waiting outside store for store to retrieve parcel from store
    if int(task.status) == system.STATUS_TASK_COLLECTING_FROM_STORE:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_WAITING_OUTSIDE_STORE)
            system.update_task_robot(taskId, robotId)
            system.robot_set_order_status(task.orderId, WAITING_FOR_PARCEL)
            print("Waiting outside store")

    # order deposited in hub and request external robot (just reached hub)
    if int(task.status) == STATUS_TASK_COLLECTED_FROM_STORE:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_REQUESTING_EXT_ROBOT)
            system.robot_set_order_status(task.orderId, AT_STORE_HUB)
            ipAddr, port = system.get_ip_route(order.customerPostalCode)
            buildingName = system.get_building_name(order.customerPostalCode)
            waypoint = system.get_egress_point(order.customerPostalCode)
            extrobotId = system.get_external_robot()
            system.set_robot_avail(extrobotId, 0)
            system.eject_robot(ipAddr, port, taskId, extrobotId, buildingName, waypoint, order.storePostalCode)
            print("requesting external robot")

    # external robot dispatched and sent to egress
    elif int(task.status) == STATUS_TASK_REQUESTING_EXT_ROBOT:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_EXT_ROBOT_DISPATCHED)
            system.update_task_robot(taskId, robotId)
            print("external robot dispatched")

    # external robot reached egress and sent to collect from hub
    elif int(task.status) == STATUS_TASK_EXT_ROBOT_DISPATCHED:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_COLLECTING_FROM_STORE_HUB)
            ipAddr, port = system.get_ip_route(order.customerPostalCode)
            system.send_external_task_rmf(ipAddr, port, taskId, 'nil', 'nil', robotId, system.TASK_COLLECT_FROM_HUB, order.orderId)
            print("collecting from store hub")

    # external robot collected from store hub and sent to store egress
    elif int(task.status) == STATUS_TASK_COLLECTING_FROM_STORE_HUB:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_SENT_TO_STORE_EGRESS)
            system.robot_set_order_status(task.orderId, BETWEEN_HUBS)
            ipAddr, port = system.get_ip_route(order.storePostalCode)
            buildingName = system.get_building_name(order.storePostalCode)
            waypoint = system.get_egress_point(order.storePostalCode)
            system.eject_robot(ipAddr, port, taskId, robotId, buildingName, waypoint, order.customerPostalCode)
            print("sent to store egress")

    # reached second egress and send for delivery
    elif int(task.status) == STATUS_TASK_SENT_TO_STORE_EGRESS:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_DELIVERING)
            system.robot_set_order_status(task.orderId, DELIVERING_TO_DOORSTEP)
            
            ipAddr, port = system.get_ip_route(order.storePostalCode)
            buildingName = system.get_building_name(order.customerPostalCode)
            waypoint = system.get_waypoint(order.customerPostalCode, order.customerUnitNumber)
            system.send_external_task_rmf(ipAddr, port, taskId, buildingName, waypoint, robotId, system.TASK_GO_TO_UNIT, order.orderId)
            print("delivering")

    elif int(task.status) == STATUS_TASK_DELIVERING:
        if status == 1:
            system.update_task_status(taskId, STATUS_TASK_ARRIVED)
            system.robot_set_order_status(task.orderId, ARRIVED)
            print("robot arrived")

    # order collected
    elif int(task.status) == STATUS_TASK_DELIVERING:
        if status == 1:
            system.set_robot_avail(robotId, 1)
            system.update_task_status(taskId, STATUS_TASK_RECEIVED)

    return json_req