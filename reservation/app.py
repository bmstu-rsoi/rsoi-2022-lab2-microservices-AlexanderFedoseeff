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
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)

@app.route('/api/v1/hotels', methods=['GET'])
def get_hotels():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    db = ReservationDB()
    print(db.get_hotels())
    print(page)
    print(size)
    items = db.get_hotels()
    result = {'page': page, 'pageSize': size, 'totalElements': len(items),  'items': items}
    return make_response(jsonify(result), 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
'''
@app.route('/api/v1/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    db = ControlDB()
    persons = db.get_persons()
    person = list(filter(lambda t: t['id'] == person_id, persons))
    if len(person) == 0:
        abort(404)
    return make_response(jsonify(person[0]), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1/persons', methods=['POST'])
def create_person():
    db = ControlDB()
    persons = db.get_persons()
    if not request.json:
        abort(400)
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
    db.create_person(person_created)
    return jsonify({}), 201, {"Location": "/api/v1/persons/" + str(person_id)}

@app.route('/api/v1/persons/<int:person_id>', methods=['PATCH'])
def update_person(person_id):
    if not request.json:
        abort(400)
    db = ControlDB()
    persons = db.get_persons()
    person = list(filter(lambda t: t['id'] == person_id, persons))
    if len(person) == 0:
        abort(404)
    person_updated = {
        'id': person_id
    }
    request_data = request.get_json()
    if 'name' in request_data:
        person_updated['name'] = request.json['name']
    if 'age' in request_data:
        person_updated['age'] = request.json['age']
    if 'address' in request_data:
        person_updated['address'] = request.json['address']
    if 'work' in request_data:
        person_updated['work'] = request.json['work']
    if db.update_person(person_updated):
        persons_updateted = db.get_persons()
        updated_person = list(filter(lambda t: t['id'] == person_id, persons_updateted))
        if len(updated_person) == 0:
            abort(404)
        return make_response(jsonify(updated_person[0]), 200)
    else:
        abort(404)

@app.route('/api/v1/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    db = ControlDB()
    persons = db.get_persons()
    for p, person in enumerate(persons):
        if persons[p]['id'] == person_id:
            print("i have found")
            db.delete_person([person_id])
            break
        if (len(persons)) - 1 == p:
            abort(404)
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))
'''