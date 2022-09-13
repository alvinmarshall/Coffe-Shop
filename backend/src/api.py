import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from backend.src.auth.auth import AuthError, requires_auth
from backend.src.database.models import db_drop_and_create_all, setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


# ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [d.long() for d in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    req = request.get_json()
    try:
        drink = Drink()
        drink.title = req['title']
        drink.recipe = json.dumps(req['recipe'])
        drink.insert()
        return jsonify({'success': True, 'drinks': [drink.long()]})
    except Exception as e:
        print(e)
        abort(400)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload,id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink:
        abort(404)
    try:
        req_title = req.get('title')
        req_recipe = req.get('recipe')
        if req_title:
            drink.title = req_title

        if req_recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update()
        return jsonify({'success': True, 'drinks': [drink.long()]}), 200
    except Exception as e:
        print(e)
        abort(400)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload,id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.delete()
        return jsonify({'success': True, 'delete': id}), 200
    except Exception as e:
        print(e)
        abort(400)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


if __name__ == '__main__':
    app.run()
