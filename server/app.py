#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurant_dict = []
    for restaurant in Restaurant.query.all():
        restaurant_dict.append(restaurant.to_dict())
    
    response  = make_response(
        restaurant_dict,
        200,
        {'Content-Type': 'application/json'}
    )
    return response
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
    if restaurant:
        return make_response(
            restaurant.to_dict(),
            200,
            {'Content-Type': 'application/json'}
        )
    else:
        return make_response(
            {'error': 'Restaurant not found'},
            404,
            {'Content-Type': 'application/json'}
        )
        
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(
            {'message': 'Restaurant deleted'},
            204,
            {'Content-Type': 'application/json'}
        )
    else:
        return make_response(
            {'error': 'Restaurant not found'},
            404,
            {'Content-Type': 'application/json'}
        )
        
@app.route('/pizzas', methods=['GET'])
def create_restaurant():
    pizza_dict = []
    pizzas=Pizza.query.all()
    if pizzas:
        for pizza in pizzas:
            pizza_dict.append(pizza.to_dict())
        return make_response(
            pizza_dict,
            200,
            {'Content-Type': 'application/json'}
        )
    else:
        return make_response(
            {'error': 'Pizza not found'},
            404,
            {'Content-Type': 'application/json'}
        )
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizzas():
    data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": ["validation errors"]}), 400               
if __name__ == "__main__":
    app.run(port=5550, debug=True)
