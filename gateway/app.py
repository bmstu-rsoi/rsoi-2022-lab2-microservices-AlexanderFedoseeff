import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8080

app = Flask(__name__)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1/hotels', methods=['GET'])
def get_hotels():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    result = requests.get('http://localhost:8070/api/v1/hotels')
    return make_response(result, 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
