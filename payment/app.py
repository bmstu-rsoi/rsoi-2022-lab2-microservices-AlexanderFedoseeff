import os
from payment_db import PaymentDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8060

app = Flask(__name__)

@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1/payment', methods=['GET'])
def get_payment():
    db = PaymentDB()
    result = list(db.get_payment())
    if len(result) > 0:
        return make_response(jsonify(result[0]), 200)
    else:
        return make_response(jsonify({}), 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
