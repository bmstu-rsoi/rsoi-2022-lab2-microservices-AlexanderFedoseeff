import os
from reservation_db import ReservationDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8070

app = Flask(__name__)

@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found in reservation'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1/hotels', methods=['GET'])
def get_hotels():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    db = ReservationDB()
    items = db.get_hotels()
    result = {'page': page, 'pageSize': size, 'totalElements': len(items),  'items': items}
    return make_response(jsonify(result), 200)

@app.route('/api/v1/reservate', methods=['POST'])
def reservate():
    db = ReservationDB()
    reservation_uid = request.form['reservation_uid']
    username = request.form['username']
    payment_uid = request.form['payment_uid']
    hotel_id = request.form['hotel_id']
    status = request.form['status']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    result = db.reservate(reservation_uid, username, payment_uid, hotel_id, status, start_date, end_date)
    if result:
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({}), 400)

@app.route('/api/v1/cancel_reservation', methods=['POST'])
def cancel_reservation():
    db = ReservationDB()
    reservation_uid = request.form['reservation_uid']
    payment_uid = db.cancel_reservation(reservation_uid)
    if payment_uid != '':
        return make_response(jsonify({'payment_uid': payment_uid}), 201)
    else:
        return make_response(jsonify({}), 400)

@app.route('/api/v1/get_user_reservations', methods=['GET'])
def get_user_reservations():
    username = request.args.get('username', default=' ', type=str)
    db = ReservationDB()
    result = db.user_reservations(username)
    return make_response(result, 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
