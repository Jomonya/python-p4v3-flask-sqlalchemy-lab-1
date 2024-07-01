#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# Add views here

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    earthquake_list = [earthquake.to_dict() for earthquake in earthquakes]
    return make_response(jsonify(earthquake_list), 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Earthquake not found'}), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquake_list = [earthquake.to_dict() for earthquake in earthquakes]
    return make_response(jsonify(earthquake_list), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
