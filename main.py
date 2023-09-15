#!/usr/bin/env python

from flask import Flask, json, render_template, request
import os
from track import *

from rq import Queue
from rq.job import Job
from worker import conn

#create instance of Flask app
app = Flask(__name__)
q = Queue(connection=conn)
id = 0

def helper(link, id):
    tracker(link, id)
@app.route("/push", methods=['GET', 'POST'])
def push():
    global id
    json_url = 'data/data.json'
    if id == 0:
        with open(json_url,"r+") as file:
            file.truncate()
            data_json = {}
            data_json["pairs"] = {}
            data_json["jobs"] = {}
            file.seek(0)
            json.dump(data_json, file)
    if request.method == 'POST':
        vid = request.form['link']
        job = q.enqueue_call(
            func=helper, args=(vid, id), result_ttl=5000
        )
        with open(json_url,"r+") as file:
            data_json = json.load(file)
            data_json["pairs"][job.get_id()] = id
            file.seek(0)
            json.dump(data_json, file)
        id += 1
        print(job.get_id())
        return job.get_id()
    return render_template('vidform.html')


@app.route("/query/<job_key>", methods=['GET'])
def query(job_key):
    json_url = os.path.join("data","data.json")
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['jobs']
        real_id = data_json['pairs'][str(job_key)]
        return data[str(real_id)]

@app.route("/status/<job_key>", methods=['GET'])
def status(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return 'finished'
    elif job.get_status()=='started':
        return 'processing'
    else:
        return 'queued'

@app.route("/list", methods=['GET'])
def list():
    json_url = os.path.join("data","data.json")
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['pairs']
        ls = []
        for a in data:
            ls.append(a)
        return ls
    
if __name__ == "__main__":
    app.run(debug=True)
