import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
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
    return make_response(jsonify({'error': 'Not found'}), 404)

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
    response = requests.get('http://loyalty:8050/api/v1/loyalty')
    return make_response(response.json(), 200)

#забронировать отель
@app.route('/api/v1/reservations', methods=['POST'])
def create_person():
    if not request.json:
        abort(400)
    if 'hotelUid' not in request.json:
        abort(400)

    response = requests.get('http://reservation:8070/api/v1/hotels')
    result = response.json()
    find_hotel_id = False
    hotel_uid = '???'
    for i in range(len(result['items'])):
        if result['items'][i]['hotel_uid'] == request.json['hotelUid']:
            find_hotel_id = True
            hotel_uid = result['items'][i]['hotel_uid']
            break
    #if find_hotel_id:
    result = hotel_uid 
    #result = jsonify(result['items'][0]['hotel_uid'])

    '''
    person_id = 0
    if len(persons) == 0:
        person_id = 1
    else:
        for p in persons:
            if p['id'] > person_id:
                person_id = p['id']
        person_id = person_id + 1
    person_created = {
        'id': person_id,
        'name': request.json['name'],
        'age': request.json['age'],
        'address': request.json['address'],
        'work': request.json['work']
    }
    '''
    return make_response(result, 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
