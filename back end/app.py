from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from bm25 import bm25_rank
from extract import extract_kmeans
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/rn/', methods=['GET', 'POST'])
@cross_origin()
def rn_test():
    res = request.json
    print(res)
    response = jsonify('Hello')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/rank/', methods = ['GET', 'POST'])
def rank():
    res = request.json

    rank = bm25_rank(res["key"], 10)
    print(rank)
    return jsonify(rank)

@app.route('/keyword/', methods=['GET', 'POST'])
def extract_keywords():
    res = request.json
    print(res)
    query = "Andrew Yang"
    keywords = extract_kmeans('1210election.data',query,10,3,3,False)
    print(keywords)
    return jsonify(keywords)
