from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/rn/', methods=['GET', 'POST'])
def rn_test():
    res = request.json
    print(res)
    return jsonify('Hello')

