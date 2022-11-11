import os
from payment_db import PaymentDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL
import uuid

port = os.environ.get('PORT')
if port is None:
    port = 8060

app = Flask(__name__)

@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found in payment'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1/get_payment', methods=['GET'])
def get_payment():
    db = PaymentDB()
    result = list(db.get_payment())
    if len(result) > 0:
        return make_response(jsonify(result[0]), 200)
    else:
        return make_response(jsonify({}), 400)

@app.route('/api/v1/post_payment', methods=['POST'])
def post_payment():
    price = request.form['price']
    payment_uid = str(uuid.uuid4())
    db = PaymentDB()
    result = list(db.post_payment(payment_uid, price))
    if len(result) > 0:
        return make_response(jsonify(result[0]), 201)
    else:
        return make_response(jsonify({}), 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
