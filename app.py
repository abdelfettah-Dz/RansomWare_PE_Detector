from flask import Flask, redirect, render_template, request
from functions import *
import requests
import time


app = Flask(__name__)

HEADERS = {"Authorization": ""}


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/analyze", methods=["POST"])
def analyze():    # Return the loading template with the task ID
    ADD_URL = "http://localhost:8090/tasks/create/file"
    file = request.files["file"]
    files = {"file": (file.filename, file)}
    response = requests.post(ADD_URL, headers=HEADERS, files=files)
    if(response.status_code==200):
        task_id = response.json()["task_id"]
        return render_template('loading.html', task_id=task_id, status= "waiting")
    else:
        return render_template('Error.html', error= "Failed to create task")

@app.route("/status/<task_id>", methods=["POST"])
def status(task_id):
    status_url = "http://localhost:8090/tasks/view/{}".format(task_id)
    status_response = requests.get(status_url, headers= HEADERS)
    if status_response.status_code == 200:
        data = status_response.json()
        status = data.get("task", {}).get("status")
        return status
    else:
        return "error"

@app.route("/result/<task_id>", methods=["POST"])
def result(task_id):
    # Get the report
    report_url = "http://localhost:8090/tasks/summary/{}".format(task_id)
    report_response = requests.get(report_url, headers= HEADERS)
    if report_response.status_code == 200:
        # USE THE REPORT TO PREDICT
        report = report_response.json()
        result= final_predict_label(report)
        return render_template('result.html', result= result)
    else:
        return render_template('Error.html', error= "Failed to report analysis")



if __name__ == "__main__":
    app.run(debug = True)
