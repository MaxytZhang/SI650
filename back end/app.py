from flask import Flask, request, jsonify
from bm25 import bm25_rank
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