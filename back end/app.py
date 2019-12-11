from flask import Flask, request, jsonify
from bm25 import bm25_rank
from extract import extract_kmeans
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/rn/', methods=['GET', 'POST'])
def rn_test():
    res = request.json
    print(res)
    return jsonify('Hello')

@app.route('/rank/', methods = ['GET', 'POST'])
def rank():
    res = request.json

    rank = bm25_rank(res)
    print(rank)
    return jsonify(rank)

@app.route('/keyword/', methods=['GET', 'POST'])
def extract_keywords():
    res = request.json
    print(res)
    query = "Yang"
    keywords = extract_kmeans('1210election.data',query,10,3,10,False)
    print(keywords)
    return jsonify(keywords)
