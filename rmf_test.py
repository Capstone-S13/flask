from flask import Flask, request, jsonify
import requests
from time import sleep
from uuid import uuid4

HOST_URL = "172.23.31.173"
# HOST_URL = "10.12.112.72"

app = Flask(__name__)
@app.route("/internal-task", methods=['POST'])
def internal_task():
    json_req = request.get_json()
    print(f"Task ID: {json_req['task_id']}")
    print(f"Building Name: {json_req['destination']['building_name']}")
    print(f"Unit: {json_req['destination']['unit']}")
    print(f"Operation Task: {json_req['operation']['task']}")
    print(f"Order ID: {json_req['order']['id']}")
    print(f"Company Name: {json_req['order']['company_name']}")
    
    sleep(5)
    url = f"http://{HOST_URL}:5000/task-status"
    print("internal task completed")

    
    requests.post(url, json={
                            "robot":
                                {
                                    'id': json_req['robot']['id']
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })
    return json_req

@app.route("/external-task", methods=['POST'])
def external_task():
    json_req = request.get_json()
    print(f"Task ID: {json_req['task_id']}")
    print(f"Building Name: {json_req['destination']['building_name']}")
    print(f"Unit: {json_req['destination']['unit']}")
    print(f"Operation Task: {json_req['operation']['task']}")
    print(f"Order ID: {json_req['order']['id']}")
    print(f"Company Name: {json_req['order']['company_name']}")

    sleep(5)
    url = f"http://{HOST_URL}:5000/task-status"
    print("external task completed")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': json_req['robot']['id']
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })
    return json_req

@app.route("/eject-robot", methods=['POST'])
def eject_robot():
    print('EJECTING ROBOT')
    json_req = request.get_json()
    print(f"Task ID: {json_req['task_id']}")
    print(f"Robot ID: {json_req['robot']['id']}")

    print(f"Building Name: {json_req['egress_point']['building_name']}")
    print(f"Unit: {json_req['egress_point']['unit']}")

    print(f"IP Address: {json_req['new_host']['ip']}")
    print(f"Port: {json_req['new_host']['port']}")    

    print(f"Map Name: {json_req['map']['image']}")
    print(f"Initial Pose: {json_req['initial_pose']}")
    sleep(5)
    url = f"http://{HOST_URL}:5000/task-status"
    print("robot ejecting")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': json_req['robot']['id']
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })

    sleep(5)
    print("robot ejected")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': json_req['robot']['id']
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })

    return json_req


app.run(host="0.0.0.0", port=80)