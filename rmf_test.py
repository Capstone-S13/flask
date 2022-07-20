from flask import Flask, request, jsonify
import requests
from time import sleep
from uuid import uuid4

app = Flask(__name__)
@app.route("/internal-task", methods=['POST'])
def internal_task():
    json_req = request.get_json()
    print(json_req)

    sleep(5)
    url = "http://172.23.31.173:5000/task-status"
    print("internal task completed")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': "some robot id"
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })
    return json_req

@app.route("/external-task", methods=['POST'])
def external_task():
    json_req = request.get_json()
    print(json_req)

    sleep(5)
    url = "http://172.23.31.173:5000/task-status"
    print("external task completed")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': "some robot id"
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })
    return json_req

@app.route("/eject-robot", methods=['POST'])
def eject_robot():
    json_req = request.get_json()
    # print(json_req)

    sleep(5)
    url = "http://172.23.31.173:5000/task-status"
    print("robot ejecting")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': "some robot id"
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })

    sleep(5)
    print("robot ejected")
    requests.post(url, json={
                            "robot":
                                {
                                    'id': "some robot id"
                                },                            
                            "task_id": json_req['task_id'],
                            "status": 1
                            })

    return json_req


app.run(host="0.0.0.0", port=80)