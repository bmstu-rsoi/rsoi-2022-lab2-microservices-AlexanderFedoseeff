import os
from loyalty_db import LoyaltyDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8050

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found in loyalty'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1/loyalty', methods=['GET'])
def get_loyalty():
    db = LoyaltyDB()
    username = request.args.get('username', default=0, type=str)
    result = list(db.get_loyalty(username))
    if len(result) == 1:
        return make_response(jsonify(result[0]), 200)
    elif len(result) == 0:
        return make_response(jsonify({'service': 'loyalty', 'error': 'Not found in db', 'username': username}), 404)
    else:
        return make_response(jsonify({'service': 'loyalty', 'error': 'More then one result in db', 'username': username}), 500)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
