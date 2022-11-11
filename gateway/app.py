import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
import datetime
import json
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
    return make_response(jsonify({'error': 'Not found in gateway'}), 404)

#получить список отелей
@app.route('/api/v1/hotels', methods=['GET'])
def get_hotels():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    response = requests.get('http://reservation:8070/api/v1/hotels')
    return make_response(response.json(), 200)

#получить информацию о статусе в системе бронирования
@app.route('/api/v1/loyalty', methods=['GET'])
def get_loyalty():
    if 'X-User-Name' not in request.headers:
        abort(400)
    username = request.headers.get('X-User-Name')
    params_dict = {'username': username}
    response = requests.get('http://loyalty:8050/api/v1/loyalty', params = params_dict)
    return make_response(response.json(), 200)

#забронировать отель
@app.route('/api/v1/reservations', methods=['POST'])
def create_person():
    er = []
    r = []
    discount_computed = False
    find_hotel_id = False
    payment_complited = False
    hotel_uid = ''
    price = 0
    total_price = 0
    discount = 0
    reservationUid = ''
    status = ''
    if not request.json:
        abort(400)
    if 'hotelUid' not in request.json or 'startDate' not in request.json or 'endDate' not in request.json:
        abort(400)
    if 'X-User-Name' not in request.headers:
        abort(400)
    username = request.headers.get('X-User-Name')
    response_hotels = requests.get('http://reservation:8070/api/v1/hotels')
    result_hotels = response_hotels.json()
    params_dict = {'username': username}
    response_loyalty = requests.get('http://loyalty:8050/api/v1/loyalty', params = params_dict)
    if response_loyalty.status_code == 200:
        discount = response_loyalty.json()['discount']
        discount_computed = True
    elif response_loyalty.status_code == 404:
        discount = 0
        discount_computed = True
    else:
        er.append({"discount_computed": False})
    
    date_time_str_startDate = request.json['startDate']
    date_time_str_endDate = request.json['endDate']
    date_time_obj_startDate = datetime.datetime.strptime(date_time_str_startDate, '%Y-%m-%d')
    date_time_obj_endDate = datetime.datetime.strptime(date_time_str_endDate, '%Y-%m-%d')
    duration = date_time_obj_endDate - date_time_obj_startDate
    duration_in_s = duration.total_seconds()
    days = duration.days

    for i in range(len(result_hotels['items'])):
        if result_hotels['items'][i]['hotel_uid'] == request.json['hotelUid']:
            find_hotel_id = True
            hotel_uid = result_hotels['items'][i]['hotel_uid']
            price = result_hotels['items'][i]['price']
            break
    if not find_hotel_id:
        er.append({"find_hotel_uid": False})
    else:
        if discount_computed:
            total_price = int((days * price) - (((days * price) / 100) * discount))
            response_payment = requests.post('http://payment:8060/api/v1/post_payment', data = {'price': total_price})
            if response_payment.status_code == 201 or True:
                reservationUid = response_payment.json()['payment_uid']
                status = response_payment.json()['status']
                payment_complited = True

                r.append({
                    "reservationUid": reservationUid,
                    "hotelUid": hotel_uid, 
                    "startDate": date_time_str_startDate, 
                    "endDate": date_time_str_endDate,
                    "discount": discount, 
                    "status": status, 
                    "payment": { 
                        "status": status,
                        "price": total_price
                    }
                })
            else:
                er.append({'payment_complited': False})

    if find_hotel_id and discount_computed and payment_complited:
        return make_response(r, 200)
    else:
        return make_response(er, 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
