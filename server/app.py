#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakeries_json = [{'id' : bakery.id, 'name': bakery.name} for bakery in all_bakeries]
    return jsonify(bakeries_json)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Query bakery by ID from the database
    bakery = Bakery.query.get(id)

    # Check if bakery with the specified ID exists
    if not bakery:
        return make_response(jsonify({'message': 'Bakery not found'}), 404)

    # Get baked goods associated with the bakery
    baked_goods = [{'id': good.id, 'name': good.name, 'price': good.price} for good in bakery.baked_goods]

    # Create bakery JSON object with nested baked goods
    bakery_json = {'id': bakery.id, 'name': bakery.name, 'baked_goods': baked_goods}

    # Return JSON response
    return jsonify(bakery_json)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query all baked goods from the database, sorted by price in descending order
    goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    # Convert baked goods to JSON objects
    goods_json = [{'id': good.id, 'name': good.name, 'price': good.price} for good in goods]

    # Return JSON response
    return jsonify(goods_json)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the single most expensive baked good from the database
    most_expensive_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    # Check if any baked goods exist
    if not most_expensive_good:
        return make_response(jsonify({'message': 'No baked goods found'}), 404)

    # Create JSON object for the most expensive baked good
    most_expensive_json = {'id': most_expensive_good.id, 'name': most_expensive_good.name, 'price': most_expensive_good.price}

    # Return JSON response
    return jsonify(most_expensive_json)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
