# -*- coding: utf-8 -*-
# pip install flask
# pip install flask-restx
# pip install pymongo
from basefunction.FindUMethod import Ctrl_F, Frequency
from flask import Flask, request, jsonify, Response
from flask_restx import Api, Resource
from flask_cors import CORS
from get_script import download_script
from pymongo import MongoClient
from bson import json_util
import ssl
import json
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
app = Flask(__name__)
CORS(app)

# MongoDB connect
# mongo
client = MongoClient("localhost", 27017)
db = client.findyou
col_video_infos = db.video_infos


@app.route('/unit-find', methods=['POST'])
def ctrl_f():
    params = request.get_json()  # json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    keyword = params['keyword']
    video_id = params['video_id']

    video_data = col_video_infos.find_one({"video_id": video_id})

    return {
        "video_id": video_id,
        "keyword": keyword,
        "result": Ctrl_F(keyword, video_data['transcript'])
    }


@app.route('/ml/freq', methods=['POST'])
def frequency():
    params = request.get_json()  # json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    keyword = params['keyword']
    video_id = params['video_id']
    result = []
    for _id in video_id:
        video_data = col_video_infos.find_one({"video_id": _id})

        if video_data is None:
            try:
                video_data = download_script(_id)
                col_video_infos.insert_one(
                    json.loads(json_util.dumps(video_data)))
            except:
                result.append({
                    "video_id": _id,
                    "credibility": "no subs"
                })
                continue

        script_data = video_data['transcript']
        tmp_result = {
            "video_id": _id,
            "credibility": Frequency(keyword, script_data)
        }
        result.append(tmp_result)
    # only_script = ""
    # for r in script_data:
    #     text = r['text']
    #     if '[' in text:
    #         continue
    #     only_script += (text.strip('"') + " ")

    #result = ""

    return {
        "keyword": keyword,
        "result": result
    }


@app.route('/scripts-load', methods=['POST'])
def load_script():
    params = request.get_json()  # json.loads(request.get_data(), encoding = 'utf-8')

    if len(params) == 0:
        return 'No parameter'

    video_id = params['video_id']
    try:
        video_data = col_video_infos.find_one({"video_id": video_id})

    except Exception:
        return {"Error_Message": "Doesn't have subscriptions"}

    if video_data is None:
        video_data = download_script(video_id)
        col_video_infos.insert_one(json.loads(json_util.dumps(video_data)))

    return json.loads(json_util.dumps(video_data))

############################# To do ###################################


@app.route('/ml', methods=['POST'])
def get_summarization():
    params = json.loads(request.get_data(), encoding='utf-8')

    if len(params) == 0:
        return 'No parameter'

    video_id = params['video_id']
    video_data = col_video_infos.find_one({"video_id": video_id})

    summarization = video_data['summarization']
    if summarization == '':
        print("no data")
        # do summarization
        result = ""
        # update data in DB
        col_video_infos.update({"video_id": video_id}, {
                               "$set": {"summarization": result}})

    response = {"video_id": video_id,
                "summarization": summarization
                }
    #response.headers.add("Access-Control-Allow-Origin", "*")

    return {"video_id": video_id,
            "summarization": summarization
            }


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(
        certfile='./cert.pem',
        keyfile='./key.pem',
        password='abcd'
    )
    app.run(host='0.0.0.0', port='5000', debug=True, ssl_context=ssl_context)
