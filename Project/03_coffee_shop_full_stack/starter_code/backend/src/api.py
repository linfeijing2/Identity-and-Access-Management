import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES

def get_drinks_all(recipe):
    drinks = Drink.query.order_by(Drink.id).all()
    if recipe == "short":
        all_drinks = [drink.short() for drink in drinks]
    elif recipe == 'long':
        all_drinks = [drink.long() for drink in drinks]
    else:
        return abort(404)
    if len(all_drinks) == 0:
        abort(404)
    return all_drinks
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(token):
    return jsonify({'success': True, 'drinks':get_drinks_all("short")})

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    return jsonify({'success': True, 'drinks':get_drinks_all("long")})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(token):
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    new_drink = Drink(title=new_title, recipe=json.dumps(body['recipe']))
    new_drink.insert()
    
    return jsonify({'success': True, 'drinks': new_drink.long()})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(token, drink_id):
    body = json.loads(request.data.decode('utf-8'))
    if not body:
        abort(404, message="body not found")
    update_drink = Drink.query.filter(Drink.id ==drink_id).one_or_none()
    if not update_drink:
        abort(404, {'drink not found'})

    update_drink.title = body['title']
    update_drink.recipe = json.dumps(body['recipe'])
    update_drink.update()

    return jsonify({'success': True, 'drink': update_drink.long()})




'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token,drink_id):
    body = request.get_json()
    delete_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    delete_drink.delete()
    return jsonify({'success': True, 'delete': drink_id})
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


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def authentification_failed(AuthError): 
    return jsonify({
            "success": False, 
            "error": AuthError.status_code,
            "message": (AuthError.error['description'], "authentification fails")
            }), 401