# -*- coding: utf-8 -*-
# pip install flask
# pip install flask-restx
# pip install pymongo
from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS
from get_script import download_script
from pymongo import MongoClient
from bson import json_util
import json
import sys, os

from os import path
from NLP.Summarization import load_summ_model
from NLP.QA import load_qa_model, QA_system
from NLP.STT import load_stt_model, stt
from NLP.basefunction import ctrl_f
from NLP.wordembedding import *


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
app = Flask(__name__)
CORS(app)
#api = Api(app)
# MongoDB connect
# mongo
client = MongoClient("mongo", 27017)
db = client.findyou
col_video_infos = db.video_infos
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

#### MODEL LOAD ########################

wm_model = load_wm_model()
summ_model = load_summ_model()
qa_model, qa_tokenizer = load_qa_model()
sc_model = load_sc_model()

########################################

@app.route('/scripts-load', methods=['POST'])
def load_script():
   params = request.get_json()#json.loads(request.get_data(), encoding = 'utf-8')

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


@app.route('/summ', methods=['POST'])
def get_summarization():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'
   
    scriptions = params['scriptions']
    result =  summary_script(scriptions, summ_model)

    return {
            "summarization": result
            }

@app.route('/qa', methods=['POST'])
def get_QA():
    params = json.loads(request.get_data(), encoding = 'utf-8')
    
    if len(params) == 0:
      return 'No parameter'

    question = params['question']
    scriptions = params['scriptions']
    answer = QA_system(qa_model, qa_tokenizer, question, scriptions)
    return {
            'answer':  answer
            }


@app.route('/stt', methods=['POST'])
def get_STT():
    params = json.loads(request.get_data(), encoding = 'utf-8')

    if len(params) == 0:
      return "No parameter"

    video_id = params['video_id'];

    return {
            'scriptions': 'success'
            }

@app.route('/cosim', methods=['POST'])
def get_cosim():
    params = json.loads(request.get_data(), encoding='utf-8')

    if len(params) == 0:
      return "No parameter"

    result = []

    scriptions = params['video_script_list']
  
    for script in scriptions:
      title = script['title']
      subs = script['scriptions']
      video_id = script['video_id']
      score = str(cosin_similar(title, subs, sc_model))
      result.append({
        'video_id' : video_id,
        'credibility' : score
      })
      
    return {
      'result': result
      }


@app.route('/association', methods=['POST'])
def get_asso():
    params = json.loads(request.get_data(), encoding='utf-8')
    scriptions = params['scriptions']
    keyword = params['keyword']
    result = association_f(keyword, scriptions, wm_model)
    return {
      'result': result
    }

if __name__ == "__main__":
#    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#    ssl_context.load_cert_chain(
#        certfile='./cert.pem',
#        keyfile='./key.pem',
#        password='abcd'
#    )
    app.run(host='0.0.0.0', port='5000', debug=True)#, ssl_context=ssl_context)
